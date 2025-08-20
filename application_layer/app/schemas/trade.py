from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class OrderItem(BaseModel):
    product_id: str
    quantity: int
    unit_price: float


class OrderBase(BaseModel):
    buyer_id: str
    seller_id: str
    items: List[OrderItem]
    total_price: float
    currency: str


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: str


class OrderResponse(OrderBase):
    id: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
