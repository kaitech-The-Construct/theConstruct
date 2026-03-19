"""
Event handlers for the data storage service
"""
import logging
from typing import Dict, Any
from uuid import UUID

# Import communication framework components
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'service_communication'))

from service_communication import (
    Event, EventType, event_handler, async_event_handler,
    emit_user_event, emit_trading_event, emit_manufacturing_event, emit_blockchain_event
)

from repositories import (
    UserRepository, AssetRepository, TradingRepository,
    ManufacturingRepository, GovernanceRepository, BlockchainRepository
)
from database import db_manager

logger = logging.getLogger(__name__)

class DataStorageEventHandlers:
    """Event handlers for data storage service"""
    
    def __init__(self):
        self.user_repo = UserRepository(db_manager)
        self.asset_repo = AssetRepository(db_manager)
        self.trading_repo = TradingRepository(db_manager)
        self.manufacturing_repo = ManufacturingRepository(db_manager)
        self.governance_repo = GovernanceRepository(db_manager)
        self.blockchain_repo = BlockchainRepository(db_manager)
    
    @async_event_handler(EventType.USER_CREATED)
    async def handle_user_created(self, event: Event):
        """Handle user created event"""
        try:
            user_data = event.data.get('user_data', {})
            
            # Create user in database if not exists
            existing_user = await self.user_repo.get_by_wallet_address(
                user_data.get('wallet_address')
            )
            
            if not existing_user:
                created_user = await self.user_repo.create(user_data)
                logger.info(f"Created user in database: {created_user['id']}")
            else:
                logger.info(f"User already exists: {existing_user['id']}")
            
        except Exception as e:
            logger.error(f"Error handling user created event: {e}")
    
    @async_event_handler(EventType.ASSET_TOKENIZED)
    async def handle_asset_tokenized(self, event: Event):
        """Handle asset tokenized event"""
        try:
            asset_data = event.data.get('asset_data', {})
            
            # Create or update asset in database
            existing_asset = await self.asset_repo.get_by_asset_id(
                asset_data.get('asset_id')
            )
            
            if not existing_asset:
                created_asset = await self.asset_repo.create(asset_data)
                logger.info(f"Created asset in database: {created_asset['id']}")
            else:
                # Update with transaction hash and status
                updated_asset = await self.asset_repo.update(
                    existing_asset['id'],
                    {
                        'transaction_hash': asset_data.get('transaction_hash'),
                        'status': 'active'
                    }
                )
                logger.info(f"Updated asset in database: {updated_asset['id']}")
            
        except Exception as e:
            logger.error(f"Error handling asset tokenized event: {e}")
    
    @async_event_handler(EventType.ORDER_CREATED)
    async def handle_order_created(self, event: Event):
        """Handle trading order created event"""
        try:
            order_data = event.data.get('order_data', {})
            
            # Create order in database
            created_order = await self.trading_repo.create_order(order_data)
            logger.info(f"Created order in database: {created_order['id']}")
            
            # Update asset trading statistics cache invalidation
            asset_id = order_data.get('asset_id')
            if asset_id:
                # This will trigger cache invalidation for asset trading stats
                await self.asset_repo.get_asset_trading_stats(UUID(asset_id))
            
        except Exception as e:
            logger.error(f"Error handling order created event: {e}")
    
    @async_event_handler(EventType.ORDER_FILLED)
    async def handle_order_filled(self, event: Event):
        """Handle order filled event"""
        try:
            order_data = event.data.get('order_data', {})
            
            # Update order status in database
            order_id = order_data.get('id')
            if order_id:
                updated_order = await self.trading_repo.update_order(
                    UUID(order_id),
                    {
                        'status': 'filled',
                        'filled_amount': order_data.get('amount'),
                        'transaction_hash': order_data.get('transaction_hash')
                    }
                )
                logger.info(f"Updated order status to filled: {updated_order['id']}")
                
                # Update user reputation for successful trade
                user_id = order_data.get('user_id')
                if user_id:
                    await self.user_repo.update_reputation(UUID(user_id), 2)  # +2 reputation for filled order
            
        except Exception as e:
            logger.error(f"Error handling order filled event: {e}")
    
    @async_event_handler(EventType.MANUFACTURING_ORDER_CREATED)
    async def handle_manufacturing_order_created(self, event: Event):
        """Handle manufacturing order created event"""
        try:
            order_data = event.data.get('order_data', {})
            
            # Create manufacturing order in database
            created_order = await self.manufacturing_repo.create_order(order_data)
            logger.info(f"Created manufacturing order in database: {created_order['id']}")
            
            # Create default milestones if provided
            milestones = order_data.get('milestones', [])
            for i, milestone in enumerate(milestones):
                milestone_data = {
                    'order_id': created_order['id'],
                    'milestone_number': i + 1,
                    'description': milestone.get('description', f'Milestone {i + 1}'),
                    'payment_percentage': milestone.get('payment_percentage', 25.0)
                }
                await self.manufacturing_repo.create_milestone(milestone_data)
            
        except Exception as e:
            logger.error(f"Error handling manufacturing order created event: {e}")
    
    @async_event_handler(EventType.MILESTONE_COMPLETED)
    async def handle_milestone_completed(self, event: Event):
        """Handle manufacturing milestone completed event"""
        try:
            milestone_data = event.data.get('milestone_data', {})
            
            # Update milestone status in database
            milestone_id = milestone_data.get('id')
            transaction_hash = milestone_data.get('transaction_hash')
            
            if milestone_id:
                updated_milestone = await self.manufacturing_repo.complete_milestone(
                    UUID(milestone_id), transaction_hash
                )
                logger.info(f"Completed milestone in database: {updated_milestone['id']}")
                
                # Update manufacturer reputation
                order_data = event.data.get('order_data', {})
                manufacturer_id = order_data.get('manufacturer_id')
                if manufacturer_id:
                    await self.user_repo.update_reputation(UUID(manufacturer_id), 3)  # +3 reputation for milestone completion
            
        except Exception as e:
            logger.error(f"Error handling milestone completed event: {e}")
    
    @async_event_handler(EventType.TRANSACTION_CONFIRMED)
    async def handle_transaction_confirmed(self, event: Event):
        """Handle blockchain transaction confirmed event"""
        try:
            tx_data = event.data.get('transaction_data', {})
            
            # Update transaction status in database
            transaction_hash = tx_data.get('transaction_hash')
            if transaction_hash:
                updated_tx = await self.blockchain_repo.update_transaction_status(
                    transaction_hash,
                    'confirmed',
                    tx_data.get('block_number'),
                    tx_data.get('block_hash')
                )
                logger.info(f"Updated transaction status to confirmed: {transaction_hash}")
            
        except Exception as e:
            logger.error(f"Error handling transaction confirmed event: {e}")
    
    @async_event_handler(EventType.PRICE_UPDATED)
    async def handle_price_updated(self, event: Event):
        """Handle price feed updated event"""
        try:
            price_data = event.data.get('price_data', {})
            
            # Create price feed entry in database
            created_price = await self.blockchain_repo.create_price_feed(price_data)
            logger.info(f"Created price feed entry: {created_price['id']}")
            
        except Exception as e:
            logger.error(f"Error handling price updated event: {e}")
    
    @async_event_handler(EventType.PROPOSAL_CREATED)
    async def handle_proposal_created(self, event: Event):
        """Handle governance proposal created event"""
        try:
            proposal_data = event.data.get('proposal_data', {})
            
            # Create proposal in database
            created_proposal = await self.governance_repo.create_proposal(proposal_data)
            logger.info(f"Created proposal in database: {created_proposal['id']}")
            
        except Exception as e:
            logger.error(f"Error handling proposal created event: {e}")
    
    @async_event_handler(EventType.VOTE_CAST)
    async def handle_vote_cast(self, event: Event):
        """Handle governance vote cast event"""
        try:
            vote_data = event.data.get('vote_data', {})
            
            # Record vote in database
            cast_vote = await self.governance_repo.cast_vote(vote_data)
            logger.info(f"Recorded vote in database: {cast_vote['id']}")
            
            # Update voter reputation
            voter_id = vote_data.get('voter_id')
            if voter_id:
                await self.user_repo.update_reputation(UUID(voter_id), 1)  # +1 reputation for voting
            
        except Exception as e:
            logger.error(f"Error handling vote cast event: {e}")
    
    @async_event_handler(EventType.QUALITY_INSPECTION_COMPLETED)
    async def handle_quality_inspection_completed(self, event: Event):
        """Handle quality inspection completed event"""
        try:
            qa_data = event.data.get('qa_data', {})
            
            # Create quality assurance record
            created_qa = await self.manufacturing_repo.create_quality_record(qa_data)
            logger.info(f"Created QA record in database: {created_qa['id']}")
            
            # Update inspector reputation
            inspector_id = qa_data.get('inspector_id')
            if inspector_id:
                reputation_delta = 2 if qa_data.get('passed') else 1
                await self.user_repo.update_reputation(UUID(inspector_id), reputation_delta)
            
        except Exception as e:
            logger.error(f"Error handling quality inspection completed event: {e}")
    
    @async_event_handler(EventType.ERROR_OCCURRED)
    async def handle_error_occurred(self, event: Event):
        """Handle system error event"""
        try:
            error_data = event.data
            
            # Log error for monitoring
            logger.error(f"System error occurred: {error_data}")
            
            # Could implement error tracking, alerting, etc.
            # For now, just log the error
            
        except Exception as e:
            logger.error(f"Error handling error occurred event: {e}")

