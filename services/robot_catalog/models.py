from pydantic import BaseModel
from typing import Dict, List


class RobotDetails(BaseModel):
    """Robot details model"""
    manufacturer: str
    manufacturer_id: str
    model_id: str
    price: Dict | None = None
    description: str
    image_url: str | None = None

class PriceDetails(BaseModel):
    """Price details for model"""
    model_id: str
    subscription_price: float
    premium_price: float | None = None