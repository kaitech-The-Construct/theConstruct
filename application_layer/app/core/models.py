import datetime
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum

from utils.common import get_current_utc_time



# Define Pricing Model
class Price(BaseModel):
    """Price Model"""

    model: str
    subscription_price: float
    listing_price: float | None = None

# Specifications 
class Specification(BaseModel):
    weight: Optional[float]
    dimensions: Optional[str]
    battery_life: Optional[str]
    payload_capacity: Optional[float]
    operating_environment: Optional[str]

# Define a Robot model
class RobotModel(BaseModel):
    """Robot Model"""

    manufacturer: str
    manufacturer_id: str
    model_id: str
    price: Price
    description: str
    image_url: str | None = None
    created_at: datetime | None = get_current_utc_time
    specification: Optional[Specification]


# Define a Software model
class SoftwareModel(BaseModel):
    """Software Model"""

    name: str
    version: str
    version_id: str
    author: str
    description: str
    compatibility: List[str]
    license: str
    documentation_url: str
    image_url: str | None = None


# Define a Trade model
class TradeModel(BaseModel):
    """Trade Model"""

    __tablename__ = "trades"

    id: int
    robot_id: int
    software_id: int
    price: Price
    trade_date: datetime | None = get_current_utc_time
    status: str


# Define a User model
class UserModel(BaseModel):
    """User Model"""

    id: int
    username: str
    email: str
    full_name: str = ""
    is_active: bool
    created_at: datetime


# Define a Governance Proposal model
class ProposalModel(BaseModel):
    """Proposal Model"""

    id: int
    title: str
    description: str
    creator_id: int
    created_at: datetime
    status: str


# Define a Vote model associated with a Governance Proposal
class VoteModel(BaseModel):
    """Vote Model"""

    id: int
    proposal_id: int
    voter_id: int
    vote: str  # For instance, "For", "Against", "Abstain"
    voted_at: datetime


# Enums for predefined choices

class RobotTypeEnum(str, Enum):
    """Robot Types"""
    industrial = 'Industrial'
    service = 'Service'
    companion = 'Companion'

class ManufacturerTypeEnum(str, Enum):
    """Entity Type"""
    business = 'Business'
    individual = 'Individual'
    government = 'Government'

class DeveloperTypeEnum(str, Enum):
    """Developer Type"""
    business = 'Business'
    freelance = 'Freelance'


class ContactInformation(BaseModel):
    """Contact Info"""
    phone_number: Optional[str]
    email: str
    address: Optional[str]

class Certification(BaseModel):
    """Certifications"""
    certification_name: str
    issued_by: str
    issue_date: datetime
    expiry_date: Optional[datetime]

class TechnologyUsed(BaseModel):
    """Technologies used for development"""
    language: str
    frameworks: List[str]
    tools: List[str]

# Robot Manufacturers Model
class Manufacturer(BaseModel):
    """Manufacturer Model"""
    id: UUID = uuid4()
    name: str
    industry: str
    contact_information: ContactInformation
    robot_type: RobotTypeEnum
    manufacturer_type: ManufacturerTypeEnum

# Software Developers Model
class Developer(BaseModel):
    """Software Developer Model"""
    id: UUID = uuid4()
    name: str
    specialization: str
    years_of_experience: int
    developer_type: DeveloperTypeEnum
    certifications: List[Certification]
    contact_information: ContactInformation
    portfolio_url: Optional[HttpUrl]
    technologies_used: Optional[TechnologyUsed]

class ProductionStatusEnum(str, Enum):
    """Production Status After Purchase"""
    active = 'Active'
    completed = 'Completed'
    pending = 'Pending'

class StatusEnum(str, Enum):
    """Status Enum"""
    active = 'Active'
    completed = 'Completed'
    on_hold = 'On-Hold'