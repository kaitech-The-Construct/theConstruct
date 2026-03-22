from typing import List, Dict
from fastapi import APIRouter, HTTPException, status
from .services.bounty_service import BountyService
from .schemas.bounty import BountyCreate, BountyResponse, AgentSubmission, AgentAutonomousSubmission, BundleConfig

router = APIRouter()
bounty_service = BountyService()


@router.post("/", response_model=BountyResponse, status_code=status.HTTP_201_CREATED)
def create_bounty(bounty_data: BountyCreate):
    """
    Create a new bounty / feature request with an escrowed reward.
    """
    return bounty_service.create_bounty(bounty_data)


@router.get("/", response_model=List[BountyResponse])
def list_bounties():
    """
    Retrieve all open bounties in the marketplace.
    """
    return bounty_service.list_bounties()


@router.get("/{bounty_id}", response_model=BountyResponse)
def get_bounty(bounty_id: str):
    """
    Get a single bounty details by its ID.
    """
    bounty = bounty_service.get_bounty(bounty_id)
    if not bounty:
        raise HTTPException(status_code=404, detail="Bounty not found")
    return bounty


@router.post("/{bounty_id}/submit-hitl")
def submit_agent_work_hitl(bounty_id: str, submission: AgentSubmission):
    """
    Submit agent work in Human-in-the-Loop mode. 
    Triggers a Xaman push notification to the developer for signature.
    """
    return bounty_service.submit_agent_work_hitl(bounty_id, submission)


@router.post("/{bounty_id}/submit-auto")
def submit_agent_work_autonomous(bounty_id: str, submission: AgentAutonomousSubmission):
    """
    Submit agent work autonomously.
    The agent submits a pre-signed transaction blob signed by their assigned XRPL Regular Key.
    """
    return bounty_service.submit_agent_work_autonomous(bounty_id, submission)


@router.post("/{bounty_id}/verify-and-payout")
def verify_and_payout(bounty_id: str, bundle_config: BundleConfig):
    """
    Oracle endpoint to run Sandbox verification.
    If passed, executes an XLS-56 atomic batch transaction for royalty splits.
    """
    return bounty_service.verify_and_payout(bounty_id, bundle_config)
