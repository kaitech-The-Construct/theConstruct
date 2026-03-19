from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List


class ProposalCreate(BaseModel):
    """Create Proposal Model"""

    title: str = Field(..., description="The title of the governance proposal")
    description: Optional[str] = Field(
        None, description="A detailed description of the governance proposal"
    )
    creator_id: int = Field(..., description="The ID of the user creating the proposal")

    class Config:
        schema_extra = {
            "example": {
                "title": "Upgrade DEX Protocol",
                "description": "A proposal to upgrade the underlying DEX protocol to version 2.0",
                "creator_id": 123,
            }
        }


class ProposalResponse(BaseModel):
    """Proposal Response Model"""

    id: int = Field(..., description="The unique ID of the governance proposal")
    title: str
    description: Optional[str]
    creator_id: int
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp when the proposal was created",
    )
    status: str = Field(..., description="Current status of the proposal")

    class Config:
        """Config"""

        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Upgrade DEX Protocol",
                "description": "A proposal to upgrade the underlying DEX protocol to version 2.0",
                "creator_id": 123,
                "created_at": datetime.now(),
                "status": "Voting",
            }
        }


class VoteCreate(BaseModel):
    """Create Vote Model"""

    proposal_id: int = Field(..., description="The ID of the proposal being voted on")
    voter_id: int = Field(..., description="The ID of the user casting the vote")
    vote: str = Field(
        ..., description="The user's vote ('For', 'Against', or 'Abstain')"
    )

    @validator("vote")
    def validate_vote(cls, v):
        """Validate vote"""
        if v not in ("For", "Against", "Abstain"):
            raise ValueError('Vote must be "For", "Against", or "Abstain"')
        return v

    class Config:
        """Config"""

        schema_extra = {"example": {"proposal_id": 1, "voter_id": 456, "vote": "For"}}


class VoteResponse(BaseModel):
    """Vote Response"""

    id: int = Field(..., description="The unique ID of the vote")
    proposal_id: int
    voter_id: int
    vote: str
    voted_at: datetime = Field(
        default_factory=datetime.now, description="Timestamp when the vote was cast"
    )

    class Config:
        """Config"""

        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "proposal_id": 1,
                "voter_id": 456,
                "vote": "For",
                "voted_at": datetime.now(),
            }
        }
