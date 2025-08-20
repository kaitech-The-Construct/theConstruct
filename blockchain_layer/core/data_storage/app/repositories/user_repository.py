"""
User repository for managing blockchain users
"""
from typing import Dict, List, Optional, Any
from uuid import UUID
import uuid
from .base import BaseRepository, CachedQuery
import logging

logger = logging.getLogger(__name__)

class UserRepository(BaseRepository):
    """Repository for managing users in the blockchain layer"""
    
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.cache_ttl = 600  # 10 minutes for user data
    
    @CachedQuery("user_by_id", ttl=600)
    async def get_by_id(self, user_id: UUID) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        query = """
            SELECT id, wallet_address, wallet_type, public_key, reputation_score,
                   created_at, updated_at, is_active, metadata
            FROM blockchain.users 
            WHERE id = $1 AND is_active = true
        """
        return await self._execute_query_one(query, user_id)
    
    @CachedQuery("user_by_wallet", ttl=600)
    async def get_by_wallet_address(self, wallet_address: str) -> Optional[Dict[str, Any]]:
        """Get user by wallet address"""
        query = """
            SELECT id, wallet_address, wallet_type, public_key, reputation_score,
                   created_at, updated_at, is_active, metadata
            FROM blockchain.users 
            WHERE wallet_address = $1 AND is_active = true
        """
        return await self._execute_query_one(query, wallet_address)
    
    async def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        user_id = uuid.uuid4()
        query = """
            INSERT INTO blockchain.users 
            (id, wallet_address, wallet_type, public_key, reputation_score, metadata)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id, wallet_address, wallet_type, public_key, reputation_score,
                      created_at, updated_at, is_active, metadata
        """
        
        result = await self._execute_query_one(
            query,
            user_id,
            user_data['wallet_address'],
            user_data.get('wallet_type', 'xrpl'),
            user_data.get('public_key'),
            user_data.get('reputation_score', 0),
            user_data.get('metadata', {})
        )
        
        if result:
            # Invalidate related cache entries
            await self._invalidate_cache(f"user_by_wallet:*{user_data['wallet_address']}*")
            
            # Backup to Firestore
            await self._backup_to_firestore('users', str(user_id), result)
        
        return result
    
    async def update(self, user_id: UUID, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user data"""
        # Build dynamic update query
        set_clauses = []
        values = []
        param_count = 1
        
        for field, value in update_data.items():
            if field in ['wallet_type', 'public_key', 'reputation_score', 'metadata']:
                set_clauses.append(f"{field} = ${param_count}")
                values.append(value)
                param_count += 1
        
        if not set_clauses:
            return await self.get_by_id(user_id)
        
        values.append(user_id)
        query = f"""
            UPDATE blockchain.users 
            SET {', '.join(set_clauses)}, updated_at = NOW()
            WHERE id = ${param_count} AND is_active = true
            RETURNING id, wallet_address, wallet_type, public_key, reputation_score,
                      created_at, updated_at, is_active, metadata
        """
        
        result = await self._execute_query_one(query, *values)
        
        if result:
            # Invalidate cache entries
            await self._invalidate_cache(f"user_by_id:*{user_id}*")
            await self._invalidate_cache(f"user_by_wallet:*{result['wallet_address']}*")
            
            # Backup to Firestore
            await self._backup_to_firestore('users', str(user_id), result)
        
        return result
    
    async def update_reputation(self, user_id: UUID, reputation_delta: int) -> Optional[Dict[str, Any]]:
        """Update user reputation score"""
        query = """
            UPDATE blockchain.users 
            SET reputation_score = GREATEST(0, reputation_score + $1), updated_at = NOW()
            WHERE id = $2 AND is_active = true
            RETURNING id, wallet_address, wallet_type, public_key, reputation_score,
                      created_at, updated_at, is_active, metadata
        """
        
        result = await self._execute_query_one(query, reputation_delta, user_id)
        
        if result:
            # Invalidate cache entries
            await self._invalidate_cache(f"user_by_id:*{user_id}*")
            await self._invalidate_cache(f"user_by_wallet:*{result['wallet_address']}*")
            
            # Backup to Firestore
            await self._backup_to_firestore('users', str(user_id), result)
        
        return result
    
    async def deactivate(self, user_id: UUID) -> bool:
        """Soft delete user by setting is_active to false"""
        query = """
            UPDATE blockchain.users 
            SET is_active = false, updated_at = NOW()
            WHERE id = $1
        """
        
        result = await self._execute_command(query, user_id)
        
        if result:
            # Invalidate cache entries
            await self._invalidate_cache(f"user_by_id:*{user_id}*")
            await self._invalidate_cache(f"user_by_wallet:*")
        
        return "UPDATE 1" in result
    
    @CachedQuery("users_by_reputation", ttl=300)
    async def get_top_users_by_reputation(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top users by reputation score"""
        query = """
            SELECT id, wallet_address, wallet_type, reputation_score, metadata
            FROM blockchain.users 
            WHERE is_active = true
            ORDER BY reputation_score DESC
            LIMIT $1
        """
        return await self._execute_query(query, limit)
    
    @CachedQuery("users_by_type", ttl=300)
    async def get_users_by_wallet_type(self, wallet_type: str) -> List[Dict[str, Any]]:
        """Get users by wallet type"""
        query = """
            SELECT id, wallet_address, wallet_type, reputation_score, metadata
            FROM blockchain.users 
            WHERE wallet_type = $1 AND is_active = true
            ORDER BY reputation_score DESC
        """
        return await self._execute_query(query, wallet_type)
    
    async def search_users(self, search_term: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search users by wallet address or metadata"""
        query = """
            SELECT id, wallet_address, wallet_type, reputation_score, metadata
            FROM blockchain.users 
            WHERE is_active = true 
            AND (
                wallet_address ILIKE $1 
                OR metadata::text ILIKE $1
            )
            ORDER BY reputation_score DESC
            LIMIT $2
        """
        search_pattern = f"%{search_term}%"
        return await self._execute_query(query, search_pattern, limit)
    
    async def get_user_stats(self, user_id: UUID) -> Dict[str, Any]:
        """Get comprehensive user statistics"""
        cache_key = self._generate_cache_key("user_stats", user_id)
        cached_stats = await self._get_from_cache(cache_key)
        
        if cached_stats:
            return cached_stats
        
        # Get user basic info
        user = await self.get_by_id(user_id)
        if not user:
            return {}
        
        # Get trading statistics
        trading_stats_query = """
            SELECT 
                COUNT(*) as total_orders,
                COUNT(CASE WHEN status = 'filled' THEN 1 END) as filled_orders,
                SUM(CASE WHEN order_type = 'buy' THEN amount ELSE 0 END) as total_bought,
                SUM(CASE WHEN order_type = 'sell' THEN amount ELSE 0 END) as total_sold
            FROM trading.orders 
            WHERE user_id = $1
        """
        trading_stats = await self._execute_query_one(trading_stats_query, user_id)
        
        # Get manufacturing statistics
        manufacturing_stats_query = """
            SELECT 
                COUNT(CASE WHEN customer_id = $1 THEN 1 END) as orders_placed,
                COUNT(CASE WHEN manufacturer_id = $1 THEN 1 END) as orders_fulfilled,
                COUNT(CASE WHEN customer_id = $1 AND status = 'completed' THEN 1 END) as completed_orders
            FROM manufacturing.orders 
            WHERE customer_id = $1 OR manufacturer_id = $1
        """
        manufacturing_stats = await self._execute_query_one(manufacturing_stats_query, user_id)
        
        # Get governance participation
        governance_stats_query = """
            SELECT 
                COUNT(DISTINCT proposal_id) as votes_cast,
                COUNT(CASE WHEN vote_type = 'for' THEN 1 END) as votes_for,
                COUNT(CASE WHEN vote_type = 'against' THEN 1 END) as votes_against
            FROM governance.votes 
            WHERE voter_id = $1
        """
        governance_stats = await self._execute_query_one(governance_stats_query, user_id)
        
        stats = {
            'user': user,
            'trading': trading_stats or {},
            'manufacturing': manufacturing_stats or {},
            'governance': governance_stats or {}
        }
        
        # Cache the stats
        await self._set_cache(cache_key, stats, 300)  # 5 minutes cache
        
        return stats
