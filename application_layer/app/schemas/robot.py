from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Schema for robot price details
class RobotPrice(BaseModel):
    """Price Details Model"""

    model: str = Field(..., description="The identifier for the robot model")
    subscription_price: float = Field(
        ..., description="The subscription price for the robot"
    )
    listing_price: float = Field(..., description="The listing price for the robot")

    class Config:
        schema_extra = {
            "example": {
                "model": "XJ-500-ID",
                "subscription_price": 49.99,
                "listing_price": 59.99,
            }
        }


# Schema for robot creation requests
class RobotCreate(BaseModel):
    """Create Robot Listing Model"""

    manufacturer: str = Field(..., description="The name of the robot's manufacturer")
    manufacturer_id: str = Field(..., description="The ID of the robot's manufacturer")
    model: str = Field(..., description="The robot's model. Provided by manufacture")
    model_id: Optional[str] = Field(None, description="Generated model ID on create.")
    description: Optional[str] = Field(
        None, description="A brief description of the robot"
    )
    price: RobotPrice = Field(..., description="The pricing details of the robot body")
    image_url: Optional[str] = Field(..., description="The image url of the robot body")

    class Config:
        """Config"""

        schema_extra = {
            "example": {
                "manufacturer": "RoboCorp",
                "manufacturer_id": "TC8993",
                "model": "XJ-500",
                "model_id": "",
                "description": "A versatile and adaptive service robot.",
                "price": {
                    "model_id": "XJ-500-ID",
                    "subscription_price": 49.99,
                    "listing_price": 59.99,
                },
                "image_url": "",
            }
        }


# Schema for robot update requests
class RobotUpdate(BaseModel):
    """Update Robot Listing Model"""

    model: Optional[str] = Field(None, description="The updated model of the robot")
    manufacturer: Optional[str] = Field(
        None, description="The updated name of the robot's manufacturer"
    )
    description: Optional[str] = Field(
        None, description="The updated brief description of the robot"
    )
    price: Optional[RobotPrice] = Field(
        None, description="The updated pricing details of the robot body"
    )
    image_url: Optional[str] = Field(
        None, description="The updated image URL of the robot body"
    )

    class Config:
        """Config"""

        schema_extra = {
            "example": {
                "model": "XJ-550",
                "manufacturer": "RoboCorp Updated",
                "description": "An enhanced and improved service robot.",
                "price": {
                    "model_id": "XJ-550-ID",
                    "subscription_price": 59.99,
                    "listing_price": 69.99,
                },
                "image_url": "https://example.com/updated-robot-image.jpg",
            }
        }


# Schema for robot response data
class RobotResponse(BaseModel):
    """Robot Response Model"""

    model: str
    model_id: Optional[str]
    manufacturer: str
    manufacturer_id: str
    description: Optional[str]
    price: RobotPrice
    image_url: str

    class Config:
        """Config"""

        orm_mode = True
        schema_extra = {
            "example": {
                "model": "XJ-500",
                "model_id": "1234567",
                "manufacturer": "RoboCorp",
                "manufacturer_id": "TC8993",
                "description": "A versatile and adaptive service robot.",
                "price": {
                    "model_id": "XJ-500-ID",
                    "subscription_price": 49.99,
                    "listing_price": 599.99,
                },
                "image_url": "https://storage.googleapis.com/app-images-the-construct-401518/cook.png",
            }
        }