# Utility functions for data storage service events
async def emit_data_storage_events(communication_manager, operation_type: str, 
                                 entity_type: str, entity_data: Dict[str, Any],
                                 correlation_id: str = None):
    """Emit events for data storage operations"""
    
    event_mapping = {
        ('create', 'user'): EventType.USER_CREATED,
        ('update', 'user'): EventType.USER_UPDATED,
        ('create', 'asset'): EventType.ASSET_TOKENIZED,
        ('update', 'asset'): EventType.ASSET_UPDATED,
        ('create', 'order'): EventType.ORDER_CREATED,
        ('update', 'order'): EventType.ORDER_FILLED,
        ('create', 'manufacturing_order'): EventType.MANUFACTURING_ORDER_CREATED,
        ('create', 'proposal'): EventType.PROPOSAL_CREATED,
        ('create', 'vote'): EventType.VOTE_CAST,
        ('create', 'transaction'): EventType.TRANSACTION_CONFIRMED,
        ('create', 'price_feed'): EventType.PRICE_UPDATED
    }
    
    event_type = event_mapping.get((operation_type, entity_type))
    if event_type:
        await communication_manager.emit_event(
            event_type,
            {f'{entity_type}_data': entity_data},
            correlation_id=correlation_id,
            user_id=entity_data.get('user_id') or entity_data.get('customer_id')
        )

