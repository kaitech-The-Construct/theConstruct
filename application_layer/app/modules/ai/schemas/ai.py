# schemas/ai.py

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class RecommendationType(str, Enum):
    PRODUCT = "product"
    CONTENT = "content"
    USER = "user"
    CATEGORY = "category"


class FraudRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComplianceStatus(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    REQUIRES_REVIEW = "requires_review"


class ProductRecommendationRequest(BaseModel):
    user_id: str = Field(..., description="User ID to get recommendations for")
    limit: int = Field(5, description="Number of recommendations to return")
    category: Optional[str] = Field(None, description="Filter by product category")
    price_range: Optional[Dict[str, float]] = Field(None, description="Price range filter")


class ProductRecommendation(BaseModel):
    product_id: str = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    description: str = Field(..., description="Product description")
    price: float = Field(..., description="Product price")
    rating: float = Field(..., description="Product rating")
    confidence_score: float = Field(..., description="Recommendation confidence (0-1)")
    reason: str = Field(..., description="Reason for recommendation")


class RecommendationResponse(BaseModel):
    user_id: str = Field(..., description="User ID")
    recommendations: List[ProductRecommendation] = Field(..., description="List of recommendations")
    total_count: int = Field(..., description="Total number of available recommendations")
    generated_at: datetime = Field(..., description="Timestamp when recommendations were generated")


class FraudDetectionRequest(BaseModel):
    transaction_id: Optional[str] = Field(None, description="Transaction ID")
    user_id: str = Field(..., description="User ID")
    amount: float = Field(..., description="Transaction amount")
    currency: str = Field(..., description="Transaction currency")
    payment_method: str = Field(..., description="Payment method used")
    ip_address: Optional[str] = Field(None, description="User IP address")
    device_info: Optional[Dict[str, Any]] = Field(None, description="Device information")
    transaction_data: Dict[str, Any] = Field(..., description="Additional transaction data")


class FraudDetectionResult(BaseModel):
    transaction_id: Optional[str] = Field(None, description="Transaction ID")
    is_fraudulent: bool = Field(..., description="Whether transaction is flagged as fraudulent")
    risk_score: float = Field(..., description="Fraud risk score (0-1)")
    risk_level: FraudRiskLevel = Field(..., description="Risk level classification")
    risk_factors: List[str] = Field(..., description="Identified risk factors")
    recommended_action: str = Field(..., description="Recommended action to take")
    confidence: float = Field(..., description="Model confidence (0-1)")


class ComplianceMonitoringRequest(BaseModel):
    content_id: Optional[str] = Field(None, description="Content ID")
    content_type: str = Field(..., description="Type of content (product, review, message)")
    text_content: str = Field(..., description="Text content to analyze")
    user_id: Optional[str] = Field(None, description="User ID who created the content")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ComplianceViolation(BaseModel):
    violation_type: str = Field(..., description="Type of violation")
    severity: str = Field(..., description="Violation severity")
    description: str = Field(..., description="Description of the violation")
    confidence: float = Field(..., description="Detection confidence (0-1)")


class ComplianceResult(BaseModel):
    content_id: Optional[str] = Field(None, description="Content ID")
    is_compliant: bool = Field(..., description="Whether content is compliant")
    status: ComplianceStatus = Field(..., description="Compliance status")
    violations: List[ComplianceViolation] = Field(..., description="List of violations found")
    overall_score: float = Field(..., description="Overall compliance score (0-1)")
    recommended_action: str = Field(..., description="Recommended action")


class PredictiveMaintenanceRequest(BaseModel):
    robot_id: str = Field(..., description="Robot ID")
    sensor_data: Dict[str, float] = Field(..., description="Current sensor readings")
    usage_hours: float = Field(..., description="Total usage hours")
    last_maintenance: Optional[datetime] = Field(None, description="Last maintenance date")
    maintenance_history: Optional[List[Dict[str, Any]]] = Field(None, description="Maintenance history")


class MaintenancePrediction(BaseModel):
    robot_id: str = Field(..., description="Robot ID")
    predicted_failure_date: Optional[datetime] = Field(None, description="Predicted failure date")
    maintenance_urgency: str = Field(..., description="Maintenance urgency level")
    recommended_actions: List[str] = Field(..., description="Recommended maintenance actions")
    confidence: float = Field(..., description="Prediction confidence (0-1)")
    risk_factors: List[str] = Field(..., description="Identified risk factors")


class SearchQuery(BaseModel):
    query: str = Field(..., description="Search query")
    user_id: Optional[str] = Field(None, description="User ID for personalization")
    filters: Optional[Dict[str, Any]] = Field(None, description="Search filters")
    limit: int = Field(20, description="Number of results to return")


class SearchResult(BaseModel):
    item_id: str = Field(..., description="Item ID")
    title: str = Field(..., description="Item title")
    description: str = Field(..., description="Item description")
    relevance_score: float = Field(..., description="Relevance score (0-1)")
    category: str = Field(..., description="Item category")
    metadata: Dict[str, Any] = Field(..., description="Additional metadata")


class EnhancedSearchResponse(BaseModel):
    query: str = Field(..., description="Original search query")
    results: List[SearchResult] = Field(..., description="Search results")
    total_count: int = Field(..., description="Total number of results")
    suggestions: List[str] = Field(..., description="Search suggestions")
    filters_applied: Dict[str, Any] = Field(..., description="Applied filters")
    search_time_ms: float = Field(..., description="Search execution time in milliseconds")


class AIServiceResponse(BaseModel):
    success: bool = Field(..., description="Success status")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    message: Optional[str] = Field(None, description="Response message")
    timestamp: datetime = Field(..., description="Response timestamp")
