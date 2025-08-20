# core/services/ai_service.py

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import re
import random

from core.config.settings import settings
from google.cloud import firestore
from schemas.ai import (
    ProductRecommendationRequest, ProductRecommendation, RecommendationResponse,
    FraudDetectionRequest, FraudDetectionResult, FraudRiskLevel,
    ComplianceMonitoringRequest, ComplianceResult, ComplianceStatus, ComplianceViolation,
    PredictiveMaintenanceRequest, MaintenancePrediction,
    SearchQuery, SearchResult, EnhancedSearchResponse
)


class AIService:
    def __init__(self):
        self.db = firestore.Client()
        self.prohibited_keywords = [
            "prohibited", "illegal", "banned", "restricted", "weapon", "drug",
            "explosive", "counterfeit", "stolen", "fraud", "scam"
        ]
        self.fraud_indicators = [
            "unusual_location", "high_velocity", "large_amount", "new_device",
            "suspicious_pattern", "blacklisted_ip"
        ]

    def get_product_recommendations(self, request: ProductRecommendationRequest) -> RecommendationResponse:
        """Get product recommendations for a user using collaborative filtering and content-based approaches"""
        try:
            # Get user's purchase history and preferences
            user_history = self._get_user_purchase_history(request.user_id)
            user_preferences = self._get_user_preferences(request.user_id)
            
            # Get products based on different recommendation strategies
            collaborative_recs = self._collaborative_filtering(request.user_id, user_history)
            content_based_recs = self._content_based_filtering(user_preferences, request.category)
            popularity_recs = self._popularity_based_recommendations(request.category)
            
            # Combine and score recommendations
            all_recommendations = {}
            
            # Weight collaborative filtering higher for users with purchase history
            collab_weight = 0.5 if user_history else 0.2
            content_weight = 0.3
            popularity_weight = 0.2
            
            for rec in collaborative_recs:
                product_id = rec["product_id"]
                all_recommendations[product_id] = all_recommendations.get(product_id, 0) + (rec["score"] * collab_weight)
            
            for rec in content_based_recs:
                product_id = rec["product_id"]
                all_recommendations[product_id] = all_recommendations.get(product_id, 0) + (rec["score"] * content_weight)
            
            for rec in popularity_recs:
                product_id = rec["product_id"]
                all_recommendations[product_id] = all_recommendations.get(product_id, 0) + (rec["score"] * popularity_weight)
            
            # Sort by combined score and get top recommendations
            sorted_recs = sorted(all_recommendations.items(), key=lambda x: x[1], reverse=True)[:request.limit]
            
            # Get detailed product information
            recommendations = []
            for product_id, score in sorted_recs:
                product_doc = self.db.collection(f"{settings.ENVIR}_robots").document(product_id).get()
                if product_doc.exists:
                    product_data = product_doc.to_dict()
                    
                    # Apply price range filter if specified
                    if request.price_range:
                        price = product_data.get("price", 0)
                        if price < request.price_range.get("min", 0) or price > request.price_range.get("max", float('inf')):
                            continue
                    
                    recommendation = ProductRecommendation(
                        product_id=product_id,
                        name=product_data.get("name", "Unknown"),
                        description=product_data.get("description", ""),
                        price=product_data.get("price", 0),
                        rating=product_data.get("ratings", {}).get("average", 0),
                        confidence_score=min(score, 1.0),
                        reason=self._generate_recommendation_reason(product_data, user_preferences)
                    )
                    recommendations.append(recommendation)
            
            return RecommendationResponse(
                user_id=request.user_id,
                recommendations=recommendations,
                total_count=len(recommendations),
                generated_at=datetime.utcnow()
            )
        except Exception as exc:
            print(f"Error getting product recommendations: {exc}")
            return RecommendationResponse(
                user_id=request.user_id,
                recommendations=[],
                total_count=0,
                generated_at=datetime.utcnow()
            )

    def detect_fraud(self, request: FraudDetectionRequest) -> FraudDetectionResult:
        """Advanced fraud detection using multiple signals and risk factors"""
        try:
            risk_score = 0.0
            risk_factors = []
            
            # Amount-based risk assessment
            if request.amount > 10000:
                risk_score += 0.3
                risk_factors.append("High transaction amount")
            elif request.amount > 5000:
                risk_score += 0.15
                risk_factors.append("Elevated transaction amount")
            
            # User behavior analysis
            user_history = self._get_user_transaction_history(request.user_id)
            if user_history:
                avg_amount = sum([t.get("amount", 0) for t in user_history]) / len(user_history)
                if request.amount > avg_amount * 5:
                    risk_score += 0.25
                    risk_factors.append("Amount significantly higher than user average")
                
                # Check transaction frequency
                recent_transactions = [t for t in user_history if 
                    (datetime.utcnow() - t.get("created_at", datetime.utcnow())).days <= 1]
                if len(recent_transactions) > 10:
                    risk_score += 0.2
                    risk_factors.append("High transaction frequency")
            else:
                risk_score += 0.1
                risk_factors.append("New user with no transaction history")
            
            # Device and location analysis
            if request.device_info:
                if request.device_info.get("is_new_device"):
                    risk_score += 0.15
                    risk_factors.append("Transaction from new device")
                
                if request.device_info.get("suspicious_fingerprint"):
                    risk_score += 0.2
                    risk_factors.append("Suspicious device fingerprint")
            
            # IP address analysis
            if request.ip_address:
                if self._is_suspicious_ip(request.ip_address):
                    risk_score += 0.25
                    risk_factors.append("Transaction from suspicious IP address")
            
            # Payment method risk
            if request.payment_method in ["cryptocurrency", "prepaid_card"]:
                risk_score += 0.1
                risk_factors.append("High-risk payment method")
            
            # Time-based analysis
            current_hour = datetime.utcnow().hour
            if current_hour < 6 or current_hour > 22:
                risk_score += 0.05
                risk_factors.append("Transaction during unusual hours")
            
            # Determine risk level and recommended action
            risk_level = FraudRiskLevel.LOW
            recommended_action = "approve"
            
            if risk_score >= 0.8:
                risk_level = FraudRiskLevel.CRITICAL
                recommended_action = "block_transaction"
            elif risk_score >= 0.6:
                risk_level = FraudRiskLevel.HIGH
                recommended_action = "manual_review"
            elif risk_score >= 0.4:
                risk_level = FraudRiskLevel.MEDIUM
                recommended_action = "additional_verification"
            
            is_fraudulent = risk_score >= 0.6
            
            return FraudDetectionResult(
                transaction_id=request.transaction_id,
                is_fraudulent=is_fraudulent,
                risk_score=min(risk_score, 1.0),
                risk_level=risk_level,
                risk_factors=risk_factors,
                recommended_action=recommended_action,
                confidence=0.85  # Model confidence
            )
        except Exception as exc:
            print(f"Error detecting fraud: {exc}")
            return FraudDetectionResult(
                transaction_id=request.transaction_id,
                is_fraudulent=False,
                risk_score=0.0,
                risk_level=FraudRiskLevel.LOW,
                risk_factors=[],
                recommended_action="approve",
                confidence=0.0
            )

    def monitor_compliance(self, request: ComplianceMonitoringRequest) -> ComplianceResult:
        """Advanced compliance monitoring using NLP and rule-based analysis"""
        try:
            violations = []
            overall_score = 1.0
            
            text_content = request.text_content.lower()
            
            # Check for prohibited keywords
            for keyword in self.prohibited_keywords:
                if keyword in text_content:
                    violation = ComplianceViolation(
                        violation_type="prohibited_content",
                        severity="high",
                        description=f"Contains prohibited keyword: {keyword}",
                        confidence=0.9
                    )
                    violations.append(violation)
                    overall_score -= 0.3
            
            # Check for spam patterns
            if self._detect_spam_patterns(text_content):
                violation = ComplianceViolation(
                    violation_type="spam_content",
                    severity="medium",
                    description="Content appears to be spam",
                    confidence=0.7
                )
                violations.append(violation)
                overall_score -= 0.2
            
            # Check for inappropriate language
            if self._detect_inappropriate_language(text_content):
                violation = ComplianceViolation(
                    violation_type="inappropriate_language",
                    severity="medium",
                    description="Contains inappropriate language",
                    confidence=0.8
                )
                violations.append(violation)
                overall_score -= 0.15
            
            # Check for potential scam indicators
            scam_indicators = self._detect_scam_indicators(text_content)
            if scam_indicators:
                violation = ComplianceViolation(
                    violation_type="potential_scam",
                    severity="high",
                    description=f"Potential scam indicators: {', '.join(scam_indicators)}",
                    confidence=0.75
                )
                violations.append(violation)
                overall_score -= 0.4
            
            # Check content length and quality
            if len(request.text_content.strip()) < 10:
                violation = ComplianceViolation(
                    violation_type="insufficient_content",
                    severity="low",
                    description="Content is too short or lacks detail",
                    confidence=0.9
                )
                violations.append(violation)
                overall_score -= 0.1
            
            # Determine compliance status
            overall_score = max(0.0, overall_score)
            
            if overall_score >= 0.8:
                status = ComplianceStatus.COMPLIANT
                recommended_action = "approve"
            elif overall_score >= 0.5:
                status = ComplianceStatus.REQUIRES_REVIEW
                recommended_action = "manual_review"
            else:
                status = ComplianceStatus.NON_COMPLIANT
                recommended_action = "reject"
            
            return ComplianceResult(
                content_id=request.content_id,
                is_compliant=status == ComplianceStatus.COMPLIANT,
                status=status,
                violations=violations,
                overall_score=overall_score,
                recommended_action=recommended_action
            )
        except Exception as exc:
            print(f"Error monitoring compliance: {exc}")
            return ComplianceResult(
                content_id=request.content_id,
                is_compliant=True,
                status=ComplianceStatus.COMPLIANT,
                violations=[],
                overall_score=1.0,
                recommended_action="approve"
            )

    def predict_maintenance(self, request: PredictiveMaintenanceRequest) -> MaintenancePrediction:
        """Predict maintenance needs for robots based on sensor data and usage patterns"""
        try:
            risk_factors = []
            maintenance_urgency = "low"
            predicted_failure_date = None
            recommended_actions = []
            
            # Analyze sensor data
            sensor_data = request.sensor_data
            
            # Temperature analysis
            if sensor_data.get("temperature", 0) > 80:
                risk_factors.append("High operating temperature")
                maintenance_urgency = "high"
                recommended_actions.append("Check cooling system")
            elif sensor_data.get("temperature", 0) > 70:
                risk_factors.append("Elevated temperature")
                if maintenance_urgency == "low":
                    maintenance_urgency = "medium"
            
            # Vibration analysis
            if sensor_data.get("vibration", 0) > 5.0:
                risk_factors.append("Excessive vibration detected")
                maintenance_urgency = "high"
                recommended_actions.append("Inspect mechanical components")
            elif sensor_data.get("vibration", 0) > 3.0:
                risk_factors.append("Increased vibration levels")
                if maintenance_urgency == "low":
                    maintenance_urgency = "medium"
            
            # Power consumption analysis
            if sensor_data.get("power_consumption", 0) > 150:
                risk_factors.append("High power consumption")
                recommended_actions.append("Check for inefficient components")
            
            # Usage hours analysis
            if request.usage_hours > 8760:  # More than 1 year of continuous operation
                risk_factors.append("High usage hours")
                recommended_actions.append("Schedule comprehensive maintenance")
                if maintenance_urgency == "low":
                    maintenance_urgency = "medium"
            
            # Last maintenance analysis
            if request.last_maintenance:
                days_since_maintenance = (datetime.utcnow() - request.last_maintenance).days
                if days_since_maintenance > 180:  # 6 months
                    risk_factors.append("Overdue for maintenance")
                    maintenance_urgency = "high"
                    recommended_actions.append("Schedule immediate maintenance")
                elif days_since_maintenance > 90:  # 3 months
                    risk_factors.append("Approaching maintenance interval")
                    if maintenance_urgency == "low":
                        maintenance_urgency = "medium"
            
            # Predict failure date based on risk factors
            if maintenance_urgency == "high":
                predicted_failure_date = datetime.utcnow() + timedelta(days=30)
            elif maintenance_urgency == "medium":
                predicted_failure_date = datetime.utcnow() + timedelta(days=90)
            
            # Default recommendations
            if not recommended_actions:
                recommended_actions = ["Regular inspection", "Lubricate moving parts"]
            
            # Calculate confidence based on available data
            confidence = 0.6
            if request.sensor_data:
                confidence += 0.2
            if request.maintenance_history:
                confidence += 0.1
            if request.last_maintenance:
                confidence += 0.1
            
            return MaintenancePrediction(
                robot_id=request.robot_id,
                predicted_failure_date=predicted_failure_date,
                maintenance_urgency=maintenance_urgency,
                recommended_actions=recommended_actions,
                confidence=min(confidence, 1.0),
                risk_factors=risk_factors
            )
        except Exception as exc:
            print(f"Error predicting maintenance: {exc}")
            return MaintenancePrediction(
                robot_id=request.robot_id,
                predicted_failure_date=None,
                maintenance_urgency="low",
                recommended_actions=["Regular inspection"],
                confidence=0.0,
                risk_factors=[]
            )

    def enhanced_search(self, query: SearchQuery) -> EnhancedSearchResponse:
        """Enhanced search with AI-powered relevance scoring and suggestions"""
        try:
            start_time = datetime.utcnow()
            
            # Process search query
            processed_query = self._process_search_query(query.query)
            
            # Search in products collection
            products_ref = self.db.collection(f"{settings.ENVIR}_robots")
            
            # Basic text search (in a real implementation, this would use full-text search)
            all_products = list(products_ref.stream())
            
            results = []
            for doc in all_products:
                product_data = doc.to_dict()
                relevance_score = self._calculate_relevance_score(
                    processed_query, product_data, query.user_id
                )
                
                if relevance_score > 0.1:  # Minimum relevance threshold
                    # Apply filters
                    if self._apply_filters(product_data, query.filters):
                        result = SearchResult(
                            item_id=doc.id,
                            title=product_data.get("name", ""),
                            description=product_data.get("description", ""),
                            relevance_score=relevance_score,
                            category=product_data.get("category", ""),
                            metadata={
                                "price": product_data.get("price", 0),
                                "rating": product_data.get("ratings", {}).get("average", 0),
                                "seller_id": product_data.get("seller_id", "")
                            }
                        )
                        results.append(result)
            
            # Sort by relevance score
            results.sort(key=lambda x: x.relevance_score, reverse=True)
            
            # Limit results
            limited_results = results[:query.limit]
            
            # Generate search suggestions
            suggestions = self._generate_search_suggestions(query.query, results)
            
            # Calculate search time
            search_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            return EnhancedSearchResponse(
                query=query.query,
                results=limited_results,
                total_count=len(results),
                suggestions=suggestions,
                filters_applied=query.filters or {},
                search_time_ms=search_time
            )
        except Exception as exc:
            print(f"Error in enhanced search: {exc}")
            return EnhancedSearchResponse(
                query=query.query,
                results=[],
                total_count=0,
                suggestions=[],
                filters_applied={},
                search_time_ms=0.0
            )

    # Helper methods
    def _get_user_purchase_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's purchase history"""
        try:
            orders_ref = self.db.collection(f"{settings.ENVIR}_orders")
            user_orders = orders_ref.where("buyer_id", "==", user_id).stream()
            return [doc.to_dict() for doc in user_orders]
        except:
            return []

    def _get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences and behavior patterns"""
        try:
            user_doc = self.db.collection(f"{settings.ENVIR}_users").document(user_id).get()
            if user_doc.exists:
                return user_doc.to_dict().get("preferences", {})
            return {}
        except:
            return {}

    def _collaborative_filtering(self, user_id: str, user_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Simple collaborative filtering implementation"""
        # Simplified implementation - in production, this would use more sophisticated algorithms
        recommendations = []
        if user_history:
            # Find similar users and recommend their purchases
            # This is a placeholder implementation
            for i in range(3):
                recommendations.append({
                    "product_id": f"collab_rec_{i}",
                    "score": 0.8 - (i * 0.1)
                })
        return recommendations

    def _content_based_filtering(self, user_preferences: Dict[str, Any], category: Optional[str]) -> List[Dict[str, Any]]:
        """Content-based filtering based on user preferences"""
        recommendations = []
        # Simplified implementation
        for i in range(3):
            recommendations.append({
                "product_id": f"content_rec_{i}",
                "score": 0.7 - (i * 0.1)
            })
        return recommendations

    def _popularity_based_recommendations(self, category: Optional[str]) -> List[Dict[str, Any]]:
        """Get popular products as recommendations"""
        try:
            products_ref = self.db.collection(f"{settings.ENVIR}_robots")
            if category:
                products_ref = products_ref.where("category", "==", category)
            
            # Get products ordered by rating
            products = products_ref.order_by("ratings.average", direction=firestore.Query.DESCENDING).limit(5).stream()
            
            recommendations = []
            for i, doc in enumerate(products):
                recommendations.append({
                    "product_id": doc.id,
                    "score": 0.6 - (i * 0.1)
                })
            
            return recommendations
        except:
            return []

    def _generate_recommendation_reason(self, product_data: Dict[str, Any], user_preferences: Dict[str, Any]) -> str:
        """Generate a reason for the recommendation"""
        reasons = [
            "Popular in your category",
            "Highly rated by other users",
            "Matches your interests",
            "Trending product",
            "Good value for money"
        ]
        return random.choice(reasons)

    def _get_user_transaction_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's transaction history for fraud analysis"""
        try:
            orders_ref = self.db.collection(f"{settings.ENVIR}_orders")
            user_orders = orders_ref.where("buyer_id", "==", user_id).limit(50).stream()
            return [doc.to_dict() for doc in user_orders]
        except:
            return []

    def _is_suspicious_ip(self, ip_address: str) -> bool:
        """Check if IP address is suspicious"""
        # Simplified implementation - in production, this would check against threat intelligence
        suspicious_patterns = ["10.0.0.", "192.168.", "127.0.0."]
        return any(pattern in ip_address for pattern in suspicious_patterns)

    def _detect_spam_patterns(self, text: str) -> bool:
        """Detect spam patterns in text"""
        spam_indicators = [
            r'click here', r'free money', r'guaranteed', r'act now',
            r'limited time', r'urgent', r'congratulations'
        ]
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in spam_indicators)

    def _detect_inappropriate_language(self, text: str) -> bool:
        """Detect inappropriate language"""
        # Simplified implementation
        inappropriate_words = ["hate", "offensive", "inappropriate"]
        return any(word in text for word in inappropriate_words)

    def _detect_scam_indicators(self, text: str) -> List[str]:
        """Detect potential scam indicators"""
        indicators = []
        scam_patterns = {
            r'send money': "Money transfer request",
            r'wire transfer': "Wire transfer mention",
            r'urgent payment': "Urgent payment request",
            r'verify account': "Account verification request"
        }
        
        for pattern, description in scam_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                indicators.append(description)
        
        return indicators

    def _process_search_query(self, query: str) -> str:
        """Process and clean search query"""
        # Remove special characters, normalize case, etc.
        return query.lower().strip()

    def _calculate_relevance_score(self, query: str, product_data: Dict[str, Any], user_id: Optional[str]) -> float:
        """Calculate relevance score for search results"""
        score = 0.0
        
        # Text matching
        name = product_data.get("name", "").lower()
        description = product_data.get("description", "").lower()
        
        if query in name:
            score += 0.8
        elif any(word in name for word in query.split()):
            score += 0.5
        
        if query in description:
            score += 0.3
        elif any(word in description for word in query.split()):
            score += 0.2
        
        # Rating boost
        rating = product_data.get("ratings", {}).get("average", 0)
        score += (rating / 5.0) * 0.2
        
        return min(score, 1.0)

    def _apply_filters(self, product_data: Dict[str, Any], filters: Optional[Dict[str, Any]]) -> bool:
        """Apply search filters"""
        if not filters:
            return True
        
        # Price filter
        if "price_range" in filters:
            price = product_data.get("price", 0)
            price_range = filters["price_range"]
            if price < price_range.get("min", 0) or price > price_range.get("max", float('inf')):
                return False
        
        # Category filter
        if "category" in filters:
            if product_data.get("category") != filters["category"]:
                return False
        
        return True

    def _generate_search_suggestions(self, query: str, results: List[SearchResult]) -> List[str]:
        """Generate search suggestions"""
        suggestions = []
        
        # Extract categories from results
        categories = list(set([result.category for result in results[:5]]))
        for category in categories:
            suggestions.append(f"{query} {category}")
        
        # Add common search refinements
        common_refinements = ["cheap", "best", "new", "used", "professional"]
        for refinement in common_refinements[:3]:
            suggestions.append(f"{refinement} {query}")
        
        return suggestions[:5]
