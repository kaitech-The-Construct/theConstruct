"""
Trading repository for managing orders and escrows
"""
from typing import Dict, List, Optional, Any
from uuid import UUID
import uuid
from datetime import datetime, timedelta
from .base import BaseRepository, CachedQuery
import logging

logger = logging.getLogger(__name__)

class TradingRepository(BaseRepository):
    """Repository for managing trading orders and escrows"""
    
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.cache_ttl = 60  # 1 minute for trading data (more volatile)
    
    # Order management
    @CachedQuery("order_by_id", ttl=60)
    async def get_order_by_id(self, order_id: UUID) -> Optional[Dict[str, Any]]:
        """Get order by ID"""
        query = """
            SELECT o.id, o.order_id, o.user_id, o.asset_id, o.order_type, o.amount,
                   o.price, o.filled_amount, o.status, o.transaction_hash, o.expiration,
                   o.created_at, o.updated_at,
                   u.wallet_address as user_wallet,
                   a.asset_name, a.asset_type
            FROM trading.orders o
            JOIN blockchain.users u ON o.user_id = u.id
            JOIN blockchain.assets a ON o.asset_id = a.id
            WHERE o.id = $1
        """
        return await self._execute_query_one(query, order_id)
    
    @CachedQuery("order_by_order_id", ttl=60)
    async def get_order_by_order_id(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Get order by order_id string"""
        query = """
            SELECT o.id, o.order_id, o.user_id, o.asset_id, o.order_type, o.amount,
                   o.price, o.filled_amount, o.status, o.transaction_hash, o.expiration,
                   o.created_at, o.updated_at,
                   u.wallet_address as user_wallet,
                   a.asset_name, a.asset_type
            FROM trading.orders o
            JOIN blockchain.users u ON o.user_id = u.id
            JOIN blockchain.assets a ON o.asset_id = a.id
            WHERE o.order_id = $1
        """
        return await self._execute_query_one(query, order_id)
    
    async def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new trading order"""
        order_uuid = uuid.uuid4()
        query = """
            INSERT INTO trading.orders 
            (id, order_id, user_id, asset_id, order_type, amount, price, 
             filled_amount, status, transaction_hash, expiration)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            RETURNING id, order_id, user_id, asset_id, order_type, amount, price,
                      filled_amount, status, transaction_hash, expiration,
                      created_at, updated_at
        """
        
        result = await self._execute_query_one(
            query,
            order_uuid,
            order_data['order_id'],
            order_data['user_id'],
            order_data['asset_id'],
            order_data['order_type'],
            order_data['amount'],
            order_data['price'],
            order_data.get('filled_amount', 0),
            order_data.get('status', 'pending'),
            order_data.get('transaction_hash'),
            order_data.get('expiration')
        )
        
        if result:
            # Invalidate related cache entries
            await self._invalidate_cache("order_book:*")
            await self._invalidate_cache("user_orders:*")
            
            # Backup to Firestore
            await self._backup_to_firestore('orders', str(order_uuid), result)
        
        return result
    
    async def update_order(self, order_id: UUID, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update order data"""
        set_clauses = []
        values = []
        param_count = 1
        
        allowed_fields = ['filled_amount', 'status', 'transaction_hash']
        
        for field, value in update_data.items():
            if field in allowed_fields:
                set_clauses.append(f"{field} = ${param_count}")
                values.append(value)
                param_count += 1
        
        if not set_clauses:
            return await self.get_order_by_id(order_id)
        
        values.append(order_id)
        query = f"""
            UPDATE trading.orders 
            SET {', '.join(set_clauses)}, updated_at = NOW()
            WHERE id = ${param_count}
            RETURNING id, order_id, user_id, asset_id, order_type, amount, price,
                      filled_amount, status, transaction_hash, expiration,
                      created_at, updated_at
        """
        
        result = await self._execute_query_one(query, *values)
        
        if result:
            # Invalidate cache entries
            await self._invalidate_cache(f"order_by_id:*{order_id}*")
            await self._invalidate_cache(f"order_by_order_id:*{result['order_id']}*")
            await self._invalidate_cache("order_book:*")
            
            # Backup to Firestore
            await self._backup_to_firestore('orders', str(order_id), result)
        
        return result
    
    @CachedQuery("order_book", ttl=30)
    async def get_order_book(self, asset_id: UUID, limit: int = 50) -> Dict[str, List[Dict[str, Any]]]:
        """Get order book for an asset"""
        buy_orders_query = """
            SELECT id, order_id, amount, price, filled_amount, created_at
            FROM trading.orders 
            WHERE asset_id = $1 AND order_type = 'buy' AND status = 'active'
            ORDER BY price DESC, created_at ASC
            LIMIT $2
        """
        
        sell_orders_query = """
            SELECT id, order_id, amount, price, filled_amount, created_at
            FROM trading.orders 
            WHERE asset_id = $1 AND order_type = 'sell' AND status = 'active'
            ORDER BY price ASC, created_at ASC
            LIMIT $2
        """
        
        buy_orders = await self._execute_query(buy_orders_query, asset_id, limit)
        sell_orders = await self._execute_query(sell_orders_query, asset_id, limit)
        
        return {
            'buy_orders': buy_orders,
            'sell_orders': sell_orders
        }
    
    async def get_user_orders(self, user_id: UUID, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get orders for a specific user"""
        base_query = """
            SELECT o.id, o.order_id, o.asset_id, o.order_type, o.amount, o.price,
                   o.filled_amount, o.status, o.expiration, o.created_at,
                   a.asset_name, a.asset_type
            FROM trading.orders o
            JOIN blockchain.assets a ON o.asset_id = a.id
            WHERE o.user_id = $1
        """
        
        params = [user_id]
        if status:
            base_query += " AND o.status = $2"
            params.append(status)
            base_query += f" ORDER BY o.created_at DESC LIMIT ${len(params) + 1}"
            params.append(limit)
        else:
            base_query += f" ORDER BY o.created_at DESC LIMIT $2"
            params.append(limit)
        
        return await self._execute_query(base_query, *params)
    
    # Escrow management
    @CachedQuery("escrow_by_id", ttl=300)
    async def get_escrow_by_id(self, escrow_id: UUID) -> Optional[Dict[str, Any]]:
        """Get escrow by ID"""
        query = """
            SELECT e.id, e.escrow_id, e.creator_id, e.destination_address, e.amount,
                   e.condition_hash, e.finish_after, e.status, e.transaction_hash,
                   e.created_at, e.updated_at,
                   u.wallet_address as creator_wallet
            FROM trading.escrows e
            JOIN blockchain.users u ON e.creator_id = u.id
            WHERE e.id = $1
        """
        return await self._execute_query_one(query, escrow_id)
    
    async def create_escrow(self, escrow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new escrow"""
        escrow_uuid = uuid.uuid4()
        query = """
            INSERT INTO trading.escrows 
            (id, escrow_id, creator_id, destination_address, amount, 
             condition_hash, finish_after, status, transaction_hash)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING id, escrow_id, creator_id, destination_address, amount,
                      condition_hash, finish_after, status, transaction_hash,
                      created_at, updated_at
        """
        
        result = await self._execute_query_one(
            query,
            escrow_uuid,
            escrow_data['escrow_id'],
            escrow_data['creator_id'],
            escrow_data['destination_address'],
            escrow_data['amount'],
            escrow_data.get('condition_hash'),
            escrow_data.get('finish_after'),
            escrow_data.get('status', 'created'),
            escrow_data.get('transaction_hash')
        )
        
        if result:
            # Invalidate related cache entries
            await self._invalidate_cache("user_escrows:*")
            
            # Backup to Firestore
            await self._backup_to_firestore('escrows', str(escrow_uuid), result)
        
        return result
    
    async def update_escrow_status(self, escrow_id: UUID, status: str, transaction_hash: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Update escrow status"""
        if transaction_hash:
            query = """
                UPDATE trading.escrows 
                SET status = $1, transaction_hash = $2, updated_at = NOW()
                WHERE id = $3
                RETURNING id, escrow_id, creator_id, destination_address, amount,
                          condition_hash, finish_after, status, transaction_hash,
                          created_at, updated_at
            """
            result = await self._execute_query_one(query, status, transaction_hash, escrow_id)
        else:
            query = """
                UPDATE trading.escrows 
                SET status = $1, updated_at = NOW()
                WHERE id = $2
                RETURNING id, escrow_id, creator_id, destination_address, amount,
                          condition_hash, finish_after, status, transaction_hash,
                          created_at, updated_at
            """
            result = await self._execute_query_one(query, status, escrow_id)
        
        if result:
            # Invalidate cache entries
            await self._invalidate_cache(f"escrow_by_id:*{escrow_id}*")
            await self._invalidate_cache("user_escrows:*")
            
            # Backup to Firestore
            await self._backup_to_firestore('escrows', str(escrow_id), result)
        
        return result
    
    async def get_user_escrows(self, user_id: UUID, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get escrows for a specific user"""
        base_query = """
            SELECT id, escrow_id, destination_address, amount, condition_hash,
                   finish_after, status, transaction_hash, created_at
            FROM trading.escrows 
            WHERE creator_id = $1
        """
        
        params = [user_id]
        if status:
            base_query += " AND status = $2"
            params.append(status)
        
        base_query += " ORDER BY created_at DESC"
        
        return await self._execute_query(base_query, *params)
    
    async def get_expired_escrows(self) -> List[Dict[str, Any]]:
        """Get escrows that have passed their finish_after time"""
        query = """
            SELECT id, escrow_id, creator_id, destination_address, amount,
                   finish_after, status, created_at
            FROM trading.escrows 
            WHERE finish_after < NOW() AND status = 'active'
            ORDER BY finish_after ASC
        """
        return await self._execute_query(query)
    
    async def get_market_summary(self, asset_id: Optional[UUID] = None) -> Dict[str, Any]:
        """Get market summary statistics"""
        cache_key = self._generate_cache_key("market_summary", asset_id or "all")
        cached_summary = await self._get_from_cache(cache_key)
        
        if cached_summary:
            return cached_summary
        
        if asset_id:
            # Asset-specific market summary
            query = """
                SELECT 
                    COUNT(*) as total_orders,
                    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_orders,
                    COUNT(CASE WHEN status = 'filled' THEN 1 END) as filled_orders,
                    AVG(CASE WHEN status = 'filled' THEN price ELSE NULL END) as avg_price,
                    MAX(CASE WHEN status = 'filled' THEN price ELSE NULL END) as high_price,
                    MIN(CASE WHEN status = 'filled' THEN price ELSE NULL END) as low_price,
                    SUM(CASE WHEN status = 'filled' THEN amount ELSE 0 END) as volume
                FROM trading.orders 
                WHERE asset_id = $1 AND created_at >= NOW() - INTERVAL '24 hours'
            """
            summary = await self._execute_query_one(query, asset_id)
        else:
            # Overall market summary
            query = """
                SELECT 
                    COUNT(*) as total_orders,
                    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_orders,
                    COUNT(CASE WHEN status = 'filled' THEN 1 END) as filled_orders,
                    COUNT(DISTINCT asset_id) as active_assets,
                    SUM(CASE WHEN status = 'filled' THEN amount * price ELSE 0 END) as total_volume
                FROM trading.orders 
                WHERE created_at >= NOW() - INTERVAL '24 hours'
            """
            summary = await self._execute_query_one(query)
        
        # Cache the summary
        await self._set_cache(cache_key, summary, 60)  # 1 minute cache
        
        return summary or {}
    
    async def get_price_history(self, asset_id: UUID, hours: int = 24, interval_minutes: int = 60) -> List[Dict[str, Any]]:
        """Get price history for an asset"""
        cache_key = self._generate_cache_key("price_history", asset_id, hours, interval_minutes)
        cached_history = await self._get_from_cache(cache_key)
        
        if cached_history:
            return cached_history
        
        query = """
            SELECT 
                DATE_TRUNC('hour', created_at) as time_bucket,
                AVG(price) as avg_price,
                MAX(price) as high_price,
                MIN(price) as low_price,
                SUM(amount) as volume,
                COUNT(*) as trade_count
            FROM trading.orders 
            WHERE asset_id = $1 
            AND status = 'filled' 
            AND created_at >= NOW() - INTERVAL '%s hours'
            GROUP BY DATE_TRUNC('hour', created_at)
            ORDER BY time_bucket DESC
        """ % hours
        
        history = await self._execute_query(query, asset_id)
        
        # Cache the history
        await self._set_cache(cache_key, history, 300)  # 5 minutes cache
        
        return history
    
    async def match_orders(self, buy_order_id: UUID, sell_order_id: UUID, match_amount: float, match_price: float) -> Dict[str, Any]:
        """Match buy and sell orders"""
        from .base import TransactionManager
        
        async with TransactionManager(self.db_manager) as tx:
            # Update buy order
            buy_update = await tx.fetchrow("""
                UPDATE trading.orders 
                SET filled_amount = filled_amount + $1,
                    status = CASE 
                        WHEN filled_amount + $1 >= amount THEN 'filled'
                        ELSE 'partially_filled'
                    END,
                    updated_at = NOW()
                WHERE id = $2
                RETURNING id, filled_amount, amount, status
            """, match_amount, buy_order_id)
            
            # Update sell order
            sell_update = await tx.fetchrow("""
                UPDATE trading.orders 
                SET filled_amount = filled_amount + $1,
                    status = CASE 
                        WHEN filled_amount + $1 >= amount THEN 'filled'
                        ELSE 'partially_filled'
                    END,
                    updated_at = NOW()
                WHERE id = $2
                RETURNING id, filled_amount, amount, status
            """, match_amount, sell_order_id)
        
        # Invalidate cache entries
        await self._invalidate_cache("order_by_id:*")
        await self._invalidate_cache("order_book:*")
        
        return {
            'buy_order': dict(buy_update) if buy_update else None,
            'sell_order': dict(sell_update) if sell_update else None,
            'match_amount': match_amount,
            'match_price': match_price
        }
    
    async def cancel_order(self, order_id: UUID) -> bool:
        """Cancel an active order"""
        query = """
            UPDATE trading.orders 
            SET status = 'cancelled', updated_at = NOW()
            WHERE id = $1 AND status IN ('active', 'pending')
        """
        
        result = await self._execute_command(query, order_id)
        
        if result and "UPDATE 1" in result:
            # Invalidate cache entries
            await self._invalidate_cache(f"order_by_id:*{order_id}*")
            await self._invalidate_cache("order_book:*")
            return True
        
        return False
    
    async def get_active_orders_by_asset(self, asset_id: UUID) -> List[Dict[str, Any]]:
        """Get all active orders for an asset"""
        query = """
            SELECT o.id, o.order_id, o.user_id, o.order_type, o.amount, o.price,
                   o.filled_amount, o.created_at,
                   u.wallet_address as user_wallet
            FROM trading.orders o
            JOIN blockchain.users u ON o.user_id = u.id
            WHERE o.asset_id = $1 AND o.status = 'active'
            ORDER BY 
                CASE WHEN o.order_type = 'buy' THEN o.price END DESC,
                CASE WHEN o.order_type = 'sell' THEN o.price END ASC,
                o.created_at ASC
        """
        return await self._execute_query(query, asset_id)
    
    async def get_recent_trades(self, asset_id: Optional[UUID] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent completed trades"""
        if asset_id:
            query = """
                SELECT o.order_id, o.order_type, o.amount, o.price, o.created_at,
                       a.asset_name, a.asset_type,
                       u.wallet_address as trader_wallet
                FROM trading.orders o
                JOIN blockchain.assets a ON o.asset_id = a.id
                JOIN blockchain.users u ON o.user_id = u.id
                WHERE o.asset_id = $1 AND o.status = 'filled'
                ORDER BY o.created_at DESC
                LIMIT $2
            """
            return await self._execute_query(query, asset_id, limit)
        else:
            query = """
                SELECT o.order_id, o.order_type, o.amount, o.price, o.created_at,
                       a.asset_name, a.asset_type,
                       u.wallet_address as trader_wallet
                FROM trading.orders o
                JOIN blockchain.assets a ON o.asset_id = a.id
                JOIN blockchain.users u ON o.user_id = u.id
                WHERE o.status = 'filled'
                ORDER BY o.created_at DESC
                LIMIT $1
            """
            return await self._execute_query(query, limit)
