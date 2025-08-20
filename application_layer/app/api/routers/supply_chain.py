# api/routers/supply_chain.py

from core.services.supply_chain_service import SupplyChainService
from fastapi import APIRouter, HTTPException, status

router = APIRouter()
supply_chain_service = SupplyChainService()


@router.post("/shipments")
async def create_shipment(shipment_data: dict):
    """
    Create a new shipment for a manufacturing order.
    """
    result = supply_chain_service.create_shipment(shipment_data)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Shipment creation failed"),
        )
    return result


@router.get("/shipments/track/{tracking_number}")
async def track_shipment(tracking_number: str):
    """
    Track a shipment using its tracking number.
    """
    result = supply_chain_service.track_shipment(tracking_number)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("message", "Shipment not found"),
        )
    return result


@router.post("/inventory")
async def manage_inventory(inventory_data: dict):
    """
    Manage inventory for a manufacturer.
    """
    result = supply_chain_service.manage_inventory(inventory_data)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Inventory management failed"),
        )
    return result


@router.put("/shipments/{shipment_id}/status")
async def update_shipment_status(shipment_id: str, status_data: dict):
    """
    Update shipment status and location.
    """
    status = status_data.get("status")
    location = status_data.get("location")
    
    if not status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status is required",
        )
    
    result = supply_chain_service.update_shipment_status(shipment_id, status, location)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Shipment status update failed"),
        )
    return result


@router.post("/shipments/{shipment_id}/delivery")
async def confirm_delivery(shipment_id: str, delivery_data: dict):
    """
    Confirm delivery of a shipment.
    """
    result = supply_chain_service.confirm_delivery(shipment_id, delivery_data)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Delivery confirmation failed"),
        )
    return result


@router.get("/suppliers/{supplier_id}/performance")
async def get_supplier_performance(supplier_id: str):
    """
    Get performance analytics for a supplier.
    """
    result = supply_chain_service.get_supplier_performance(supplier_id)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Performance analytics failed"),
        )
    return result


@router.post("/procurement/automated")
async def automated_procurement(procurement_data: dict):
    """
    Handle automated procurement workflows.
    """
    result = supply_chain_service.automated_procurement(procurement_data)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Automated procurement failed"),
        )
    return result
