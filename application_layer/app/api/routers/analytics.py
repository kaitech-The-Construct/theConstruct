# api/routers/analytics.py

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, status, Query
from core.services.analytics_service import AnalyticsService
from schemas.analytics import (
    DateRange, MarketplaceMetrics, UserBehavior, FinancialReport,
    DemandForecast, SystemMetrics, AnalyticsResponse
)

router = APIRouter()
analytics_service = AnalyticsService()


@router.get("/marketplace/metrics", response_model=MarketplaceMetrics)
async def get_marketplace_metrics():
    """
    Get real-time metrics for the marketplace including products, users, orders, and revenue.
    """
    try:
        result = analytics_service.generate_marketplace_metrics()
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate marketplace metrics: {str(exc)}",
        )


@router.get("/users/{user_id}/behavior", response_model=UserBehavior)
async def get_user_behavior(user_id: str):
    """
    Track user behavior and activity including logins, product views, and session data.
    """
    try:
        result = analytics_service.track_user_behavior(user_id)
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to track user behavior: {str(exc)}",
        )


@router.post("/reports/financial", response_model=FinancialReport)
async def create_financial_report(date_range: DateRange):
    """
    Create a comprehensive financial report for a given date range including revenue,
    top-selling products, and category breakdowns.
    """
    try:
        result = analytics_service.create_financial_reports(date_range)
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create financial report: {str(exc)}",
        )


@router.get("/demand/forecast/{product_category}", response_model=DemandForecast)
async def get_demand_forecast(product_category: str):
    """
    Get demand forecast for a specific product category using historical data and trends.
    """
    try:
        result = analytics_service.predict_demand_trends(product_category)
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate demand forecast: {str(exc)}",
        )


@router.get("/system/performance", response_model=SystemMetrics)
async def get_system_performance():
    """
    Get current system performance metrics including CPU, memory, disk usage, and API metrics.
    """
    try:
        result = analytics_service.monitor_system_performance()
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get system performance metrics: {str(exc)}",
        )


@router.post("/activity/log")
async def log_user_activity(
    user_id: str,
    activity_type: str,
    metadata: Dict[str, Any] = None
):
    """
    Log user activity for analytics tracking.
    """
    try:
        success = analytics_service.log_user_activity(user_id, activity_type, metadata)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to log user activity"
            )
        return {"message": "Activity logged successfully"}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to log activity: {str(exc)}",
        )


@router.get("/products/popular")
async def get_popular_products(limit: int = Query(10, ge=1, le=50)):
    """
    Get most popular products based on views and orders.
    """
    try:
        result = analytics_service.get_popular_products(limit)
        return {"popular_products": result}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get popular products: {str(exc)}",
        )
