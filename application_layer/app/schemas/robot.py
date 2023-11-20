from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Schema for robot price details
class RobotPrice(BaseModel):
    """Price Details Model"""

    model_id: str = Field(..., description="The unique identifier for the robot model")
    subscription_price: float = Field(
        ..., description="The subscription price for the robot"
    )
    premium_price: float = Field(..., description="The premium price for the robot")

    class Config:
        schema_extra = {
            "example": {
                "model_id": "XJ-500-ID",
                "subscription_price": 49.99,
                "premium_price": 59.99,
            }
        }


# Schema for robot creation requests
class RobotCreate(BaseModel):
    """Create Robot Listing Model"""

    name: str = Field(..., description="The name of the robot model")
    manufacturer: str = Field(..., description="The name of the robot's manufacturer")
    description: Optional[str] = Field(
        None, description="A brief description of the robot"
    )
    price: RobotPrice = Field(..., description="The pricing details of the robot body")
    image_url: Optional[str] = Field(..., description="The image url of the robot body")

    class Config:
        """Config"""

        schema_extra = {
            "example": {
                "name": "XJ-500",
                "manufacturer": "RoboCorp",
                "description": "A versatile and adaptive service robot.",
                "price": {
                    "model_id": "XJ-500-ID",
                    "subscription_price": 49.99,
                    "premium_price": 59.99,
                },
            }
        }


# Schema for robot response data
class RobotResponse(BaseModel):
    """Robot Response Model"""

    id: int
    name: str
    manufacturer: str
    description: Optional[str]
    price: RobotPrice
    created_at: datetime
    image_url: str

    class Config:
        """Config"""

        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "XJ-500",
                "manufacturer": "RoboCorp",
                "description": "A versatile and adaptive service robot.",
                "price": {
                    "model_id": "XJ-500-ID",
                    "subscription_price": 49.99,
                    "premium_price": 59.99,
                },
                "created_at": "2023-04-12T10:00:00Z",
                "image_url":"https://storage.googleapis.com/app-images-the-construct-401518/cook.png"
            }
        }
