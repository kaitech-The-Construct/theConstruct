# api/routers/ai.py

from core.services.ai_service import AIService
from fastapi import APIRouter, HTTPException, status

router = APIRouter()
ai_service = AIService()


@router.get("/recommendations/{user_id}")
async def get_recommendations(user_id: str):
    """
    Get product recommendations for a user.
    """
    recommendations = ai_service.get_product_recommendations(user_id)
    return {"recommendations": recommendations}


@router.post("/fraud-detection")
async def detect_fraud(transaction_data: dict):
    """
    Detect fraudulent transactions.
    """
    result = ai_service.detect_fraud(transaction_data)
    return result


@router.post("/compliance-monitoring")
async def monitor_compliance(data: dict):
    """
    Monitor for compliance with platform policies.
    """
    result = ai_service.monitor_compliance(data)
    return result
