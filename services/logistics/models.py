from pydantic import BaseModel
from typing import Dict, List

class ServiceDetails(BaseModel):
    serviceId: str
    category = str
    description: str
    name: str
    type: str
    price: Dict | None = None
    providerId: str | None = None
    reviewsId: str | None = None
