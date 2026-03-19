from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


# Schema for creating a new software listing
class SoftwareCreate(BaseModel):
    """Create Software Listing Model"""

    name: str = Field(..., description="The name of the software application")
    version: str = Field(..., description="The version identifier for the software")
    author: str = Field(
        ..., description="The author or developing entity of the software"
    )
    description: str = Field(
        ..., description="A brief description of the software's functionality"
    )
    compatibility: List[str] = Field(
        ..., description="List of compatible robot models/IDs"
    )
    license: str = Field(
        ..., description="The type of license under which the software is distributed"
    )
    documentation_url: HttpUrl = Field(
        ..., description="URL to the software's documentation"
    )
    image_url: Optional[HttpUrl] = Field(
        None, description="URL to an image representing the software"
    )

    class Config:
        schema_extra = {
            "example": {
                "name": "RoboVision AI",
                "version": "1.2.3",
                "author": "VisionTech",
                "description": "Advanced vision and pattern recognition software for robots.",
                "compatibility": ["XJ-500", "XJ-550"],
                "license": "MIT",
                "documentation_url": "https://docs.robovision.ai",
                "image_url": "https://storage.googleapis.com/app-images-the-construct-401518/software.png",
            }
        }


# Schema for software update requests (all fields optional for partial updates)
class SoftwareUpdate(BaseModel):
    """Update Software Model"""

    name: Optional[str] = Field(
        None, description="The name of the software application"
    )
    version: Optional[str] = Field(
        None, description="The version identifier for the software"
    )
    author: Optional[str] = Field(
        None, description="The author or developing entity of the software"
    )
    description: Optional[str] = Field(
        None, description="A brief description of the software's functionality"
    )
    compatibility: Optional[List[str]] = Field(
        None, description="List of compatible robot models/IDs"
    )
    license: Optional[str] = Field(
        None, description="The type of license under which the software is distributed"
    )
    documentation_url: Optional[HttpUrl] = Field(
        None, description="URL to the software's documentation"
    )
    image_url: Optional[HttpUrl] = Field(
        None, description="URL to an image representing the software"
    )

    class Config:
        """Config"""

        schema_extra = {
            "example": {
                "name": "RoboVision AI",
                "version": "1.3.0",
                "author": "VisionTech",
                "description": "Updated vision software with new pattern recognition capabilities.",
                "compatibility": ["XJ-500", "XJ-550", "XJ-600"],
                "license": "GPL-3.0",
                "documentation_url": "",
                "image_url": "https://storage.googleapis.com/app-images-the-construct-401518/software.png",
            }
        }


# Schema for software response data
class SoftwareResponse(SoftwareCreate):
    """Software Response Model"""

    name: str
    version: str
    version_id: Optional[str]
    author: str
    description: str
    compatibility: List[str]
    license: str
    documentation_url: str
    image_url: str | None = None

    class Config:
        """Config"""

        orm_mode = True  # Enable ORM compatibility
        schema_extra = {
            "example": {
                "version_id": "101",
                "name": "RoboVision AI",
                "version": "1.2.3",
                "author": "VisionTech",
                "description": "Advanced vision and pattern recognition software for robots.",
                "compatibility": ["XJ-500", "XJ-550"],
                "license": "MIT",
                "documentation_url": "https://docs.robovision.ai",
                "image_url": "https://storage.googleapis.com/app-images-the-construct-401518/software.png",
            }
        }
