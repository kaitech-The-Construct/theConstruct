# # core/services/governance_service.py

# from typing import List, Optional
# from schemas.governance import (
#     ProposalCreate,
#     ProposalResponse,
#     VoteCreate,
#     VoteResponse,
# )
# from core.models import ProposalModel, VoteModel
# from core.database.database import SessionLocal
# from sqlalchemy.orm import Session


# class GovernanceService:
#     """Governance Service"""

#     def __init__(self, db: Session = SessionLocal()):
#         self.db = db

#     def create_proposal(self, proposal: ProposalCreate) -> ProposalResponse:
#         """Create Proposal"""
#         new_proposal = ProposalModel(**proposal.dict())
#         self.db.add(new_proposal)
#         self.db.commit()
#         self.db.refresh(new_proposal)
#         return ProposalResponse.from_orm(new_proposal)

#     def get_all_proposals(self) -> List[ProposalResponse]:
#         """Retrieve all proposals"""
#         proposals = self.db.query(ProposalModel).all()
#         return [ProposalResponse.from_orm(proposal) for proposal in proposals]

#     def get_proposal_by_id(self, proposal_id: int) -> Optional[ProposalResponse]:
#         """Retrieve Proposal by ID"""
#         proposal = (
#             self.db.query(ProposalModel).filter(ProposalModel.id == proposal_id).first()
#         )
#         if proposal:
#             return ProposalResponse.from_orm(proposal)
#         return None

#     def vote_on_proposal(self, proposal_id: int, vote: VoteCreate) -> VoteResponse:
#         """Vote on Proposal"""
#         proposal = (
#             self.db.query(ProposalModel).filter(ProposalModel.id == proposal_id).first()
#         )
#         if not proposal:
#             return None  # Proposal not found
#         new_vote = VoteModel(**vote.dict(), proposal_id=proposal_id)
#         self.db.add(new_vote)
#         self.db.commit()
#         self.db.refresh(new_vote)
#         return VoteResponse.from_orm(new_vote)

#     # Add service methods i.e. vote updates, deletion, etc.
