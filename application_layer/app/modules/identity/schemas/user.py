from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class Profile(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None


class Wallets(BaseModel):
    xrpl: Optional[str] = None
    solana: Optional[str] = None


class KYC(BaseModel):
    status: str = "pending"
    documents: Optional[List[str]] = None
    verified_at: Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    profile: Optional[Profile] = None
    wallets: Optional[Wallets] = None


class UserResponse(UserBase):
    id: str
    profile: Optional[Profile] = None
    wallets: Optional[Wallets] = None
    kyc: Optional[KYC] = None
    is_active: bool = Field(True)
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    """User Login Model"""

    username: str = Field(..., example="roboticist123")
    password: str = Field(..., min_length=8, example="securepassword123")
