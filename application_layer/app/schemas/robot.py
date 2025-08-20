from typing import List, Optional

from pydantic import BaseModel, Field


class Specifications(BaseModel):
    technical: dict
    compatibility: List[str]
    dimensions: dict


class Media(BaseModel):
    images: List[str]
    videos: List[str]
    documents: List[str]


class Ratings(BaseModel):
    average: float
    count: int


class RobotPrice(BaseModel):
    """Price Details Model"""

    model: str = Field(..., description="The identifier for the robot model")
    subscription_price: float = Field(
        ..., description="The subscription price for the robot"
    )
    listing_price: float = Field(..., description="The listing price for the robot")


class RobotCreate(BaseModel):
    """Create Robot Listing Model"""

    manufacturer: str = Field(..., description="The name of the robot's manufacturer")
    manufacturer_id: str = Field(..., description="The ID of the robot's manufacturer")
    model: str = Field(..., description="The robot's model. Provided by manufacture")
    description: Optional[str] = Field(
        None, description="A brief description of the robot"
    )
    specifications: Specifications
    media: Media
    price: RobotPrice = Field(..., description="The pricing details of the robot body")


class RobotUpdate(BaseModel):
    """Update Robot Listing Model"""

    model: Optional[str] = Field(None, description="The updated model of the robot")
    manufacturer: Optional[str] = Field(
        None, description="The updated name of the robot's manufacturer"
    )
    description: Optional[str] = Field(
        None, description="The updated brief description of the robot"
    )
    specifications: Optional[Specifications] = None
    media: Optional[Media] = None
    price: Optional[RobotPrice] = Field(
        None, description="The updated pricing details of the robot body"
    )


class RobotResponse(BaseModel):
    """Robot Response Model"""

    id: str
    model: str
    manufacturer: str
    manufacturer_id: str
    description: Optional[str]
    specifications: Specifications
    media: Media
    ratings: Ratings
    price: RobotPrice

    class Config:
        """Config"""

        orm_mode = True
