"""
Manufacturing repository for managing orders, milestones, and quality assurance
"""
from typing import Dict, List, Optional, Any
from uuid import UUID
import uuid
from datetime import datetime, timedelta
from .base import BaseRepository, CachedQuery
import logging

logger = logging.getLogger(__name__)

class ManufacturingRepository(BaseRepository):
    """Repository for managing manufacturing orders and processes"""
    
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.cache_ttl = 300  # 5 minutes for manufacturing data
    
    # Manufacturing order management
    @CachedQuery("mfg_order_by_id", ttl=300)
    async def get_order_by_id(self, order_id: UUID) -> Optional[Dict[str, Any]]:
        """Get manufacturing order by ID"""
        query = """
            SELECT o.id, o.order_id, o.customer_id, o.manufacturer_id, o.component_id,
                   o.quantity, o.specifications, o.delivery_address, o.max_price,
                   o.deadline, o.status, o.created_at, o.updated_at,
                   c.wallet_address as customer_wallet,
                   m.wallet_address as manufacturer_wallet,
                   a.asset_name, a.asset_type
            FROM manufacturing.orders o
            JOIN blockchain.users c ON o.customer_id = c.id
            LEFT JOIN blockchain.users m ON o.manufacturer_id = m.id
            JOIN blockchain.assets a ON o.component_id = a.id
            WHERE o.id = $1
        """
        return await self._execute_query_one(query, order_id)
    
    @CachedQuery("mfg_order_by_order_id", ttl=300)
    async def get_order_by_order_id(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Get manufacturing order by order_id string"""
        query = """
            SELECT o.id, o.order_id, o.customer_id, o.manufacturer_id, o.component_id,
                   o.quantity, o.specifications, o.delivery_address, o.max_price,
                   o.deadline, o.status, o.created_at, o.updated_at,
                   c.wallet_address as customer_wallet,
                   m.wallet_address as manufacturer_wallet,
                   a.asset_name, a.asset_type
            FROM manufacturing.orders o
            JOIN blockchain.users c ON o.customer_id = c.id
            LEFT JOIN blockchain.users m ON o.manufacturer_id = m.id
            JOIN blockchain.assets a ON o.component_id = a.id
            WHERE o.order_id = $1
        """
        return await self._execute_query_one(query, order_id)
    
    async def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new manufacturing order"""
        order_uuid = uuid.uuid4()
        query = """
            INSERT INTO manufacturing.orders 
            (id, order_id, customer_id, manufacturer_id, component_id, quantity,
             specifications, delivery_address, max_price, deadline, status)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            RETURNING id, order_id, customer_id, manufacturer_id, component_id,
                      quantity, specifications, delivery_address, max_price,
                      deadline, status, created_at, updated_at
        """
        
        result = await self._execute_query_one(
            query,
            order_uuid,
            order_data['order_id'],
            order_data['customer_id'],
            order_data.get('manufacturer_id'),
            order_data['component_id'],
            order_data['quantity'],
            order_data['specifications'],
            order_data['delivery_address'],
            order_data['max_price'],
            order_data['deadline'],
            order_data.get('status', 'pending')
        )
        
        if result:
            # Invalidate related cache entries
            await self._invalidate_cache("mfg_orders_by_*")
            
            # Backup to Firestore
            await self._backup_to_firestore('manufacturing_orders', str(order_uuid), result)
        
        return result
    
    async def update_order(self, order_id: UUID, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update manufacturing order"""
        set_clauses = []
        values = []
        param_count = 1
        
        allowed_fields = [
            'manufacturer_id', 'specifications', 'delivery_address', 
            'max_price', 'deadline', 'status'
        ]
        
        for field, value in update_data.items():
            if field in allowed_fields:
                set_clauses.append(f"{field} = ${param_count}")
                values.append(value)
                param_count += 1
        
        if not set_clauses:
            return await self.get_order_by_id(order_id)
        
        values.append(order_id)
        query = f"""
            UPDATE manufacturing.orders 
            SET {', '.join(set_clauses)}, updated_at = NOW()
            WHERE id = ${param_count}
            RETURNING id, order_id, customer_id, manufacturer_id, component_id,
                      quantity, specifications, delivery_address, max_price,
                      deadline, status, created_at, updated_at
        """
        
        result = await self._execute_query_one(query, *values)
        
        if result:
            # Invalidate cache entries
            await self._invalidate_cache(f"mfg_order_by_id:*{order_id}*")
            await self._invalidate_cache(f"mfg_order_by_order_id:*{result['order_id']}*")
            await self._invalidate_cache("mfg_orders_by_*")
            
            # Backup to Firestore
            await self._backup_to_firestore('manufacturing_orders', str(order_id), result)
        
        return result
    
    async def get_orders_by_customer(self, customer_id: UUID, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get manufacturing orders by customer"""
        base_query = """
            SELECT o.id, o.order_id, o.manufacturer_id, o.component_id, o.quantity,
                   o.specifications, o.max_price, o.deadline, o.status, o.created_at,
                   m.wallet_address as manufacturer_wallet,
                   a.asset_name, a.asset_type
            FROM manufacturing.orders o
            LEFT JOIN blockchain.users m ON o.manufacturer_id = m.id
            JOIN blockchain.assets a ON o.component_id = a.id
            WHERE o.customer_id = $1
        """
        
        params = [customer_id]
        if status:
            base_query += " AND o.status = $2"
            params.append(status)
            base_query += f" ORDER BY o.created_at DESC LIMIT ${len(params) + 1}"
            params.append(limit)
        else:
            base_query += f" ORDER BY o.created_at DESC LIMIT $2"
            params.append(limit)
        
        return await self._execute_query(base_query, *params)
    
    async def get_orders_by_manufacturer(self, manufacturer_id: UUID, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get manufacturing orders by manufacturer"""
        base_query = """
            SELECT o.id, o.order_id, o.customer_id, o.component_id, o.quantity,
                   o.specifications, o.delivery_address, o.max_price, o.deadline,
                   o.status, o.created_at,
                   c.wallet_address as customer_wallet,
                   a.asset_name, a.asset_type
            FROM manufacturing.orders o
            JOIN blockchain.users c ON o.customer_id = c.id
            JOIN blockchain.assets a ON o.component_id = a.id
            WHERE o.manufacturer_id = $1
        """
        
        params = [manufacturer_id]
        if status:
            base_query += " AND o.status = $2"
            params.append(status)
            base_query += f" ORDER BY o.created_at DESC LIMIT ${len(params) + 1}"
            params.append(limit)
        else:
            base_query += f" ORDER BY o.created_at DESC LIMIT $2"
            params.append(limit)
        
        return await self._execute_query(base_query, *params)
    
    async def get_available_orders(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get manufacturing orders available for manufacturers to accept"""
        query = """
            SELECT o.id, o.order_id, o.customer_id, o.component_id, o.quantity,
                   o.specifications, o.max_price, o.deadline, o.created_at,
                   c.wallet_address as customer_wallet,
                   a.asset_name, a.asset_type, a.specifications as component_specs
            FROM manufacturing.orders o
            JOIN blockchain.users c ON o.customer_id = c.id
            JOIN blockchain.assets a ON o.component_id = a.id
            WHERE o.manufacturer_id IS NULL AND o.status = 'pending'
            ORDER BY o.created_at DESC
            LIMIT $1
        """
        return await self._execute_query(query, limit)
    
    # Milestone management
    async def get_milestones_by_order(self, order_id: UUID) -> List[Dict[str, Any]]:
        """Get all milestones for a manufacturing order"""
        query = """
            SELECT id, milestone_number, description, payment_percentage, status,
                   completed_at, payment_released, transaction_hash, created_at, updated_at
            FROM manufacturing.milestones 
            WHERE order_id = $1
            ORDER BY milestone_number ASC
        """
        return await self._execute_query(query, order_id)
    
    async def create_milestone(self, milestone_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new milestone"""
        milestone_uuid = uuid.uuid4()
        query = """
            INSERT INTO manufacturing.milestones 
            (id, order_id, milestone_number, description, payment_percentage, status)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id, order_id, milestone_number, description, payment_percentage,
                      status, completed_at, payment_released, transaction_hash,
                      created_at, updated_at
        """
        
        result = await self._execute_query_one(
            query,
            milestone_uuid,
            milestone_data['order_id'],
            milestone_data['milestone_number'],
            milestone_data['description'],
            milestone_data['payment_percentage'],
            milestone_data.get('status', 'pending')
        )
        
        if result:
            # Backup to Firestore
            await self._backup_to_firestore('milestones', str(milestone_uuid), result)
        
        return result
    
    async def complete_milestone(self, milestone_id: UUID, transaction_hash: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Mark milestone as completed and optionally release payment"""
        query = """
            UPDATE manufacturing.milestones 
            SET status = 'completed', 
                completed_at = NOW(),
                payment_released = CASE WHEN $2 IS NOT NULL THEN true ELSE payment_released END,
                transaction_hash = COALESCE($2, transaction_hash),
                updated_at = NOW()
            WHERE id = $1
            RETURNING id, order_id, milestone_number, description, payment_percentage,
                      status, completed_at, payment_released, transaction_hash,
                      created_at, updated_at
        """
        
        result = await self._execute_query_one(query, milestone_id, transaction_hash)
        
        if result:
            # Backup to Firestore
            await self._backup_to_firestore('milestones', str(milestone_id), result)
        
        return result
    
    async def get_pending_milestones(self, manufacturer_id: UUID) -> List[Dict[str, Any]]:
        """Get pending milestones for a manufacturer"""
        query = """
            SELECT m.id, m.order_id, m.milestone_number, m.description, 
                   m.payment_percentage, m.status, m.created_at,
                   o.order_id as order_string_id, o.quantity, o.deadline,
                   c.wallet_address as customer_wallet,
                   a.asset_name
            FROM manufacturing.milestones m
            JOIN manufacturing.orders o ON m.order_id = o.id
            JOIN blockchain.users c ON o.customer_id = c.id
            JOIN blockchain.assets a ON o.component_id = a.id
            WHERE o.manufacturer_id = $1 AND m.status = 'pending'
            ORDER BY o.deadline ASC, m.milestone_number ASC
        """
        return await self._execute_query(query, manufacturer_id)
    
    # Quality assurance management
    async def create_quality_record(self, qa_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a quality assurance record"""
        qa_uuid = uuid.uuid4()
        query = """
            INSERT INTO manufacturing.quality_assurance 
            (id, order_id, inspector_id, quality_metrics, passed, notes)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id, order_id, inspector_id, quality_metrics, passed, notes,
                      inspection_date, created_at
        """
        
        result = await self._execute_query_one(
            query,
            qa_uuid,
            qa_data['order_id'],
            qa_data['inspector_id'],
            qa_data['quality_metrics'],
            qa_data['passed'],
            qa_data.get('notes', '')
        )
        
        if result:
            # Backup to Firestore
            await self._backup_to_firestore('quality_assurance', str(qa_uuid), result)
        
        return result
    
    async def get_quality_records_by_order(self, order_id: UUID) -> List[Dict[str, Any]]:
        """Get all quality assurance records for an order"""
        query = """
            SELECT qa.id, qa.quality_metrics, qa.passed, qa.notes, qa.inspection_date,
                   qa.created_at,
                   i.wallet_address as inspector_wallet,
                   i.metadata as inspector_info
            FROM manufacturing.quality_assurance qa
            JOIN blockchain.users i ON qa.inspector_id = i.id
            WHERE qa.order_id = $1
            ORDER BY qa.inspection_date DESC
        """
        return await self._execute_query(query, order_id)
    
    async def get_order_progress(self, order_id: UUID) -> Dict[str, Any]:
        """Get comprehensive order progress including milestones and QA"""
        cache_key = self._generate_cache_key("order_progress", order_id)
        cached_progress = await self._get_from_cache(cache_key)
        
        if cached_progress:
            return cached_progress
        
        # Get order details
        order = await self.get_order_by_id(order_id)
        if not order:
            return {}
        
        # Get milestones
        milestones = await self.get_milestones_by_order(order_id)
        
        # Get quality records
        quality_records = await self.get_quality_records_by_order(order_id)
        
        # Calculate progress metrics
        total_milestones = len(milestones)
        completed_milestones = len([m for m in milestones if m['status'] == 'completed'])
        total_payment_released = sum([
            m['payment_percentage'] for m in milestones 
            if m['payment_released']
        ])
        
        progress = {
            'order': order,
            'milestones': milestones,
            'quality_records': quality_records,
            'progress_metrics': {
                'total_milestones': total_milestones,
                'completed_milestones': completed_milestones,
                'completion_percentage': (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0,
                'payment_released_percentage': total_payment_released,
                'remaining_payment_percentage': 100 - total_payment_released
            }
        }
        
        # Cache the progress
        await self._set_cache(cache_key, progress, 180)  # 3 minutes cache
        
        return progress
    
    async def assign_manufacturer(self, order_id: UUID, manufacturer_id: UUID) -> Optional[Dict[str, Any]]:
        """Assign a manufacturer to an order"""
        query = """
            UPDATE manufacturing.orders 
            SET manufacturer_id = $1, status = 'assigned', updated_at = NOW()
            WHERE id = $2 AND status = 'pending'
            RETURNING id, order_id, customer_id, manufacturer_id, component_id,
                      quantity, specifications, delivery_address, max_price,
                      deadline, status, created_at, updated_at
        """
        
        result = await self._execute_query_one(query, manufacturer_id, order_id)
        
        if result:
            # Invalidate cache entries
            await self._invalidate_cache(f"mfg_order_by_id:*{order_id}*")
            await self._invalidate_cache("mfg_orders_by_*")
            
            # Backup to Firestore
            await self._backup_to_firestore('manufacturing_orders', str(order_id), result)
        
        return result
    
    async def get_overdue_orders(self) -> List[Dict[str, Any]]:
        """Get manufacturing orders that are past their deadline"""
        query = """
            SELECT o.id, o.order_id, o.customer_id, o.manufacturer_id, o.deadline,
                   o.status, o.created_at,
                   c.wallet_address as customer_wallet,
                   m.wallet_address as manufacturer_wallet,
                   a.asset_name
            FROM manufacturing.orders o
            JOIN blockchain.users c ON o.customer_id = c.id
            LEFT JOIN blockchain.users m ON o.manufacturer_id = m.id
            JOIN blockchain.assets a ON o.component_id = a.id
            WHERE o.deadline < NOW() AND o.status NOT IN ('completed', 'cancelled')
            ORDER BY o.deadline ASC
        """
        return await self._execute_query(query)
    
    async def get_manufacturer_workload(self, manufacturer_id: UUID) -> Dict[str, Any]:
        """Get current workload for a manufacturer"""
        cache_key = self._generate_cache_key("manufacturer_workload", manufacturer_id)
        cached_workload = await self._get_from_cache(cache_key)
        
        if cached_workload:
            return cached_workload
        
        # Get active orders
        active_orders_query = """
            SELECT COUNT(*) as active_orders,
                   SUM(quantity) as total_quantity,
                   AVG(EXTRACT(EPOCH FROM (deadline - NOW())) / 86400) as avg_days_to_deadline
            FROM manufacturing.orders 
            WHERE manufacturer_id = $1 AND status IN ('assigned', 'in_progress')
        """
        active_stats = await self._execute_query_one(active_orders_query, manufacturer_id)
        
        # Get completion stats
        completion_stats_query = """
            SELECT 
                COUNT(*) as total_completed,
                AVG(EXTRACT(EPOCH FROM (updated_at - created_at)) / 86400) as avg_completion_days,
                COUNT(CASE WHEN updated_at <= deadline THEN 1 END) as on_time_deliveries
            FROM manufacturing.orders 
            WHERE manufacturer_id = $1 AND status = 'completed'
            AND created_at >= NOW() - INTERVAL '90 days'
        """
        completion_stats = await self._execute_query_one(completion_stats_query, manufacturer_id)
        
        workload = {
            'active': active_stats or {},
            'completion': completion_stats or {}
        }
        
        # Cache the workload
        await self._set_cache(cache_key, workload, 300)  # 5 minutes cache
        
        return workload
    
    async def search_orders(self, search_filters: Dict[str, Any], limit: int = 50) -> List[Dict[str, Any]]:
        """Search manufacturing orders with various filters"""
        where_clauses = ["1=1"]  # Base condition
        values = []
        param_count = 1
        
        # Build dynamic query based on filters
        if 'status' in search_filters:
            where_clauses.append(f"o.status = ${param_count}")
            values.append(search_filters['status'])
            param_count += 1
        
        if 'component_type' in search_filters:
            where_clauses.append(f"a.asset_type = ${param_count}")
            values.append(search_filters['component_type'])
            param_count += 1
        
        if 'max_price_range' in search_filters:
            min_price, max_price = search_filters['max_price_range']
            where_clauses.append(f"o.max_price BETWEEN ${param_count} AND ${param_count + 1}")
            values.extend([min_price, max_price])
            param_count += 2
        
        if 'deadline_before' in search_filters:
            where_clauses.append(f"o.deadline <= ${param_count}")
            values.append(search_filters['deadline_before'])
            param_count += 1
        
        if 'specifications' in search_filters:
            for spec_key, spec_value in search_filters['specifications'].items():
                where_clauses.append(f"o.specifications->>'{spec_key}' = ${param_count}")
                values.append(str(spec_value))
                param_count += 1
        
        values.append(limit)
        query = f"""
            SELECT o.id, o.order_id, o.customer_id, o.manufacturer_id, o.component_id,
                   o.quantity, o.specifications, o.max_price, o.deadline, o.status,
                   o.created_at,
                   c.wallet_address as customer_wallet,
                   m.wallet_address as manufacturer_wallet,
                   a.asset_name, a.asset_type
            FROM manufacturing.orders o
            JOIN blockchain.users c ON o.customer_id = c.id
            LEFT JOIN blockchain.users m ON o.manufacturer_id = m.id
            JOIN blockchain.assets a ON o.component_id = a.id
            WHERE {' AND '.join(where_clauses)}
            ORDER BY o.created_at DESC
            LIMIT ${param_count}
        """
        
        return await self._execute_query(query, *values)
    
    async def get_manufacturing_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get manufacturing analytics for the specified period"""
        cache_key = self._generate_cache_key("manufacturing_analytics", days)
        cached_analytics = await self._get_from_cache(cache_key)
        
        if cached_analytics:
            return cached_analytics
        
        # Order statistics
        order_stats_query = """
            SELECT 
                COUNT(*) as total_orders,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_orders,
                COUNT(CASE WHEN status = 'in_progress' THEN 1 END) as in_progress_orders,
                COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_orders,
                AVG(max_price) as avg_order_value,
                SUM(quantity) as total_quantity
            FROM manufacturing.orders 
            WHERE created_at >= NOW() - INTERVAL '%s days'
        """ % days
        order_stats = await self._execute_query_one(order_stats_query)
        
        # Component type distribution
        component_stats_query = """
            SELECT a.asset_type, COUNT(*) as order_count, SUM(o.quantity) as total_quantity
            FROM manufacturing.orders o
            JOIN blockchain.assets a ON o.component_id = a.id
            WHERE o.created_at >= NOW() - INTERVAL '%s days'
            GROUP BY a.asset_type
            ORDER BY order_count DESC
        """ % days
        component_stats = await self._execute_query(component_stats_query)
        
        # Manufacturer performance
        manufacturer_stats_query = """
            SELECT 
                m.wallet_address,
                COUNT(*) as orders_completed,
                AVG(EXTRACT(EPOCH FROM (o.updated_at - o.created_at)) / 86400) as avg_completion_days,
                COUNT(CASE WHEN o.updated_at <= o.deadline THEN 1 END) as on_time_deliveries
            FROM manufacturing.orders o
            JOIN blockchain.users m ON o.manufacturer_id = m.id
            WHERE o.status = 'completed' 
            AND o.created_at >= NOW() - INTERVAL '%s days'
            GROUP BY m.id, m.wallet_address
            ORDER BY orders_completed DESC
            LIMIT 10
        """ % days
        manufacturer_stats = await self._execute_query(manufacturer_stats_query)
        
        analytics = {
            'order_statistics': order_stats or {},
            'component_distribution': component_stats,
            'top_manufacturers': manufacturer_stats
        }
        
        # Cache the analytics
        await self._set_cache(cache_key, analytics, 1800)  # 30 minutes cache
        
        return analytics
