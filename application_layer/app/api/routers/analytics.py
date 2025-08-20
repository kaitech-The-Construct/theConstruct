# api/routers/analytics.py

from core.services.analytics_service import AnalyticsService
from fastapi import APIRouter, HTTPException, status

router = APIRouter()
analytics_service = AnalyticsService()


@router.get("/marketplace/metrics")
async def get_marketplace_metrics():
    """
    Get real-time metrics for the marketplace.
    """
    result = analytics_service.generate_marketplace_metrics()
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("message", "Failed to generate metrics"),
        )
    return result


@router.get("/users/{user_id}/behavior")
async def get_user_behavior(user_id: str):
    """
    Track user behavior and activity.
    """
    result = analytics_service.track_user_behavior(user_id)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("message", "Failed to track behavior"),
        )
    return result


@router.post("/reports/financial")
async def create_financial_report(date_range: dict):
    """
    Create a financial report for a given date range.
    """
    result = analytics_service.create_financial_reports(date_range)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("message", "Failed to create report"),
        )
    return result
