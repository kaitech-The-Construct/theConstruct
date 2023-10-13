from pydantic import BaseModel
from typing import Dict, List

class PaymentModel(BaseModel):
    invoiceId: str
    serviceId: str
    userId = str
    amount: str
    expirationDate: str | None = None
    status: str | None = None

