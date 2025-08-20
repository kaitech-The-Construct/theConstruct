"""
Governance repository for managing proposals and voting
"""
from typing import Dict, List, Optional, Any
from uuid import UUID
import uuid
from datetime import datetime, timedelta
from .base import BaseRepository, CachedQuery
import logging

logger = logging.getLogger(__name__)

class GovernanceRepository(BaseRepository):
    """Repository for managing governance proposals and voting"""
    
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.cache_ttl = 180  # 3 minutes for governance data
    
    # Proposal management
    @CachedQuery("proposal_by_id", ttl=180)
    async def get_proposal_by_id(self, proposal_id: UUID) -> Optional[Dict[str, Any]]:
        """Get proposal by ID"""
        query = """
            SELECT p.id, p.proposal_id, p.proposer_id, p.title, p.description,
                   p.proposal_type, p.voting_start, p.voting_end, p.status,
                   p.votes_for, p.votes_against, p.total_votes, p.created_at, p.updated_at,
                   u.wallet_address as proposer_wallet,
                   u.reputation_score as proposer_reputation
            FROM governance.proposals p
            JOIN blockchain.users u ON p.proposer_id = u.id
            WHERE p.id = $1
        """
        return await self._execute_query_one(query, proposal_id)
    
    @CachedQuery("proposal_by_proposal_id", ttl=180)
    async def get_proposal_by_proposal_id(self, proposal_id: str) -> Optional[Dict[str, Any]]:
        """Get proposal by proposal_id string"""
        query = """
            SELECT p.id, p.proposal_id, p.proposer_id, p.title, p.description,
                   p.proposal_type, p.voting_start, p.voting_end, p.status,
                   p.votes_for, p.votes_against, p.total_votes, p.created_at, p.updated_at,
                   u.wallet_address as proposer_wallet,
                   u.reputation_score as proposer_reputation
            FROM governance.proposals p
            JOIN blockchain.users u ON p.proposer_id = u.id
            WHERE p.proposal_id = $1
        """
        return await self._execute_query_one(query, proposal_id)
    
    async def create_proposal(self, proposal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new governance proposal"""
        proposal_uuid = uuid.uuid4()
        query = """
            INSERT INTO governance.proposals 
            (id, proposal_id, proposer_id, title, description, proposal_type,
             voting_start, voting_end, status)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING id, proposal_id, proposer_id, title, description, proposal_type,
                      voting_start, voting_end, status, votes_for, votes_against,
                      total_votes, created_at, updated_at
        """
        
        result = await self._execute_query_one(
            query,
            proposal_uuid,
            proposal_data['proposal_id'],
            proposal_data['proposer_id'],
            proposal_data['title'],
            proposal_data['description'],
            proposal_data['proposal_type'],
            proposal_data['voting_start'],
            proposal_data['voting_end'],
            proposal_data.get('status', 'active')
        )
        
        if result:
            # Invalidate related cache entries
            await self._invalidate_cache("proposals_by_*")
            
            # Backup to Firestore
            await self._backup_to_firestore('proposals', str(proposal_uuid), result)
        
        return result
    
    async def update_proposal_status(self, proposal_id: UUID, status: str) -> Optional[Dict[str, Any]]:
        """Update proposal status"""
        query = """
            UPDATE governance.proposals 
            SET status = $1, updated_at = NOW()
            WHERE id = $2
            RETURNING id, proposal_id, proposer_id, title, description, proposal_type,
                      voting_start, voting_end, status, votes_for, votes_against,
                      total_votes, created_at, updated_at
        """
        
        result = await self._execute_query_one(query, status, proposal_id)
        
        if result:
            # Invalidate cache entries
            await self._invalidate_cache(f"proposal_by_id:*{proposal_id}*")
            await self._invalidate_cache(f"proposal_by_proposal_id:*{result['proposal_id']}*")
            await self._invalidate_cache("proposals_by_*")
            
            # Backup to Firestore
            await self._backup_to_firestore('proposals', str(proposal_id), result)
        
        return result
    
    @CachedQuery("proposals_by_status", ttl=180)
    async def get_proposals_by_status(self, status: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get proposals by status"""
        query = """
            SELECT p.id, p.proposal_id, p.title, p.proposal_type, p.voting_start,
                   p.voting_end, p.status, p.votes_for, p.votes_against, p.total_votes,
                   p.created_at,
                   u.wallet_address as proposer_wallet
            FROM governance.proposals p
            JOIN blockchain.users u ON p.proposer_id = u.id
            WHERE p.status = $1
            ORDER BY p.created_at DESC
            LIMIT $2
        """
        return await self._execute_query(query, status, limit)
    
    @CachedQuery("active_proposals", ttl=60)
    async def get_active_proposals(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get currently active proposals"""
        query = """
            SELECT p.id, p.proposal_id, p.title, p.description, p.proposal_type,
                   p.voting_start, p.voting_end, p.votes_for, p.votes_against,
                   p.total_votes, p.created_at,
                   u.wallet_address as proposer_wallet,
                   EXTRACT(EPOCH FROM (p.voting_end - NOW())) as seconds_remaining
            FROM governance.proposals p
            JOIN blockchain.users u ON p.proposer_id = u.id
            WHERE p.status = 'active' 
            AND p.voting_start <= NOW() 
            AND p.voting_end > NOW()
            ORDER BY p.voting_end ASC
            LIMIT $1
        """
        return await self._execute_query(query, limit)
    
    # Vote management
    async def cast_vote(self, vote_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cast a vote on a proposal"""
        from .base import TransactionManager
        
        vote_uuid = uuid.uuid4()
        
        async with TransactionManager(self.db_manager) as tx:
            # Insert the vote
            vote_result = await tx.fetchrow("""
                INSERT INTO governance.votes 
                (id, proposal_id, voter_id, vote_type, voting_power, transaction_hash)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id, proposal_id, voter_id, vote_type, voting_power,
                          transaction_hash, created_at
            """, 
            vote_uuid,
            vote_data['proposal_id'],
            vote_data['voter_id'],
            vote_data['vote_type'],
            vote_data.get('voting_power', 1),
            vote_data.get('transaction_hash')
            )
            
            # Update proposal vote counts
            if vote_data['vote_type'] == 'for':
                await tx.execute("""
                    UPDATE governance.proposals 
                    SET votes_for = votes_for + $1, total_votes = total_votes + $1
                    WHERE id = $2
                """, vote_data.get('voting_power', 1), vote_data['proposal_id'])
            elif vote_data['vote_type'] == 'against':
                await tx.execute("""
                    UPDATE governance.proposals 
                    SET votes_against = votes_against + $1, total_votes = total_votes + $1
                    WHERE id = $2
                """, vote_data.get('voting_power', 1), vote_data['proposal_id'])
            else:  # abstain
                await tx.execute("""
                    UPDATE governance.proposals 
                    SET total_votes = total_votes + $1
                    WHERE id = $2
                """, vote_data.get('voting_power', 1), vote_data['proposal_id'])
        
        # Invalidate cache entries
        await self._invalidate_cache("proposal_by_*")
        await self._invalidate_cache("proposals_by_*")
        await self._invalidate_cache("user_votes:*")
        
        # Backup to Firestore
        if vote_result:
            await self._backup_to_firestore('votes', str(vote_uuid), dict(vote_result))
        
        return dict(vote_result) if vote_result else {}
    
    async def get_user_votes(self, user_id: UUID, proposal_id: Optional[UUID] = None) -> List[Dict[str, Any]]:
        """Get votes cast by a user"""
        if proposal_id:
            query = """
                SELECT v.id, v.proposal_id, v.vote_type, v.voting_power, v.transaction_hash,
                       v.created_at,
                       p.title as proposal_title, p.proposal_type
                FROM governance.votes v
                JOIN governance.proposals p ON v.proposal_id = p.id
                WHERE v.voter_id = $1 AND v.proposal_id = $2
            """
            return await self._execute_query(query, user_id, proposal_id)
        else:
            query = """
                SELECT v.id, v.proposal_id, v.vote_type, v.voting_power, v.transaction_hash,
                       v.created_at,
                       p.title as proposal_title, p.proposal_type, p.status as proposal_status
                FROM governance.votes v
                JOIN governance.proposals p ON v.proposal_id = p.id
                WHERE v.voter_id = $1
                ORDER BY v.created_at DESC
            """
            return await self._execute_query(query, user_id)
    
    async def get_proposal_votes(self, proposal_id: UUID) -> List[Dict[str, Any]]:
        """Get all votes for a proposal"""
        query = """
            SELECT v.id, v.voter_id, v.vote_type, v.voting_power, v.transaction_hash,
                   v.created_at,
                   u.wallet_address as voter_wallet,
                   u.reputation_score as voter_reputation
            FROM governance.votes v
            JOIN blockchain.users u ON v.voter_id = u.id
            WHERE v.proposal_id = $1
            ORDER BY v.created_at DESC
        """
        return await self._execute_query(query, proposal_id)
    
    async def check_user_voted(self, proposal_id: UUID, user_id: UUID) -> bool:
        """Check if user has already voted on a proposal"""
        query = """
            SELECT EXISTS(
                SELECT 1 FROM governance.votes 
                WHERE proposal_id = $1 AND voter_id = $2
            )
        """
        result = await self._execute_query_one(query, proposal_id, user_id)
        return result['exists'] if result else False
    
    async def get_expired_proposals(self) -> List[Dict[str, Any]]:
        """Get proposals that have passed their voting end time"""
        query = """
            SELECT id, proposal_id, title, proposal_type, voting_end, votes_for,
                   votes_against, total_votes, status
            FROM governance.proposals 
            WHERE voting_end < NOW() AND status = 'active'
            ORDER BY voting_end ASC
        """
        return await self._execute_query(query)
    
    async def finalize_proposal(self, proposal_id: UUID) -> Optional[Dict[str, Any]]:
        """Finalize a proposal by determining the outcome"""
        # Get proposal details
        proposal = await self.get_proposal_by_id(proposal_id)
        if not proposal:
            return None
        
        # Determine outcome based on votes
        votes_for = proposal['votes_for']
        votes_against = proposal['votes_against']
        total_votes = proposal['total_votes']
        
        # Simple majority rule (can be customized based on proposal type)
        if votes_for > votes_against and total_votes >= 3:  # Minimum quorum
            final_status = 'passed'
        elif votes_against >= votes_for:
            final_status = 'rejected'
        else:
            final_status = 'failed_quorum'
        
        # Update proposal status
        result = await self.update_proposal_status(proposal_id, final_status)
        
        return result
    
    @CachedQuery("governance_analytics", ttl=600)
    async def get_governance_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get governance analytics for the specified period"""
        # Proposal statistics
        proposal_stats_query = """
            SELECT 
                COUNT(*) as total_proposals,
                COUNT(CASE WHEN status = 'passed' THEN 1 END) as passed_proposals,
                COUNT(CASE WHEN status = 'rejected' THEN 1 END) as rejected_proposals,
                COUNT(CASE WHEN status = 'active' THEN 1 END) as active_proposals,
                AVG(total_votes) as avg_votes_per_proposal
            FROM governance.proposals 
            WHERE created_at >= NOW() - INTERVAL '%s days'
        """ % days
        proposal_stats = await self._execute_query_one(proposal_stats_query)
        
        # Voting participation
        participation_query = """
            SELECT 
                COUNT(DISTINCT voter_id) as unique_voters,
                COUNT(*) as total_votes,
                COUNT(CASE WHEN vote_type = 'for' THEN 1 END) as votes_for,
                COUNT(CASE WHEN vote_type = 'against' THEN 1 END) as votes_against,
                COUNT(CASE WHEN vote_type = 'abstain' THEN 1 END) as votes_abstain
            FROM governance.votes v
            JOIN governance.proposals p ON v.proposal_id = p.id
            WHERE v.created_at >= NOW() - INTERVAL '%s days'
        """ % days
        participation_stats = await self._execute_query_one(participation_query)
        
        # Top voters
        top_voters_query = """
            SELECT 
                u.wallet_address,
                COUNT(*) as votes_cast,
                SUM(v.voting_power) as total_voting_power,
                u.reputation_score
            FROM governance.votes v
            JOIN blockchain.users u ON v.voter_id = u.id
            WHERE v.created_at >= NOW() - INTERVAL '%s days'
            GROUP BY u.id, u.wallet_address, u.reputation_score
            ORDER BY votes_cast DESC, total_voting_power DESC
            LIMIT 10
        """ % days
        top_voters = await self._execute_query(top_voters_query)
        
        # Proposal types distribution
        proposal_types_query = """
            SELECT proposal_type, COUNT(*) as count
            FROM governance.proposals 
            WHERE created_at >= NOW() - INTERVAL '%s days'
            GROUP BY proposal_type
            ORDER BY count DESC
        """ % days
        proposal_types = await self._execute_query(proposal_types_query)
        
        return {
            'proposal_statistics': proposal_stats or {},
            'participation_statistics': participation_stats or {},
            'top_voters': top_voters,
            'proposal_types': proposal_types
        }
    
    async def get_user_voting_history(self, user_id: UUID, limit: int = 50) -> Dict[str, Any]:
        """Get comprehensive voting history for a user"""
        cache_key = self._generate_cache_key("user_voting_history", user_id)
        cached_history = await self._get_from_cache(cache_key)
        
        if cached_history:
            return cached_history
        
        # Get voting statistics
        voting_stats_query = """
            SELECT 
                COUNT(*) as total_votes,
                COUNT(CASE WHEN vote_type = 'for' THEN 1 END) as votes_for,
                COUNT(CASE WHEN vote_type = 'against' THEN 1 END) as votes_against,
                COUNT(CASE WHEN vote_type = 'abstain' THEN 1 END) as votes_abstain,
                SUM(voting_power) as total_voting_power
            FROM governance.votes 
            WHERE voter_id = $1
        """
        voting_stats = await self._execute_query_one(voting_stats_query, user_id)
        
        # Get recent votes
        recent_votes = await self.get_user_votes(user_id)
        
        # Get proposals created by user
        created_proposals_query = """
            SELECT id, proposal_id, title, proposal_type, status, votes_for,
                   votes_against, total_votes, created_at
            FROM governance.proposals 
            WHERE proposer_id = $1
            ORDER BY created_at DESC
            LIMIT $2
        """
        created_proposals = await self._execute_query(created_proposals_query, user_id, limit)
        
        history = {
            'voting_statistics': voting_stats or {},
            'recent_votes': recent_votes[:limit],
            'created_proposals': created_proposals
        }
        
        # Cache the history
        await self._set_cache(cache_key, history, 300)  # 5 minutes cache
        
        return history
    
    async def get_proposals_by_type(self, proposal_type: str, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get proposals by type and optionally by status"""
        base_query = """
            SELECT p.id, p.proposal_id, p.title, p.description, p.voting_start,
                   p.voting_end, p.status, p.votes_for, p.votes_against, p.total_votes,
                   p.created_at,
                   u.wallet_address as proposer_wallet
            FROM governance.proposals p
            JOIN blockchain.users u ON p.proposer_id = u.id
            WHERE p.proposal_type = $1
        """
        
        params = [proposal_type]
        if status:
            base_query += " AND p.status = $2"
            params.append(status)
            base_query += f" ORDER BY p.created_at DESC LIMIT ${len(params) + 1}"
            params.append(limit)
        else:
            base_query += f" ORDER BY p.created_at DESC LIMIT $2"
            params.append(limit)
        
        return await self._execute_query(base_query, *params)
    
    async def get_voting_power(self, user_id: UUID) -> int:
        """Calculate voting power for a user based on reputation and stake"""
        cache_key = self._generate_cache_key("voting_power", user_id)
        cached_power = await self._get_from_cache(cache_key)
        
        if cached_power is not None:
            return cached_power
        
        # Get user reputation
        user_query = """
            SELECT reputation_score FROM blockchain.users WHERE id = $1
        """
        user_result = await self._execute_query_one(user_query, user_id)
        
        if not user_result:
            return 1  # Default voting power
        
        reputation_score = user_result['reputation_score']
        
        # Calculate voting power (can be customized)
        # Base power of 1, plus bonus based on reputation
        voting_power = 1 + max(0, (reputation_score - 50) // 10)
        
        # Cache the voting power
        await self._set_cache(cache_key, voting_power, 1800)  # 30 minutes cache
        
        return voting_power
    
    async def get_proposal_timeline(self, proposal_id: UUID) -> List[Dict[str, Any]]:
        """Get timeline of events for a proposal"""
        query = """
            SELECT 
                'proposal_created' as event_type,
                p.created_at as timestamp,
                p.proposer_id as user_id,
                u.wallet_address as user_wallet,
                NULL as vote_type
            FROM governance.proposals p
            JOIN blockchain.users u ON p.proposer_id = u.id
            WHERE p.id = $1
            
            UNION ALL
            
            SELECT 
                'vote_cast' as event_type,
                v.created_at as timestamp,
                v.voter_id as user_id,
                u.wallet_address as user_wallet,
                v.vote_type
            FROM governance.votes v
            JOIN blockchain.users u ON v.voter_id = u.id
            WHERE v.proposal_id = $1
            
            ORDER BY timestamp ASC
        """
        return await self._execute_query(query, proposal_id)
    
    async def update_proposal_vote_counts(self, proposal_id: UUID) -> Optional[Dict[str, Any]]:
        """Recalculate and update vote counts for a proposal"""
        # Get actual vote counts
        vote_counts_query = """
            SELECT 
                COUNT(CASE WHEN vote_type = 'for' THEN 1 END) as votes_for,
                COUNT(CASE WHEN vote_type = 'against' THEN 1 END) as votes_against,
                COUNT(*) as total_votes
            FROM governance.votes 
            WHERE proposal_id = $1
        """
        counts = await self._execute_query_one(vote_counts_query, proposal_id)
        
        if not counts:
            return None
        
        # Update proposal with correct counts
        update_query = """
            UPDATE governance.proposals 
            SET votes_for = $1, votes_against = $2, total_votes = $3, updated_at = NOW()
            WHERE id = $4
            RETURNING id, proposal_id, title, votes_for, votes_against, total_votes
        """
        
        result = await self._execute_query_one(
            update_query,
            counts['votes_for'],
            counts['votes_against'],
            counts['total_votes'],
            proposal_id
        )
        
        if result:
            # Invalidate cache entries
            await self._invalidate_cache(f"proposal_by_id:*{proposal_id}*")
            await self._invalidate_cache("proposals_by_*")
        
        return result
