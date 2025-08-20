"""
Asset repository for managing tokenized components
"""
from typing import Dict, List, Optional, Any
from uuid import UUID
import uuid
from .base import BaseRepository, CachedQuery
import logging

logger = logging.getLogger(__name__)

class AssetRepository(BaseRepository):
    """Repository for managing tokenized assets in the blockchain layer"""
    
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.cache_ttl = 300  # 5 minutes for asset data
    
    @CachedQuery("asset_by_id", ttl=300)
    async def get_by_id(self, asset_id: UUID) -> Optional[Dict[str, Any]]:
        """Get asset by ID"""
        query = """
            SELECT id, asset_id, asset_name, asset_description, asset_type, token_count,
                   issuer_address, transaction_hash, metadata, specifications, 
                   manufacturer_info, created_at, updated_at, status
            FROM blockchain.assets 
            WHERE id = $1
        """
        return await self._execute_query_one(query, asset_id)
    
    @CachedQuery("asset_by_asset_id", ttl=300)
    async def get_by_asset_id(self, asset_id: str) -> Optional[Dict[str, Any]]:
        """Get asset by asset_id string"""
        query = """
            SELECT id, asset_id, asset_name, asset_description, asset_type, token_count,
                   issuer_address, transaction_hash, metadata, specifications, 
                   manufacturer_info, created_at, updated_at, status
            FROM blockchain.assets 
            WHERE asset_id = $1
        """
        return await self._execute_query_one(query, asset_id)
    
    async def create(self, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new tokenized asset"""
        asset_uuid = uuid.uuid4()
        query = """
            INSERT INTO blockchain.assets 
            (id, asset_id, asset_name, asset_description, asset_type, token_count,
             issuer_address, transaction_hash, metadata, specifications, manufacturer_info, status)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            RETURNING id, asset_id, asset_name, asset_description, asset_type, token_count,
                      issuer_address, transaction_hash, metadata, specifications, 
                      manufacturer_info, created_at, updated_at, status
        """
        
        result = await self._execute_query_one(
            query,
            asset_uuid,
            asset_data['asset_id'],
            asset_data['asset_name'],
            asset_data.get('asset_description', ''),
            asset_data['asset_type'],
            asset_data['token_count'],
            asset_data['issuer_address'],
            asset_data.get('transaction_hash'),
            asset_data.get('metadata', {}),
            asset_data.get('specifications', {}),
            asset_data.get('manufacturer_info', {}),
            asset_data.get('status', 'pending')
        )
        
        if result:
            # Invalidate related cache entries
            await self._invalidate_cache(f"asset_by_asset_id:*{asset_data['asset_id']}*")
            await self._invalidate_cache("assets_by_*")
            
            # Backup to Firestore
            await self._backup_to_firestore('assets', str(asset_uuid), result)
        
        return result
    
    async def update(self, asset_id: UUID, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update asset data"""
        # Build dynamic update query
        set_clauses = []
        values = []
        param_count = 1
        
        allowed_fields = [
            'asset_name', 'asset_description', 'token_count', 'transaction_hash',
            'metadata', 'specifications', 'manufacturer_info', 'status'
        ]
        
        for field, value in update_data.items():
            if field in allowed_fields:
                set_clauses.append(f"{field} = ${param_count}")
                values.append(value)
                param_count += 1
        
        if not set_clauses:
            return await self.get_by_id(asset_id)
        
        values.append(asset_id)
        query = f"""
            UPDATE blockchain.assets 
            SET {', '.join(set_clauses)}, updated_at = NOW()
            WHERE id = ${param_count}
            RETURNING id, asset_id, asset_name, asset_description, asset_type, token_count,
                      issuer_address, transaction_hash, metadata, specifications, 
                      manufacturer_info, created_at, updated_at, status
        """
        
        result = await self._execute_query_one(query, *values)
        
        if result:
            # Invalidate cache entries
            await self._invalidate_cache(f"asset_by_id:*{asset_id}*")
            await self._invalidate_cache(f"asset_by_asset_id:*{result['asset_id']}*")
            await self._invalidate_cache("assets_by_*")
            
            # Backup to Firestore
            await self._backup_to_firestore('assets', str(asset_id), result)
        
        return result
    
    @CachedQuery("assets_by_type", ttl=300)
    async def get_by_type(self, asset_type: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get assets by type"""
        query = """
            SELECT id, asset_id, asset_name, asset_description, asset_type, token_count,
                   issuer_address, metadata, specifications, manufacturer_info, 
                   created_at, status
            FROM blockchain.assets 
            WHERE asset_type = $1 AND status = 'active'
            ORDER BY created_at DESC
            LIMIT $2
        """
        return await self._execute_query(query, asset_type, limit)
    
    @CachedQuery("assets_by_issuer", ttl=300)
    async def get_by_issuer(self, issuer_address: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get assets by issuer address"""
        query = """
            SELECT id, asset_id, asset_name, asset_description, asset_type, token_count,
                   issuer_address, metadata, specifications, manufacturer_info, 
                   created_at, status
            FROM blockchain.assets 
            WHERE issuer_address = $1
            ORDER BY created_at DESC
            LIMIT $2
        """
        return await self._execute_query(query, issuer_address, limit)
    
    async def search_assets(self, search_term: str, asset_type: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Search assets by name, description, or specifications"""
        base_query = """
            SELECT id, asset_id, asset_name, asset_description, asset_type, token_count,
                   issuer_address, metadata, specifications, manufacturer_info, 
                   created_at, status
            FROM blockchain.assets 
            WHERE status = 'active'
            AND (
                asset_name ILIKE $1 
                OR asset_description ILIKE $1
                OR specifications::text ILIKE $1
                OR metadata::text ILIKE $1
            )
        """
        
        search_pattern = f"%{search_term}%"
        params = [search_pattern]
        
        if asset_type:
            base_query += " AND asset_type = $2"
            params.append(asset_type)
            base_query += f" ORDER BY created_at DESC LIMIT ${len(params) + 1}"
            params.append(limit)
        else:
            base_query += f" ORDER BY created_at DESC LIMIT $2"
            params.append(limit)
        
        return await self._execute_query(base_query, *params)
    
    @CachedQuery("asset_categories", ttl=600)
    async def get_asset_categories(self) -> List[Dict[str, Any]]:
        """Get all asset categories with counts"""
        query = """
            SELECT asset_type, COUNT(*) as count, 
                   AVG(token_count) as avg_token_count
            FROM blockchain.assets 
            WHERE status = 'active'
            GROUP BY asset_type
            ORDER BY count DESC
        """
        return await self._execute_query(query)
    
    async def get_asset_trading_stats(self, asset_id: UUID) -> Dict[str, Any]:
        """Get trading statistics for an asset"""
        cache_key = self._generate_cache_key("asset_trading_stats", asset_id)
        cached_stats = await self._get_from_cache(cache_key)
        
        if cached_stats:
            return cached_stats
        
        # Get asset info
        asset = await self.get_by_id(asset_id)
        if not asset:
            return {}
        
        # Get trading statistics
        trading_stats_query = """
            SELECT 
                COUNT(*) as total_orders,
                COUNT(CASE WHEN status = 'filled' THEN 1 END) as filled_orders,
                COUNT(CASE WHEN status = 'active' THEN 1 END) as active_orders,
                SUM(CASE WHEN order_type = 'buy' AND status = 'filled' THEN amount ELSE 0 END) as total_bought,
                SUM(CASE WHEN order_type = 'sell' AND status = 'filled' THEN amount ELSE 0 END) as total_sold,
                AVG(CASE WHEN status = 'filled' THEN price ELSE NULL END) as avg_price,
                MAX(CASE WHEN status = 'filled' THEN price ELSE NULL END) as max_price,
                MIN(CASE WHEN status = 'filled' THEN price ELSE NULL END) as min_price
            FROM trading.orders 
            WHERE asset_id = $1
        """
        trading_stats = await self._execute_query_one(trading_stats_query, asset_id)
        
        # Get recent price history
        price_history_query = """
            SELECT price, created_at
            FROM trading.orders 
            WHERE asset_id = $1 AND status = 'filled'
            ORDER BY created_at DESC
            LIMIT 10
        """
        price_history = await self._execute_query(price_history_query, asset_id)
        
        stats = {
            'asset': asset,
            'trading': trading_stats or {},
            'price_history': price_history
        }
        
        # Cache the stats
        await self._set_cache(cache_key, stats, 180)  # 3 minutes cache
        
        return stats
    
    async def get_assets_by_specifications(self, spec_filters: Dict[str, Any], limit: int = 20) -> List[Dict[str, Any]]:
        """Get assets matching specific specifications"""
        # Build dynamic query based on specification filters
        where_clauses = ["status = 'active'"]
        values = []
        param_count = 1
        
        for spec_key, spec_value in spec_filters.items():
            where_clauses.append(f"specifications->>'{spec_key}' = ${param_count}")
            values.append(str(spec_value))
            param_count += 1
        
        values.append(limit)
        query = f"""
            SELECT id, asset_id, asset_name, asset_description, asset_type, token_count,
                   issuer_address, metadata, specifications, manufacturer_info, 
                   created_at, status
            FROM blockchain.assets 
            WHERE {' AND '.join(where_clauses)}
            ORDER BY created_at DESC
            LIMIT ${param_count}
        """
        
        return await self._execute_query(query, *values)
    
    async def update_token_count(self, asset_id: UUID, new_count: int) -> Optional[Dict[str, Any]]:
        """Update token count for an asset"""
        query = """
            UPDATE blockchain.assets 
            SET token_count = $1, updated_at = NOW()
            WHERE id = $2
            RETURNING id, asset_id, asset_name, token_count, status
        """
        
        result = await self._execute_query_one(query, new_count, asset_id)
        
        if result:
            # Invalidate cache entries
            await self._invalidate_cache(f"asset_by_id:*{asset_id}*")
            await self._invalidate_cache(f"asset_by_asset_id:*{result['asset_id']}*")
            
            # Backup to Firestore
            await self._backup_to_firestore('assets', str(asset_id), result)
        
        return result
