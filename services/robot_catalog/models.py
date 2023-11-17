from pydantic import BaseModel
from typing import Dict, List


class RobotDetails(BaseModel):
    """Robot API call details"""
    manufacturer_id: str
    model_id: str
    price: Dict | None = None
    description: str

class PriceDetails(BaseModel):
    """Price details for model"""
    model_id: str
    subscription_price: float
    premium_price: float | None = None