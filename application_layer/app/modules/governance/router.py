# from fastapi import APIRouter, HTTPException, status, Depends
# from typing import List
# from core.services.goverenance_service import GovernanceService
# from schemas.governance import (
#     ProposalCreate,
#     ProposalResponse,
#     VoteCreate,
#     VoteResponse,
# )

# router = APIRouter()


# # Dependency injection for governance service
# def get_governance_service():
#     return GovernanceService()


# @router.post(
#     "/proposals", response_model=ProposalResponse, status_code=status.HTTP_201_CREATED
# )
# async def create_proposal(
#     proposal: ProposalCreate,
#     service: GovernanceService = Depends(get_governance_service),
# ):
#     """
#     Submit a new governance proposal.
#     """
#     new_proposal = service.create_proposal(proposal)
#     if new_proposal is None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating proposal"
#         )
#     return new_proposal


# @router.get("/proposals", response_model=List[ProposalResponse])
# async def list_proposals(service: GovernanceService = Depends(get_governance_service)):
#     """
#     Retrieve a list of governance proposals.
#     """
#     proposals = service.get_all_proposals()
#     return proposals


# @router.post("/proposals/{proposal_id}/votes", response_model=VoteResponse)
# async def vote_on_proposal(
#     proposal_id: int,
#     vote: VoteCreate,
#     service: GovernanceService = Depends(get_governance_service),
# ):
#     """
#     Cast a vote on a governance proposal.
#     """
#     new_vote = service.vote_on_proposal(proposal_id, vote)
#     if new_vote is None:
#         raise HTTPException(
#             status_code=404, detail="Proposal not found or error casting vote"
#         )
#     return new_vote
