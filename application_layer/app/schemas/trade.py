from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Schema to represent trade creation request by a user
class TradeCreate(BaseModel):
    robot_id: str = Field(..., description="The ID of the robot asset being traded")
    software_id: str = Field(
        ..., description="The ID of the software asset being traded"
    )
    user_id: str = Field(..., description="The ID of the user creating the trade")
    price: float = Field(
        ..., description="The agreed price of the trade in CONSTRUCT tokens"
    )
    # Include any additional fields for trade agreements, terms, etc.

    class Config:
        schema_extra = {
            "example": {
                "robot_id": "12987",
                "software_id": "101356",
                "user_id": "100154678",
                "price": 150.00,
            }
        }


# Schema for trade update requests
class TradeUpdate(BaseModel):
    price: Optional[float] = Field(
        None, description="The updated price of the trade in CONSTRUCT tokens"
    )
    # Include other fields that can be updated, if any

    class Config:
        schema_extra = {"example": {"price": 155.00}}


# Schema for responding with trade data
class TradeResponse(BaseModel):
    robot_id: str
    software_id: str
    user_id: str
    price: float
    trade_date: Optional[datetime] = Field(
        default_factory=datetime.now, description="The date and time of the trade"
    )
    status: str = Field(
        default="Pending", description="The current status of the trade"
    )

    class Config:
        orm_mode = True  # Enable ORM compatibility
        schema_extra = {
            "example": {
                "robot_id": 1,
                "software_id": 101,
                "user_id": 1001,
                "price": 150.00,
                "trade_date": "2023-01-01T10:00:00Z",
                "status": "Completed",
            }
        }