# Integration helpers
class DataStorageServiceIntegration:
    """Integration layer for data storage service with communication framework"""
    
    def __init__(self, communication_framework):
        self.framework = communication_framework
        self.event_handlers = DataStorageEventHandlers()
    
    async def initialize(self):
        """Initialize event handlers"""
        await self.framework.register_event_handlers(self.event_handlers)
        logger.info("Data storage service event handlers registered")
    
    async def emit_repository_event(self, operation: str, entity_type: str, 
                                  entity_data: Dict[str, Any], correlation_id: str = None):
        """Emit event for repository operations"""
        await emit_data_storage_events(
            self.framework.communication_manager,
            operation, entity_type, entity_data, correlation_id
        )
    
    # Convenience methods for common operations
    async def notify_user_created(self, user_data: Dict[str, Any], correlation_id: str = None):
        """Notify that a user was created"""
        await self.emit_repository_event('create', 'user', user_data, correlation_id)
    
    async def notify_order_created(self, order_data: Dict[str, Any], correlation_id: str = None):
        """Notify that an order was created"""
        await self.emit_repository_event('create', 'order', order_data, correlation_id)
    
    async def notify_order_filled(self, order_data: Dict[str, Any], correlation_id: str = None):
        """Notify that an order was filled"""
        await self.emit_repository_event('update', 'order', order_data, correlation_id)
    
    async def notify_manufacturing_order_created(self, order_data: Dict[str, Any], correlation_id: str = None):
        """Notify that a manufacturing order was created"""
        await self.emit_repository_event('create', 'manufacturing_order', order_data, correlation_id)
    
    async def notify_milestone_completed(self, milestone_data: Dict[str, Any], 
                                       order_data: Dict[str, Any], correlation_id: str = None):
        """Notify that a milestone was completed"""
        await self.framework.emit_event(
            EventType.MILESTONE_COMPLETED,
            {
                'milestone_data': milestone_data,
                'order_data': order_data
            },
            correlation_id=correlation_id,
            user_id=order_data.get('manufacturer_id')
        )
    
    async def notify_transaction_confirmed(self, transaction_data: Dict[str, Any], correlation_id: str = None):
        """Notify that a transaction was confirmed"""
        await self.emit_repository_event('create', 'transaction', transaction_data, correlation_id)
    
    async def notify_price_updated(self, price_data: Dict[str, Any], correlation_id: str = None):
        """Notify that a price was updated"""
        await self.emit_repository_event('create', 'price_feed', price_data, correlation_id)

# Service communication middleware for FastAPI
class ServiceCommunicationMiddleware:
    """Middleware to add service communication to FastAPI requests"""
    
    def __init__(self, communication_framework):
        self.framework = communication_framework
    
    async def __call__(self, request, call_next):
        """Process request with communication context"""
        # Add correlation ID to request if not present
        correlation_id = request.headers.get('X-Correlation-ID')
        if not correlation_id:
            correlation_id = self.framework.create_correlation_id()
            request.state.correlation_id = correlation_id
        
        # Add communication framework to request state
        request.state.communication_framework = self.framework
        
        # Process request
        response = await call_next(request)
        
        # Add correlation ID to response headers
        response.headers['X-Correlation-ID'] = correlation_id
        
        return response

# Health check integration
async def check_communication_health(communication_framework) -> Dict[str, Any]:
    """Check health of communication components"""
    health_status = {
        'service_mesh': False,
        'message_queue': False,
        'service_discovery': False,
        'overall': False
    }
    
    try:
        # Check service mesh health
        mesh_health = await communication_framework.get_service_mesh_health()
        health_status['service_mesh'] = len(mesh_health) > 0
        
        # Check message queue (Redis) health
        try:
            redis_client = await communication_framework.communication_manager.message_queue.redis_client
            if redis_client:
                await redis_client.ping()
                health_status['message_queue'] = True
        except Exception:
            health_status['message_queue'] = False
        
        # Check service discovery
        try:
            services = await communication_framework.discover_services()
            health_status['service_discovery'] = len(services) > 0
        except Exception:
            health_status['service_discovery'] = False
        
        health_status['overall'] = all([
            health_status['service_mesh'],
            health_status['message_queue'],
            health_status['service_discovery']
        ])
        
    except Exception as e:
        logger.error(f"Communication health check failed: {e}")
    
    return health_status
