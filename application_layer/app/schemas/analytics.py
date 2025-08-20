# schemas/analytics.py

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class DateRange(BaseModel):
    start_date: datetime = Field(..., description="Start date for the report")
    end_date: datetime = Field(..., description="End date for the report")


class MarketplaceMetrics(BaseModel):
    total_products: int = Field(..., description="Total number of products")
    total_users: int = Field(..., description="Total number of users")
    total_orders: int = Field(..., description="Total number of orders")
    active_users_24h: int = Field(..., description="Active users in last 24 hours")
    revenue_24h: float = Field(..., description="Revenue in last 24 hours")
    last_updated: datetime = Field(..., description="Last update timestamp")


class UserBehavior(BaseModel):
    user_id: str = Field(..., description="User ID")
    total_logins: int = Field(..., description="Total number of logins")
    products_viewed: int = Field(..., description="Number of products viewed")
    orders_placed: int = Field(..., description="Number of orders placed")
    avg_session_duration: float = Field(..., description="Average session duration in minutes")
    last_activity: datetime = Field(..., description="Last activity timestamp")


class FinancialReport(BaseModel):
    date_range: DateRange = Field(..., description="Date range for the report")
    total_revenue: float = Field(..., description="Total revenue")
    total_orders: int = Field(..., description="Total number of orders")
    average_order_value: float = Field(..., description="Average order value")
    top_selling_products: List[dict] = Field(..., description="Top selling products")
    revenue_by_category: dict = Field(..., description="Revenue breakdown by category")


class DemandForecast(BaseModel):
    product_category: str = Field(..., description="Product category")
    predicted_demand: float = Field(..., description="Predicted demand")
    confidence_score: float = Field(..., description="Confidence score (0-1)")
    forecast_period: str = Field(..., description="Forecast period (e.g., '30 days')")
    factors: List[str] = Field(..., description="Factors influencing the forecast")


class SystemMetrics(BaseModel):
    cpu_usage: float = Field(..., description="CPU usage percentage")
    memory_usage: float = Field(..., description="Memory usage percentage")
    disk_usage: float = Field(..., description="Disk usage percentage")
    api_response_time: float = Field(..., description="Average API response time in ms")
    active_connections: int = Field(..., description="Number of active connections")
    error_rate: float = Field(..., description="Error rate percentage")
    timestamp: datetime = Field(..., description="Metrics timestamp")


class AnalyticsResponse(BaseModel):
    success: bool = Field(..., description="Success status")
    data: Optional[dict] = Field(None, description="Response data")
    message: Optional[str] = Field(None, description="Response message")
