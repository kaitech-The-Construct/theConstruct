from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Schema for robotics design details
class RoboticsDesign(BaseModel):
    """Robotics Design Model"""

    design_id: str = Field(..., description="The identifier for the robotics design")
    designer: str = Field(..., description="The name of the designer")
    robot_model: str = Field(
        ..., description="The model of the robot that this design is for"
    )
    specifications: dict = Field(
        ..., description="The specifications of the robot design"
    )
    category: str = Field(..., description="The category of the robot design")
    date_created: datetime = Field(
        ..., description="The date on which the design was created"
    )
    url_to_images: list[str] = Field(
        ..., description="The URLs of the images of the robot design"
    )
    current_status: str = Field(
        ..., description="The current status of the robot design"
    )
    tags: list[str] = Field(..., description="The tags associated with the robot design")
    additional_info: Optional[dict] = Field(
        None, description="Additional information about the robot design"
    )

    class Config:
        """Config"""

        schema_extra = {
            "example": {
                "design_id": "1234567890",
                "designer": "John Smith",
                "robot_model": "XJ-500",
                "specifications": {
                    "weight": "100 lbs",
                    "height": "6 feet",
                    "speed": "10 mph",
                },
                "category": "Service robot",
                "date_created": "2023-03-08T12:00:00Z",
                "url_to_images": [
                    "https://example.com/image1.jpg",
                    "https://example.com/image2.jpg",
                ],
                "current_status": "In progress",
                "tags": ["autonomous", "mobile"],
                "additional_info": {
                    "notes": "This robot is designed to perform tasks in a hazardous environment.",
                    "references": ["https://example.com/reference1.pdf", "https://example.com/reference2.pdf"],
                },
            }
        }
# Schema for creating a new robotics design
class DesignCreate(BaseModel):
    """Robotics Design Create Model"""

    designer: str = Field(..., description="The name of the designer")
    robot_model: str = Field(
        ..., description="The model of the robot that this design is for"
    )
    specifications: dict = Field(
        ..., description="The specifications of the robot design"
    )
    category: str = Field(..., description="The category of the robot design")
    date_created: datetime = Field(
        ..., description="The date on which the design was created"
    )
    url_to_images: list[str] = Field(
        ..., description="The URLs of the images of the robot design"
    )
    current_status: str = Field(
        ..., description="The current status of the robot design"
    )
    tags: list[str] = Field(..., description="The tags associated with the robot design")
    additional_info: Optional[dict] = Field(
        None, description="Additional information about the robot design"
    )


# Schema for a robotics design response
class DesignResponse(BaseModel):
    """Robotics Design Response Model"""

    design_id: str = Field(..., description="The identifier for the robotics design")
    designer: str = Field(..., description="The name of the designer")
    robot_model: str = Field(
        ..., description="The model of the robot that this design is for"
    )
    specifications: dict = Field(
        ..., description="The specifications of the robot design"
    )
    category: str = Field(..., description="The category of the robot design")
    date_created: datetime = Field(
        ..., description="The date on which the design was created"
    )
    url_to_images: list[str] = Field(
        ..., description="The URLs of the images of the robot design"
    )
    current_status: str = Field(
        ..., description="The current status of the robot design"
    )
    tags: list[str] = Field(..., description="The tags associated with the robot design")
    additional_info: Optional[dict] = Field(
        None, description="Additional information about the robot design"
    )


# Schema for updating a robotics design
class DesignUpdate(BaseModel):
    """Robotics Design Update Model"""

    designer: Optional[str] = Field(None, description="The name of the designer")
    robot_model: Optional[str] = Field(
        None, description="The model of the robot that this design is for"
    )
    specifications: Optional[dict] = Field(
        None, description="The specifications of the robot design"
    )
    category: Optional[str] = Field(None, description="The category of the robot design")
    date_created: Optional[datetime] = Field(
        None, description="The date on which the design was created"
    )
    url_to_images: Optional[list[str]] = Field(
        None, description="The URLs of the images of the robot design"
    )
    current_status: Optional[str] = Field(
        None, description="The current status of the robot design"
    )
    tags: Optional[list[str]] = Field(None, description="The tags associated with the robot design")
    additional_info: Optional[dict] = Field(
        None, description="Additional information about the robot design"
    )