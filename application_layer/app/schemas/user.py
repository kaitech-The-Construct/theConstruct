from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Schema to represent user creation requests
class UserCreate(BaseModel):
    """Create User Model"""

    username: str = Field(..., example="roboticist123")
    email: str = Field(..., example="user@example.com")
    full_name: Optional[str] = Field(None, example="Alex Roboticist")
    password: str = Field(..., min_length=8, example="securepassword123")


# Schema for user data that is sent in response to
# API calls (excluding sensitive info like passwords)
class UserResponse(BaseModel):
    """User Response Model"""

    id: int = Field(..., example=1)
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool = Field(True)
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        """Config"""

        orm_mode = True  


# Schema for user update requests (all fields optional for partial updates)
class UserUpdate(BaseModel):
    """Update User Model"""

    email: Optional[str] = Field(None, example="newemail@example.com")
    full_name: Optional[str] = Field(None, example="New Name")
    # Not including a password field here for simplicity; password updates would
    # typically be handled by a separate endpoint.

    class Config:
        """Config"""

        orm_mode = True  


# Schema for user authentication - used for login operations.
class UserLogin(BaseModel):
    """User Login Model"""

    username: str = Field(..., example="roboticist123")
    password: str = Field(..., min_length=8, example="securepassword123")
