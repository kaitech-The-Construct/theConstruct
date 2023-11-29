
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import UUID4, BaseModel, Field


# Schema to represent manufacturer creation requests
class ManufacturerCreate(BaseModel):
    """Create Manufacturer Model"""

    manufacturer_name: str = Field(..., example="roboticist123")
    primary_user_email: str = Field(..., example="manufacturer@example.com")
    secondary_user_email: str = Field(..., example="manufacturer@example.com")
    full_name: Optional[str] = Field(None, example="Alex Roboticist")
    password: str = Field(..., min_length=8, example="securepassword123")


# Schema for manufacturer data that is sent in response to
# API calls
class ManufacturerResponse(BaseModel):
    """Manufacturer Response Model"""

    id: int = Field(..., example=1)
    manufacturername: str
    email: str
    full_name: Optional[str]
    is_active: bool = Field(True)
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        """Config"""

        orm_mode = True  # Enable use of ORM models (if using an ORM like SQLAlchemy)


# Schema for manufacturer update requests (all fields optional for partial updates)
class ManufacturerUpdate(BaseModel):
    """Update Manufacturer Model"""

    email: Optional[str] = Field(None, example="newemail@example.com")
    full_name: Optional[str] = Field(None, example="New Name")
    # Not including a password field here for simplicity; password updates would
    # typically be handled by a separate endpoint.

    class Config:
        """Config"""

        orm_mode = True  # Enable use of ORM models (if using an ORM like SQLAlchemy)


# Enums for predefined choices
class RobotTypeEnum(str, Enum):
    industrial = 'Industrial'
    service = 'Service'
    companion = 'Companion'

class ManufacturerTypeEnum(str, Enum):
    public = 'Public'
    private = 'Private'
    government = 'Government'

# Shared submodel for contact information
class ContactInformation(BaseModel):
    phone_number: Optional[str] = Field(None, example="123-456-7890")
    email: Optional[str] = Field(None, example="contact@manufacturer.com")
    address: Optional[str] = Field(None, example="123 Robo Street, Technopolis")

# Manufacturer Model with additional metadata for documentation and validation
class Manufacturer(BaseModel):
    """Manufacturer Model"""
    
    id: UUID4 = Field(default_factory=UUID4, example="123e4567-e89b-12d3-a456-426614174000")
    name: str = Field(..., example="RoboMaker Inc.")
    industry: str = Field(..., example="Automotive")
    contact_information: ContactInformation
    robot_type: RobotTypeEnum = Field(..., example=RobotTypeEnum.industrial)
    manufacturer_type: ManufacturerTypeEnum = Field(..., example=ManufacturerTypeEnum.private)

    class Config:
        """Config"""