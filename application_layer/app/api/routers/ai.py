# api/routers/ai.py

from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query
from core.services.ai_service import AIService
from schemas.ai import (
    ProductRecommendationRequest, RecommendationResponse,
    FraudDetectionRequest, FraudDetectionResult,
    ComplianceMonitoringRequest, ComplianceResult,
    PredictiveMaintenanceRequest, MaintenancePrediction,
    SearchQuery, EnhancedSearchResponse, AIServiceResponse
)

router = APIRouter()
ai_service = AIService()


@router.post("/recommendations", response_model=RecommendationResponse)
async def get_product_recommendations(request: ProductRecommendationRequest):
    """
    Get personalized product recommendations using collaborative filtering,
    content-based filtering, and popularity-based approaches.
    """
    try:
        result = ai_service.get_product_recommendations(request)
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get product recommendations: {str(exc)}",
        )


@router.get("/recommendations/{user_id}", response_model=RecommendationResponse)
async def get_recommendations_simple(
    user_id: str,
    limit: int = Query(5, ge=1, le=20),
    category: Optional[str] = Query(None)
):
    """
    Get product recommendations for a user (simplified endpoint).
    """
    try:
        request = ProductRecommendationRequest(
            user_id=user_id,
            limit=limit,
            category=category
        )
        result = ai_service.get_product_recommendations(request)
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recommendations: {str(exc)}",
        )


@router.post("/fraud-detection", response_model=FraudDetectionResult)
async def detect_fraud(request: FraudDetectionRequest):
    """
    Advanced fraud detection using multiple signals including user behavior,
    transaction patterns, device fingerprinting, and risk scoring.
    """
    try:
        result = ai_service.detect_fraud(request)
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to detect fraud: {str(exc)}",
        )


@router.post("/compliance-monitoring", response_model=ComplianceResult)
async def monitor_compliance(request: ComplianceMonitoringRequest):
    """
    Monitor content for compliance with platform policies using NLP
    and rule-based analysis for prohibited content, spam, and scams.
    """
    try:
        result = ai_service.monitor_compliance(request)
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to monitor compliance: {str(exc)}",
        )


@router.post("/maintenance/predict", response_model=MaintenancePrediction)
async def predict_maintenance(request: PredictiveMaintenanceRequest):
    """
    Predict maintenance needs for robots based on sensor data,
    usage patterns, and historical maintenance records.
    """
    try:
        result = ai_service.predict_maintenance(request)
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to predict maintenance: {str(exc)}",
        )


@router.post("/search/enhanced", response_model=EnhancedSearchResponse)
async def enhanced_search(query: SearchQuery):
    """
    Enhanced search with AI-powered relevance scoring, personalization,
    and intelligent suggestions.
    """
    try:
        result = ai_service.enhanced_search(query)
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to perform enhanced search: {str(exc)}",
        )


@router.get("/search")
async def search_simple(
    q: str = Query(..., description="Search query"),
    user_id: Optional[str] = Query(None, description="User ID for personalization"),
    limit: int = Query(20, ge=1, le=100, description="Number of results")
):
    """
    Simple search endpoint with query parameter.
    """
    try:
        search_query = SearchQuery(
            query=q,
            user_id=user_id,
            limit=limit
        )
        result = ai_service.enhanced_search(search_query)
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to perform search: {str(exc)}",
        )
