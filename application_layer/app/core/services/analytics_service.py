# core/services/analytics_service.py

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import psutil
import time

from core.config.settings import settings
from google.cloud import firestore
from schemas.analytics import (
    MarketplaceMetrics, UserBehavior, FinancialReport, 
    DemandForecast, SystemMetrics, DateRange
)


class AnalyticsService:
    def __init__(self):
        self.db = firestore.Client()

    def generate_marketplace_metrics(self) -> MarketplaceMetrics:
        """Generate real-time marketplace metrics"""
        try:
            # Get total products
            products_count = len(list(self.db.collection(f"{settings.ENVIR}_robots").stream()))
            
            # Get total users
            users_count = len(list(self.db.collection(f"{settings.ENVIR}_users").stream()))
            
            # Get total orders
            orders_count = len(list(self.db.collection(f"{settings.ENVIR}_orders").stream()))
            
            # Get active users in last 24 hours
            yesterday = datetime.utcnow() - timedelta(days=1)
            active_users_query = self.db.collection(f"{settings.ENVIR}_activities").where(
                "created_at", ">=", yesterday
            ).where("type", "==", "login")
            active_users_24h = len(set([doc.to_dict().get("userId") for doc in active_users_query.stream()]))
            
            # Get revenue in last 24 hours
            orders_24h_query = self.db.collection(f"{settings.ENVIR}_orders").where(
                "created_at", ">=", yesterday
            )
            revenue_24h = sum([doc.to_dict().get("total_price", 0) for doc in orders_24h_query.stream()])
            
            return MarketplaceMetrics(
                total_products=products_count,
                total_users=users_count,
                total_orders=orders_count,
                active_users_24h=active_users_24h,
                revenue_24h=revenue_24h,
                last_updated=datetime.utcnow()
            )
        except Exception as exc:
            print(f"Error generating marketplace metrics: {exc}")
            raise Exception("Metrics generation failed")

    def track_user_behavior(self, user_id: str) -> UserBehavior:
        """Track user behavior and activity"""
        try:
            # Get user activity history
            activities_ref = self.db.collection(f"{settings.ENVIR}_activities")
            docs = activities_ref.where("userId", "==", user_id).stream()
            
            activity_summary = {
                "total_logins": 0,
                "products_viewed": 0,
                "orders_placed": 0,
                "session_durations": []
            }
            last_activity = None
            
            for doc in docs:
                activity = doc.to_dict()
                activity_time = activity.get("created_at")
                if activity_time and (not last_activity or activity_time > last_activity):
                    last_activity = activity_time
                    
                if activity.get("type") == "login":
                    activity_summary["total_logins"] += 1
                elif activity.get("type") == "view_product":
                    activity_summary["products_viewed"] += 1
                elif activity.get("type") == "place_order":
                    activity_summary["orders_placed"] += 1
                elif activity.get("type") == "session_end":
                    duration = activity.get("duration", 0)
                    activity_summary["session_durations"].append(duration)
            
            avg_session_duration = (
                sum(activity_summary["session_durations"]) / len(activity_summary["session_durations"])
                if activity_summary["session_durations"] else 0
            )
            
            return UserBehavior(
                user_id=user_id,
                total_logins=activity_summary["total_logins"],
                products_viewed=activity_summary["products_viewed"],
                orders_placed=activity_summary["orders_placed"],
                avg_session_duration=avg_session_duration,
                last_activity=last_activity or datetime.utcnow()
            )
        except Exception as exc:
            print(f"Error tracking user behavior: {exc}")
            raise Exception("Behavior tracking failed")

    def create_financial_reports(self, date_range: DateRange) -> FinancialReport:
        """Create financial reports"""
        try:
            # Query orders within date range
            orders_ref = self.db.collection(f"{settings.ENVIR}_orders")
            docs = orders_ref.where("created_at", ">=", date_range.start_date).where(
                "created_at", "<=", date_range.end_date
            ).stream()
            
            total_revenue = 0
            total_orders = 0
            category_revenue = {}
            product_sales = {}
            
            for doc in docs:
                order = doc.to_dict()
                order_value = order.get("total_price", 0)
                total_revenue += order_value
                total_orders += 1
                
                # Track by category
                product_id = order.get("product_id")
                if product_id:
                    # Get product details for category
                    product_doc = self.db.collection(f"{settings.ENVIR}_robots").document(product_id).get()
                    if product_doc.exists:
                        product_data = product_doc.to_dict()
                        category = product_data.get("category", "Unknown")
                        category_revenue[category] = category_revenue.get(category, 0) + order_value
                        
                        # Track product sales
                        product_name = product_data.get("name", "Unknown")
                        if product_name not in product_sales:
                            product_sales[product_name] = {"sales": 0, "revenue": 0}
                        product_sales[product_name]["sales"] += 1
                        product_sales[product_name]["revenue"] += order_value
            
            # Get top selling products
            top_selling = sorted(
                product_sales.items(), 
                key=lambda x: x[1]["revenue"], 
                reverse=True
            )[:10]
            
            top_selling_products = [
                {"name": name, "sales": data["sales"], "revenue": data["revenue"]}
                for name, data in top_selling
            ]
            
            return FinancialReport(
                date_range=date_range,
                total_revenue=total_revenue,
                total_orders=total_orders,
                average_order_value=total_revenue / total_orders if total_orders > 0 else 0,
                top_selling_products=top_selling_products,
                revenue_by_category=category_revenue
            )
        except Exception as exc:
            print(f"Error creating financial reports: {exc}")
            raise Exception("Financial report creation failed")

    def predict_demand_trends(self, product_category: str) -> DemandForecast:
        """Predict demand trends for a product category"""
        try:
            # Get historical sales data for the category
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            
            # Query recent orders for products in this category
            orders_ref = self.db.collection(f"{settings.ENVIR}_orders")
            recent_orders = orders_ref.where("created_at", ">=", thirty_days_ago).stream()
            
            category_orders = []
            for doc in recent_orders:
                order = doc.to_dict()
                product_id = order.get("product_id")
                if product_id:
                    product_doc = self.db.collection(f"{settings.ENVIR}_robots").document(product_id).get()
                    if product_doc.exists:
                        product_data = product_doc.to_dict()
                        if product_data.get("category") == product_category:
                            category_orders.append(order)
            
            # Simple trend analysis (in a real implementation, this would use ML models)
            recent_demand = len(category_orders)
            
            # Calculate trend factors
            factors = []
            if recent_demand > 10:
                factors.append("High recent activity")
            if len(category_orders) > 0:
                avg_price = sum([order.get("total_price", 0) for order in category_orders]) / len(category_orders)
                if avg_price < 1000:
                    factors.append("Affordable price point")
                factors.append("Market interest")
            
            # Simple prediction logic
            predicted_demand = recent_demand * 1.2  # 20% growth assumption
            confidence = min(0.8, len(category_orders) / 20)  # Higher confidence with more data
            
            return DemandForecast(
                product_category=product_category,
                predicted_demand=predicted_demand,
                confidence_score=confidence,
                forecast_period="30 days",
                factors=factors
            )
        except Exception as exc:
            print(f"Error predicting demand trends: {exc}")
            raise Exception("Demand prediction failed")

    def monitor_system_performance(self) -> SystemMetrics:
        """Monitor system performance metrics"""
        try:
            # Get system metrics
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Simulate API response time (in a real implementation, this would be tracked)
            api_response_time = 150.0  # milliseconds
            
            # Simulate active connections (would be tracked by load balancer/proxy)
            active_connections = 45
            
            # Simulate error rate (would be tracked by monitoring system)
            error_rate = 0.5  # percentage
            
            return SystemMetrics(
                cpu_usage=cpu_usage,
                memory_usage=memory.percent,
                disk_usage=disk.percent,
                api_response_time=api_response_time,
                active_connections=active_connections,
                error_rate=error_rate,
                timestamp=datetime.utcnow()
            )
        except Exception as exc:
            print(f"Error monitoring system performance: {exc}")
            raise Exception("System monitoring failed")

    def log_user_activity(self, user_id: str, activity_type: str, metadata: Dict[str, Any] = None) -> bool:
        """Log user activity for analytics"""
        try:
            activity_record = {
                "userId": user_id,
                "type": activity_type,
                "metadata": metadata or {},
                "created_at": firestore.SERVER_TIMESTAMP
            }
            self.db.collection(f"{settings.ENVIR}_activities").add(activity_record)
            return True
        except Exception as exc:
            print(f"Error logging user activity: {exc}")
            return False

    def get_popular_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most popular products based on views and orders"""
        try:
            # Get product view counts from activities
            activities_ref = self.db.collection(f"{settings.ENVIR}_activities")
            view_activities = activities_ref.where("type", "==", "view_product").stream()
            
            product_views = {}
            for doc in view_activities:
                activity = doc.to_dict()
                product_id = activity.get("metadata", {}).get("product_id")
                if product_id:
                    product_views[product_id] = product_views.get(product_id, 0) + 1
            
            # Sort by popularity and get top products
            popular_product_ids = sorted(
                product_views.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:limit]
            
            # Get product details
            popular_products = []
            for product_id, view_count in popular_product_ids:
                product_doc = self.db.collection(f"{settings.ENVIR}_robots").document(product_id).get()
                if product_doc.exists:
                    product_data = product_doc.to_dict()
                    product_data["view_count"] = view_count
                    product_data["product_id"] = product_id
                    popular_products.append(product_data)
            
            return popular_products
        except Exception as exc:
            print(f"Error getting popular products: {exc}")
            return []
