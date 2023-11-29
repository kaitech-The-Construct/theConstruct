from typing import List, Optional

from core.config.settings import settings
from fastapi import HTTPException, status
from google.cloud import firestore
from schemas.trade import TradeCreate, TradeResponse, TradeUpdate

# For demo purposes firestore will be used to record transactional data. For production a more suitable database will be used i.e. Cloud SQL and BigQuery

class TradeService:
    def __init__(self):
        self.db = firestore.Client()

    def create_trade(self, trade_data: TradeCreate) -> Optional[TradeResponse]:
        """Create Trade"""
        try:
            self.db.collection(f"{settings.ENVIR}_trades").add(trade_data.dict())
            return TradeResponse(**trade_data.dict())
        except Exception as exc:
            print(f"Error creating trade: {exc}")

    def get_trade_by_id(self, trade_id: str) -> Optional[TradeResponse]:
        """Retrieve Trade by ID"""
        trade_doc = (
            self.db.collection(f"{settings.ENVIR}_trades").document(trade_id).get()
        )
        if trade_doc.exists:
            trade_data = trade_doc.to_dict()
            trade_data["id"] = trade_id
            return TradeResponse(**trade_data)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trade not found"
        )

    def update_trade(
        self, trade_id: str, trade_data: TradeUpdate
    ) -> Optional[TradeResponse]:
        """Update Trade"""
        trade_ref = self.db.collection(f"{settings.ENVIR}_trades").document(trade_id)
        trade_doc = trade_ref.get()
        if trade_doc.exists:
            trade_ref.update(trade_data.dict(exclude_unset=True))
            trade_data = trade_ref.get().to_dict()
            trade_data["id"] = trade_id
            return TradeResponse(**trade_data)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trade not found"
        )

    def delete_trade(self, trade_id: str) -> bool:
        """Delete Trade"""
        trade_ref = self.db.collection(f"{settings.ENVIR}_trades").document(trade_id)
        trade_doc = trade_ref.get()
        if trade_doc.exists:
            trade_ref.delete()
            return True
        return False

    def list_all_trades(self) -> List[TradeResponse]:
        """List all Trades"""
        trade_docs = self.db.collection(f"{settings.ENVIR}_trades").stream()
        trades = [TradeResponse(**doc.to_dict()) for doc in trade_docs]
        return trades
