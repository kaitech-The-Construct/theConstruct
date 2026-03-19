"""
Blockchain repository for managing transactions and price feeds
"""
from typing import Dict, List, Optional, Any
from uuid import UUID
import uuid
from datetime import datetime, timedelta
from .base import BaseRepository, CachedQuery
import logging

logger = logging.getLogger(__name__)

class BlockchainRepository(BaseRepository):
    """Repository for managing blockchain transactions and price feeds"""
    
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.cache_ttl = 60  # 1 minute for blockchain data
    
    # Transaction management
    @CachedQuery("transaction_by_hash", ttl=300)
    async def get_transaction_by_hash(self, transaction_hash: str) -> Optional[Dict[str, Any]]:
        """Get transaction by hash"""
        query = """
            SELECT id, transaction_hash, transaction_type, from_address, to_address,
                   amount, fee, status, block_number, block_hash, gas_used,
                   metadata, created_at, confirmed_at
            FROM blockchain.transactions 
            WHERE transaction_hash = $1
        """
        return await self._execute_query_one(query, transaction_hash)
    
    async def create_transaction(self, tx_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new transaction record"""
        tx_uuid = uuid.uuid4()
        query = """
            INSERT INTO blockchain.transactions 
            (id, transaction_hash, transaction_type, from_address, to_address,
             amount, fee, status, block_number, block_hash, gas_used, metadata)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            RETURNING id, transaction_hash, transaction_type, from_address, to_address,
                      amount, fee, status, block_number, block_hash, gas_used,
                      metadata, created_at, confirmed_at
        """
        
        result = await self._execute_query_one(
            query,
            tx_uuid,
            tx_data['transaction_hash'],
            tx_data['transaction_type'],
            tx_data.get('from_address'),
            tx_data.get('to_address'),
            tx_data.get('amount'),
            tx_data.get('fee'),
            tx_data.get('status', 'pending'),
            tx_data.get('block_number'),
            tx_data.get('block_hash'),
            tx_data.get('gas_used'),
            tx_data.get('metadata', {})
        )
        
        if result:
            # Invalidate related cache entries
            await self._invalidate_cache("transactions_by_*")
            
            # Backup to Firestore
            await self._backup_to_firestore('transactions', str(tx_uuid), result)
        
        return result
    
    async def update_transaction_status(self, transaction_hash: str, status: str, 
                                      block_number: Optional[int] = None, 
                                      block_hash: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Update transaction status and confirmation details"""
        if block_number and block_hash:
            query = """
                UPDATE blockchain.transactions 
                SET status = $1, block_number = $2, block_hash = $3, 
                    confirmed_at = CASE WHEN $1 = 'confirmed' THEN NOW() ELSE confirmed_at END
                WHERE transaction_hash = $4
                RETURNING id, transaction_hash, transaction_type, from_address, to_address,
                          amount, fee, status, block_number, block_hash, gas_used,
                          metadata, created_at, confirmed_at
            """
            result = await self._execute_query_one(query, status, block_number, block_hash, transaction_hash)
        else:
            query = """
                UPDATE blockchain.transactions 
                SET status = $1,
                    confirmed_at = CASE WHEN $1 = 'confirmed' THEN NOW() ELSE confirmed_at END
                WHERE transaction_hash = $2
                RETURNING id, transaction_hash, transaction_type, from_address, to_address,
                          amount, fee, status, block_number, block_hash, gas_used,
                          metadata, created_at, confirmed_at
            """
            result = await self._execute_query_one(query, status, transaction_hash)
        
        if result:
            # Invalidate cache entries
            await self._invalidate_cache(f"transaction_by_hash:*{transaction_hash}*")
            await self._invalidate_cache("transactions_by_*")
            
            # Backup to Firestore
            await self._backup_to_firestore('transactions', str(result['id']), result)
        
        return result
    
    async def get_transactions_by_address(self, address: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get transactions involving a specific address"""
        query = """
            SELECT id, transaction_hash, transaction_type, from_address, to_address,
                   amount, fee, status, block_number, created_at, confirmed_at
            FROM blockchain.transactions 
            WHERE from_address = $1 OR to_address = $1
            ORDER BY created_at DESC
            LIMIT $2
        """
        return await self._execute_query(query, address, limit)
    
    async def get_transactions_by_type(self, transaction_type: str, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get transactions by type and optionally by status"""
        base_query = """
            SELECT id, transaction_hash, transaction_type, from_address, to_address,
                   amount, fee, status, block_number, created_at, confirmed_at
            FROM blockchain.transactions 
            WHERE transaction_type = $1
        """
        
        params = [transaction_type]
        if status:
            base_query += " AND status = $2"
            params.append(status)
            base_query += f" ORDER BY created_at DESC LIMIT ${len(params) + 1}"
            params.append(limit)
        else:
            base_query += f" ORDER BY created_at DESC LIMIT $2"
            params.append(limit)
        
        return await self._execute_query(base_query, *params)
    
    async def get_pending_transactions(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get pending transactions that need confirmation"""
        query = """
            SELECT id, transaction_hash, transaction_type, from_address, to_address,
                   amount, fee, metadata, created_at
            FROM blockchain.transactions 
            WHERE status = 'pending'
            ORDER BY created_at ASC
            LIMIT $1
        """
        return await self._execute_query(query, limit)
    
    # Price feed management
    async def create_price_feed(self, price_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new price feed entry"""
        price_uuid = uuid.uuid4()
        query = """
            INSERT INTO blockchain.price_feeds 
            (id, asset_symbol, price, source, timestamp, metadata)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id, asset_symbol, price, source, timestamp, metadata
        """
        
        result = await self._execute_query_one(
            query,
            price_uuid,
            price_data['asset_symbol'],
            price_data['price'],
            price_data['source'],
            price_data.get('timestamp', datetime.utcnow()),
            price_data.get('metadata', {})
        )
        
        if result:
            # Invalidate price cache
            await self._invalidate_cache(f"price_*{price_data['asset_symbol']}*")
            
            # Backup to Firestore
            await self._backup_to_firestore('price_feeds', str(price_uuid), result)
        
        return result
    
    @CachedQuery("latest_price", ttl=30)
    async def get_latest_price(self, asset_symbol: str, source: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get latest price for an asset"""
        if source:
            query = """
                SELECT id, asset_symbol, price, source, timestamp, metadata
                FROM blockchain.price_feeds 
                WHERE asset_symbol = $1 AND source = $2
                ORDER BY timestamp DESC
                LIMIT 1
            """
            return await self._execute_query_one(query, asset_symbol, source)
        else:
            query = """
                SELECT id, asset_symbol, price, source, timestamp, metadata
                FROM blockchain.price_feeds 
                WHERE asset_symbol = $1
                ORDER BY timestamp DESC
                LIMIT 1
            """
            return await self._execute_query_one(query, asset_symbol)
    
    @CachedQuery("price_history", ttl=300)
    async def get_price_history(self, asset_symbol: str, hours: int = 24, source: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get price history for an asset"""
        if source:
            query = """
                SELECT asset_symbol, price, source, timestamp, metadata
                FROM blockchain.price_feeds 
                WHERE asset_symbol = $1 AND source = $2
                AND timestamp >= NOW() - INTERVAL '%s hours'
                ORDER BY timestamp DESC
            """ % hours
            return await self._execute_query(query, asset_symbol, source)
        else:
            query = """
                SELECT asset_symbol, price, source, timestamp, metadata
                FROM blockchain.price_feeds 
                WHERE asset_symbol = $1
                AND timestamp >= NOW() - INTERVAL '%s hours'
                ORDER BY timestamp DESC
            """ % hours
            return await self._execute_query(query, asset_symbol)
    
    @CachedQuery("price_aggregated", ttl=60)
    async def get_aggregated_price(self, asset_symbol: str, minutes: int = 5) -> Optional[Dict[str, Any]]:
        """Get aggregated price data from multiple sources"""
        query = """
            SELECT 
                asset_symbol,
                AVG(price) as avg_price,
                MAX(price) as max_price,
                MIN(price) as min_price,
                COUNT(*) as source_count,
                ARRAY_AGG(DISTINCT source) as sources,
                MAX(timestamp) as latest_timestamp
            FROM blockchain.price_feeds 
            WHERE asset_symbol = $1
            AND timestamp >= NOW() - INTERVAL '%s minutes'
            GROUP BY asset_symbol
        """ % minutes
        return await self._execute_query_one(query, asset_symbol)
    
    async def get_transaction_analytics(self, days: int = 7) -> Dict[str, Any]:
        """Get transaction analytics for the specified period"""
        cache_key = self._generate_cache_key("transaction_analytics", days)
        cached_analytics = await self._get_from_cache(cache_key)
        
        if cached_analytics:
            return cached_analytics
        
        # Transaction statistics
        tx_stats_query = """
            SELECT 
                COUNT(*) as total_transactions,
                COUNT(CASE WHEN status = 'confirmed' THEN 1 END) as confirmed_transactions,
                COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_transactions,
                COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_transactions,
                AVG(fee) as avg_fee,
                SUM(amount) as total_volume
            FROM blockchain.transactions 
            WHERE created_at >= NOW() - INTERVAL '%s days'
        """ % days
        tx_stats = await self._execute_query_one(tx_stats_query)
        
        # Transaction types distribution
        tx_types_query = """
            SELECT transaction_type, COUNT(*) as count, SUM(amount) as volume
            FROM blockchain.transactions 
            WHERE created_at >= NOW() - INTERVAL '%s days'
            GROUP BY transaction_type
            ORDER BY count DESC
        """ % days
        tx_types = await self._execute_query(tx_types_query)
        
        # Daily transaction volume
        daily_volume_query = """
            SELECT 
                DATE_TRUNC('day', created_at) as date,
                COUNT(*) as transaction_count,
                SUM(amount) as daily_volume,
                AVG(fee) as avg_fee
            FROM blockchain.transactions 
            WHERE created_at >= NOW() - INTERVAL '%s days'
            AND status = 'confirmed'
            GROUP BY DATE_TRUNC('day', created_at)
            ORDER BY date DESC
        """ % days
        daily_volume = await self._execute_query(daily_volume_query)
        
        analytics = {
            'transaction_statistics': tx_stats or {},
            'transaction_types': tx_types,
            'daily_volume': daily_volume
        }
        
        # Cache the analytics
        await self._set_cache(cache_key, analytics, 600)  # 10 minutes cache
        
        return analytics
    
    async def get_network_health(self) -> Dict[str, Any]:
        """Get network health metrics"""
        cache_key = "network_health"
        cached_health = await self._get_from_cache(cache_key)
        
        if cached_health:
            return cached_health
        
        # Recent transaction success rate
        success_rate_query = """
            SELECT 
                COUNT(*) as total_recent,
                COUNT(CASE WHEN status = 'confirmed' THEN 1 END) as confirmed_recent,
                AVG(EXTRACT(EPOCH FROM (confirmed_at - created_at))) as avg_confirmation_time
            FROM blockchain.transactions 
            WHERE created_at >= NOW() - INTERVAL '1 hour'
        """
        success_stats = await self._execute_query_one(success_rate_query)
        
        # Pending transaction backlog
        pending_query = """
            SELECT COUNT(*) as pending_count,
                   MAX(created_at) as oldest_pending
            FROM blockchain.transactions 
            WHERE status = 'pending'
        """
        pending_stats = await self._execute_query_one(pending_query)
        
        # Price feed freshness
        price_freshness_query = """
            SELECT 
                COUNT(DISTINCT asset_symbol) as tracked_assets,
                AVG(EXTRACT(EPOCH FROM (NOW() - timestamp))) as avg_age_seconds,
                MAX(timestamp) as latest_update
            FROM blockchain.price_feeds 
            WHERE timestamp >= NOW() - INTERVAL '1 hour'
        """
        price_stats = await self._execute_query_one(price_freshness_query)
        
        health = {
            'transaction_success': success_stats or {},
            'pending_backlog': pending_stats or {},
            'price_feed_health': price_stats or {}
        }
        
        # Cache the health metrics
        await self._set_cache(cache_key, health, 60)  # 1 minute cache
        
        return health
    
    async def cleanup_old_price_feeds(self, days_to_keep: int = 30) -> int:
        """Clean up old price feed data"""
        query = """
            DELETE FROM blockchain.price_feeds 
            WHERE timestamp < NOW() - INTERVAL '%s days'
        """ % days_to_keep
        
        result = await self._execute_command(query)
        
        # Extract number of deleted rows
        if result and "DELETE" in result:
            deleted_count = int(result.split()[1])
            logger.info(f"Cleaned up {deleted_count} old price feed records")
            
            # Invalidate price cache
            await self._invalidate_cache("price_*")
            
            return deleted_count
        
        return 0
    
    async def get_transaction_volume_by_period(self, period: str = 'day', limit: int = 30) -> List[Dict[str, Any]]:
        """Get transaction volume aggregated by time period"""
        if period not in ['hour', 'day', 'week']:
            period = 'day'
        
        cache_key = self._generate_cache_key("volume_by_period", period, limit)
        cached_volume = await self._get_from_cache(cache_key)
        
        if cached_volume:
            return cached_volume
        
        query = f"""
            SELECT 
                DATE_TRUNC('{period}', created_at) as period_start,
                COUNT(*) as transaction_count,
                SUM(CASE WHEN amount IS NOT NULL THEN amount ELSE 0 END) as total_volume,
                AVG(CASE WHEN amount IS NOT NULL THEN amount ELSE NULL END) as avg_amount,
                SUM(CASE WHEN fee IS NOT NULL THEN fee ELSE 0 END) as total_fees
            FROM blockchain.transactions 
            WHERE status = 'confirmed'
            AND created_at >= NOW() - INTERVAL '{limit} {period}s'
            GROUP BY DATE_TRUNC('{period}', created_at)
            ORDER BY period_start DESC
        """
        
        volume_data = await self._execute_query(query)
        
        # Cache the volume data
        await self._set_cache(cache_key, volume_data, 300)  # 5 minutes cache
        
        return volume_data
    
    async def get_gas_analytics(self, days: int = 7) -> Dict[str, Any]:
        """Get gas usage analytics"""
        cache_key = self._generate_cache_key("gas_analytics", days)
        cached_analytics = await self._get_from_cache(cache_key)
        
        if cached_analytics:
            return cached_analytics
        
        # Gas statistics by transaction type
        gas_stats_query = """
            SELECT 
                transaction_type,
                COUNT(*) as transaction_count,
                AVG(gas_used) as avg_gas,
                MAX(gas_used) as max_gas,
                MIN(gas_used) as min_gas,
                SUM(gas_used) as total_gas
            FROM blockchain.transactions 
            WHERE gas_used IS NOT NULL 
            AND created_at >= NOW() - INTERVAL '%s days'
            GROUP BY transaction_type
            ORDER BY avg_gas DESC
        """ % days
        gas_stats = await self._execute_query(gas_stats_query)
        
        # Fee statistics
        fee_stats_query = """
            SELECT 
                AVG(fee) as avg_fee,
                MAX(fee) as max_fee,
                MIN(fee) as min_fee,
                SUM(fee) as total_fees,
                COUNT(*) as transaction_count
            FROM blockchain.transactions 
            WHERE fee IS NOT NULL 
            AND created_at >= NOW() - INTERVAL '%s days'
            AND status = 'confirmed'
        """ % days
        fee_stats = await self._execute_query_one(fee_stats_query)
        
        analytics = {
            'gas_by_type': gas_stats,
            'fee_statistics': fee_stats or {}
        }
        
        # Cache the analytics
        await self._set_cache(cache_key, analytics, 600)  # 10 minutes cache
        
        return analytics
    
    async def search_transactions(self, search_filters: Dict[str, Any], limit: int = 50) -> List[Dict[str, Any]]:
        """Search transactions with various filters"""
        where_clauses = ["1=1"]  # Base condition
        values = []
        param_count = 1
        
        # Build dynamic query based on filters
        if 'transaction_type' in search_filters:
            where_clauses.append(f"transaction_type = ${param_count}")
            values.append(search_filters['transaction_type'])
            param_count += 1
        
        if 'status' in search_filters:
            where_clauses.append(f"status = ${param_count}")
            values.append(search_filters['status'])
            param_count += 1
        
        if 'address' in search_filters:
            where_clauses.append(f"(from_address = ${param_count} OR to_address = ${param_count})")
            values.append(search_filters['address'])
            param_count += 1
        
        if 'amount_range' in search_filters:
            min_amount, max_amount = search_filters['amount_range']
            where_clauses.append(f"amount BETWEEN ${param_count} AND ${param_count + 1}")
            values.extend([min_amount, max_amount])
            param_count += 2
        
        if 'date_range' in search_filters:
            start_date, end_date = search_filters['date_range']
            where_clauses.append(f"created_at BETWEEN ${param_count} AND ${param_count + 1}")
            values.extend([start_date, end_date])
            param_count += 2
        
        values.append(limit)
        query = f"""
            SELECT id, transaction_hash, transaction_type, from_address, to_address,
                   amount, fee, status, block_number, block_hash, gas_used,
                   metadata, created_at, confirmed_at
            FROM blockchain.transactions 
            WHERE {' AND '.join(where_clauses)}
            ORDER BY created_at DESC
            LIMIT ${param_count}
        """
        
        return await self._execute_query(query, *values)
    
    @CachedQuery("supported_assets", ttl=3600)
    async def get_supported_price_assets(self) -> List[str]:
        """Get list of assets with price feeds"""
        query = """
            SELECT DISTINCT asset_symbol
            FROM blockchain.price_feeds 
            WHERE timestamp >= NOW() - INTERVAL '24 hours'
            ORDER BY asset_symbol
        """
        results = await self._execute_query(query)
        return [row['asset_symbol'] for row in results]
    
    async def get_price_volatility(self, asset_symbol: str, hours: int = 24) -> Dict[str, Any]:
        """Calculate price volatility for an asset"""
        cache_key = self._generate_cache_key("price_volatility", asset_symbol, hours)
        cached_volatility = await self._get_from_cache(cache_key)
        
        if cached_volatility:
            return cached_volatility
        
        query = """
            SELECT 
                asset_symbol,
                COUNT(*) as data_points,
                AVG(price) as avg_price,
                STDDEV(price) as price_stddev,
                MAX(price) as max_price,
                MIN(price) as min_price,
                (MAX(price) - MIN(price)) / AVG(price) * 100 as price_range_percent
            FROM blockchain.price_feeds 
            WHERE asset_symbol = $1
            AND timestamp >= NOW() - INTERVAL '%s hours'
            GROUP BY asset_symbol
        """ % hours
        
        volatility = await self._execute_query_one(query, asset_symbol)
        
        if volatility:
            # Calculate volatility percentage
            if volatility['avg_price'] and volatility['price_stddev']:
                volatility['volatility_percent'] = (volatility['price_stddev'] / volatility['avg_price']) * 100
            else:
                volatility['volatility_percent'] = 0
        
        # Cache the volatility data
        await self._set_cache(cache_key, volatility or {}, 600)  # 10 minutes cache
        
        return volatility or {}
