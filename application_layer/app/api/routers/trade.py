from typing import List

from core.services.trade_service import TradeService
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.trade import TradeCreate, TradeResponse, TradeUpdate

router = APIRouter()

trade_service = TradeService()


@router.post("/", response_model=TradeResponse)
async def create_trade(trade: TradeCreate):
    """
    Create a new trade record for a robotic asset.
    """
    new_trade = trade_service.create_trade(trade)
    return new_trade


@router.get("/", response_model=List[TradeResponse])
async def list_trades(service: TradeService = Depends()):
    """
    Retrieve a list of all trade records.
    """
    trades = trade_service.list_all_trades()
    return trades


@router.get("/{trade_id}", response_model=TradeResponse)
async def retrieve_trade(trade_id: str):
    """
    Retrieve a specific trade record by its ID.
    """
    trade = trade_service.get_trade_by_id(trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade


@router.put("/{trade_id}", response_model=TradeResponse)
async def update_trade(trade_id: str, trade: TradeUpdate):
    """
    Update a specific trade record.
    """
    updated_trade = trade_service.update_trade(trade_id, trade)
    if not updated_trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return updated_trade


@router.delete("/{trade_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trade(trade_id: str):
    """
    Delete a specific trade record by its ID.
    """
    deleted = trade_service.delete_trade(trade_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Trade not found")
    return {"ok": True}
