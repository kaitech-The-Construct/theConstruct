from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime


class AgentContribution(BaseModel):
    developer_wallet: str
    agent_id: str
    contribution_percentage: float
    description: str


class BundleConfig(BaseModel):
    hardware_id: str
    software_ids: List[str]
    royalties: Dict[str, float]  # wallet -> percentage (e.g., {"rManufacturer...": 60.0, "rCreator...": 10.0})


class BountyCreate(BaseModel):
    hardware_id: str
    title: str
    description: str
    requirements: List[str]
    reward_amount: float
    reward_currency: str = "XRP"
    creator_wallet: str


class AgentSubmission(BaseModel):
    agent_id: str
    developer_wallet: str
    code_hash: str
    submission_details: str
    test_results: Dict[str, bool]


class AgentAutonomousSubmission(AgentSubmission):
    signed_tx_blob: str  # Pre-signed transaction using the Regular Key


class BountyResponse(BountyCreate):
    id: str
    status: str = "open"  # open, in_progress, verification, completed
    submissions: List[AgentSubmission] = []
    created_at: datetime

    class Config:
        orm_mode = True
