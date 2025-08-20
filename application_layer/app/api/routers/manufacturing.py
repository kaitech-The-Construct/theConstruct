# api/routers/manufacturing.py

from typing import List

from core.services.manufacturing_service import ManufacturingService
from fastapi import APIRouter, HTTPException, status

router = APIRouter()
manufacturing_service = ManufacturingService()


@router.post("/rfq")
async def request_for_quote(rfq_data: dict):
    """
    Submit a request for quote (RFQ) to the manufacturing network.
    """
    result = manufacturing_service.process_quote_request(rfq_data)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "RFQ submission failed"),
        )
    return result


@router.get("/rfq/{rfq_id}/quotes")
async def get_quotes(rfq_id: str):
    """
    Get quotes for a specific RFQ.
    """
    quotes = manufacturing_service.get_quotes_for_rfq(rfq_id)
    return {"quotes": quotes}


@router.post("/orders")
async def create_manufacturing_order(order_data: dict):
    """
    Create a new manufacturing order.
    """
    result = manufacturing_service.manage_manufacturing_order(order_data)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Order creation failed"),
        )
    return result


@router.get("/orders/{order_id}")
async def get_manufacturing_order(order_id: str):
    """
    Get details for a specific manufacturing order.
    """
    # This would typically query the manufacturing orders collection
    # For now, return placeholder data
    return {"order_id": order_id, "status": "in_production"}


@router.get("/orders/{order_id}/milestones")
async def get_milestones(order_id: str):
    """
    Get production milestones for a manufacturing order.
    """
    milestones = manufacturing_service.track_production_milestones(order_id)
    return {"milestones": milestones}


@router.post("/quality-report")
async def submit_quality_report(report_data: dict):
    """
    Submit a quality control report for a manufacturing order.
    """
    order_id = report_data.get("order_id")
    if not order_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order ID is required",
        )
    result = manufacturing_service.handle_quality_control(order_id, report_data)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "QC report submission failed"),
        )
    return result


@router.put("/orders/{order_id}/milestone")
async def update_milestone(order_id: str, milestone_data: dict):
    """
    Update a milestone for a manufacturing order.
    """
    milestone_id = milestone_data.get("milestone_id")
    status = milestone_data.get("status")
    
    if not milestone_id or not status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Milestone ID and status are required",
        )
    
    result = manufacturing_service.update_milestone_status(order_id, milestone_id, status)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Milestone update failed"),
        )
    return result


@router.post("/suppliers")
async def register_supplier(supplier_data: dict):
    """
    Register a new supplier in the network.
    """
    result = manufacturing_service.manage_supplier_network(supplier_data)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Supplier registration failed"),
        )
    return result
