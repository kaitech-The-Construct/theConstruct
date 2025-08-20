from typing import List

from core.services.trade_service import TradeService
from fastapi import APIRouter, HTTPException, status
from schemas.trade import OrderCreate, OrderResponse, OrderUpdate

router = APIRouter()
trade_service = TradeService()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    """
    Create a new order for a robotic asset.
    """
    new_order = trade_service.create_order(order)
    return new_order


@router.get("/user/{user_id}", response_model=List[OrderResponse])
async def list_orders(user_id: str):
    """
    Retrieve a list of all orders for a specific user.
    """
    orders = trade_service.get_orders_by_user(user_id)
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def retrieve_order(order_id: str):
    """
    Retrieve a specific order by its ID.
    """
    order = trade_service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(order_id: str, order: OrderUpdate):
    """
    Update a specific order.
    """
    updated_order = trade_service.update_order_status(order_id, order)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order


@router.post("/{order_id}/payment")
async def process_payment(order_id: str, payment_data: dict):
    """
    Process payment for an order.
    """
    result = trade_service.process_payment(order_id, payment_data.get("method", "direct"))
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Payment processing failed")
        )
    return result


@router.get("/{order_id}/tracking")
async def track_order(order_id: str):
    """
    Track order status and delivery information.
    """
    tracking_info = trade_service.track_order_status(order_id)
    if tracking_info.get("status") == "not_found":
        raise HTTPException(status_code=404, detail="Order not found")
    return tracking_info


@router.post("/escrow/create")
async def create_escrow(escrow_data: dict):
    """
    Create escrow for an order.
    """
    order_id = escrow_data.get("order_id")
    if not order_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order ID is required"
        )
    
    result = trade_service.manage_escrow(order_id, escrow_data)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Escrow creation failed")
        )
    return result


@router.put("/escrow/{escrow_id}/release")
async def release_escrow(escrow_id: str):
    """
    Release escrow funds.
    """
    # This would typically interact with blockchain escrow contracts
    # For now, return a placeholder response
    return {"message": "Escrow release initiated", "escrow_id": escrow_id}


@router.post("/{order_id}/dispute")
async def create_dispute(order_id: str, dispute_data: dict):
    """
    Create a dispute for an order.
    """
    result = trade_service.handle_disputes(order_id, dispute_data)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Dispute creation failed")
        )
    return result
