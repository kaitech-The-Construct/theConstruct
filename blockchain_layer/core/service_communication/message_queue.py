"""
Redis Pub/Sub message queue for event-driven architecture
"""
import asyncio
import json
import logging
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import redis.asyncio as redis
import uuid

logger = logging.getLogger(__name__)

class EventType(Enum):
    """Event types for the message queue"""
    # User events
    USER_CREATED = "user.created"
    USER_UPDATED = "user.updated"
    USER_REPUTATION_CHANGED = "user.reputation.changed"
    
    # Asset events
    ASSET_TOKENIZED = "asset.tokenized"
    ASSET_UPDATED = "asset.updated"
    ASSET_TRANSFERRED = "asset.transferred"
    
    # Trading events
    ORDER_CREATED = "order.created"
    ORDER_FILLED = "order.filled"
    ORDER_CANCELLED = "order.cancelled"
    ORDER_PARTIALLY_FILLED = "order.partially_filled"
    
    # Escrow events
    ESCROW_CREATED = "escrow.created"
    ESCROW_RELEASED = "escrow.released"
    ESCROW_EXPIRED = "escrow.expired"
    
    # Manufacturing events
    MANUFACTURING_ORDER_CREATED = "manufacturing.order.created"
    MANUFACTURING_ORDER_ASSIGNED = "manufacturing.order.assigned"
    MILESTONE_COMPLETED = "manufacturing.milestone.completed"
    PAYMENT_RELEASED = "manufacturing.payment.released"
    QUALITY_INSPECTION_COMPLETED = "manufacturing.quality.completed"
    
    # Governance events
    PROPOSAL_CREATED = "governance.proposal.created"
    VOTE_CAST = "governance.vote.cast"
    PROPOSAL_FINALIZED = "governance.proposal.finalized"
    
    # Blockchain events
    TRANSACTION_CONFIRMED = "blockchain.transaction.confirmed"
    TRANSACTION_FAILED = "blockchain.transaction.failed"
    PRICE_UPDATED = "blockchain.price.updated"
    
    # System events
    SERVICE_STARTED = "system.service.started"
    SERVICE_STOPPED = "system.service.stopped"
    ERROR_OCCURRED = "system.error.occurred"

@dataclass
class Event:
    """Base event structure"""
    event_id: str
    event_type: EventType
    source_service: str
    timestamp: datetime
    data: Dict[str, Any]
    correlation_id: Optional[str] = None
    user_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        return {
            'event_id': self.event_id,
            'event_type': self.event_type.value,
            'source_service': self.source_service,
            'timestamp': self.timestamp.isoformat(),
            'data': self.data,
            'correlation_id': self.correlation_id,
            'user_id': self.user_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        """Create event from dictionary"""
        return cls(
            event_id=data['event_id'],
            event_type=EventType(data['event_type']),
            source_service=data['source_service'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            data=data['data'],
            correlation_id=data.get('correlation_id'),
            user_id=data.get('user_id')
        )

class MessageQueue:
    """Redis Pub/Sub message queue manager"""
    
    def __init__(self, redis_config: Dict[str, Any], service_name: str):
        self.redis_config = redis_config
        self.service_name = service_name
        self.redis_client: Optional[redis.Redis] = None
        self.pubsub: Optional[redis.client.PubSub] = None
        self.subscribers: Dict[str, List[Callable]] = {}
        self.running = False
        
    async def initialize(self):
        """Initialize Redis connection and pub/sub"""
        try:
            self.redis_client = redis.Redis(
                host=self.redis_config['host'],
                port=self.redis_config['port'],
                password=self.redis_config.get('password'),
                db=self.redis_config.get('db', 0),
                decode_responses=True
            )
            
            # Test connection
            await self.redis_client.ping()
            
            # Initialize pub/sub
            self.pubsub = self.redis_client.pubsub()
            
            logger.info(f"Message queue initialized for service: {self.service_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize message queue: {e}")
            raise
    
    async def close(self):
        """Close Redis connections"""
        self.running = False
        
        if self.pubsub:
            await self.pubsub.close()
        
        if self.redis_client:
            await self.redis_client.close()
        
        logger.info("Message queue connections closed")
    
    async def publish_event(self, event: Event) -> bool:
        """Publish an event to the message queue"""
        if not self.redis_client:
            raise RuntimeError("Message queue not initialized")
        
        try:
            # Publish to specific event type channel
            channel = f"events.{event.event_type.value}"
            message = json.dumps(event.to_dict())
            
            result = await self.redis_client.publish(channel, message)
            
            # Also publish to general events channel for monitoring
            await self.redis_client.publish("events.all", message)
            
            logger.debug(f"Published event {event.event_id} to channel {channel}")
            return result > 0
            
        except Exception as e:
            logger.error(f"Failed to publish event {event.event_id}: {e}")
            return False
    
    async def subscribe_to_event(self, event_type: EventType, handler: Callable[[Event], None]):
        """Subscribe to a specific event type"""
        channel = f"events.{event_type.value}"
        
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        
        self.subscribers[channel].append(handler)
        
        if self.pubsub:
            await self.pubsub.subscribe(channel)
        
        logger.info(f"Subscribed to event type: {event_type.value}")
    
    async def subscribe_to_pattern(self, pattern: str, handler: Callable[[Event], None]):
        """Subscribe to events matching a pattern"""
        if pattern not in self.subscribers:
            self.subscribers[pattern] = []
        
        self.subscribers[pattern].append(handler)
        
        if self.pubsub:
            await self.pubsub.psubscribe(pattern)
        
        logger.info(f"Subscribed to event pattern: {pattern}")
    
    async def start_listening(self):
        """Start listening for messages"""
        if not self.pubsub:
            raise RuntimeError("Pub/Sub not initialized")
        
        self.running = True
        logger.info("Started listening for messages")
        
        try:
            while self.running:
                message = await self.pubsub.get_message(timeout=1.0)
                
                if message and message['type'] == 'message':
                    await self._handle_message(message)
                elif message and message['type'] == 'pmessage':
                    await self._handle_pattern_message(message)
                
        except Exception as e:
            logger.error(f"Error in message listener: {e}")
        finally:
            logger.info("Stopped listening for messages")
    
    async def _handle_message(self, message: Dict[str, Any]):
        """Handle incoming message"""
        try:
            channel = message['channel']
            data = json.loads(message['data'])
            event = Event.from_dict(data)
            
            # Call all handlers for this channel
            if channel in self.subscribers:
                for handler in self.subscribers[channel]:
                    try:
                        if asyncio.iscoroutinefunction(handler):
                            await handler(event)
                        else:
                            handler(event)
                    except Exception as e:
                        logger.error(f"Error in event handler for {channel}: {e}")
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def _handle_pattern_message(self, message: Dict[str, Any]):
        """Handle incoming pattern message"""
        try:
            pattern = message['pattern']
            data = json.loads(message['data'])
            event = Event.from_dict(data)
            
            # Call all handlers for this pattern
            if pattern in self.subscribers:
                for handler in self.subscribers[pattern]:
                    try:
                        if asyncio.iscoroutinefunction(handler):
                            await handler(event)
                        else:
                            handler(event)
                    except Exception as e:
                        logger.error(f"Error in pattern handler for {pattern}: {e}")
            
        except Exception as e:
            logger.error(f"Error handling pattern message: {e}")
    
    def create_event(self, event_type: EventType, data: Dict[str, Any], 
                    correlation_id: Optional[str] = None, user_id: Optional[str] = None) -> Event:
        """Create a new event"""
        return Event(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            source_service=self.service_name,
            timestamp=datetime.utcnow(),
            data=data,
            correlation_id=correlation_id,
            user_id=user_id
        )

class EventBus:
    """High-level event bus for service communication"""
    
    def __init__(self, message_queue: MessageQueue):
        self.message_queue = message_queue
        self.event_handlers: Dict[EventType, List[Callable]] = {}
    
    async def emit(self, event_type: EventType, data: Dict[str, Any], 
                  correlation_id: Optional[str] = None, user_id: Optional[str] = None) -> bool:
        """Emit an event"""
        event = self.message_queue.create_event(event_type, data, correlation_id, user_id)
        return await self.message_queue.publish_event(event)
    
    async def on(self, event_type: EventType, handler: Callable[[Event], None]):
        """Register event handler"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
            await self.message_queue.subscribe_to_event(event_type, self._dispatch_event)
        
        self.event_handlers[event_type].append(handler)
        logger.info(f"Registered handler for event type: {event_type.value}")
    
    async def _dispatch_event(self, event: Event):
        """Dispatch event to registered handlers"""
        if event.event_type in self.event_handlers:
            for handler in self.event_handlers[event.event_type]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event)
                    else:
                        handler(event)
                except Exception as e:
                    logger.error(f"Error in event handler for {event.event_type.value}: {e}")

class CircuitBreaker:
    """Circuit breaker for service communication resilience"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = "closed"  # closed, open, half_open
    
    async def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == "open":
            if self._should_attempt_reset():
                self.state = "half_open"
            else:
                raise Exception("Circuit breaker is open")
        
        try:
            result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit breaker should attempt reset"""
        if not self.last_failure_time:
            return True
        
        return (datetime.utcnow() - self.last_failure_time).seconds >= self.recovery_timeout
    
    def _on_success(self):
        """Handle successful operation"""
        self.failure_count = 0
        self.state = "closed"
    
    def _on_failure(self):
        """Handle failed operation"""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
            logger.warning(f"Circuit breaker opened after {self.failure_count} failures")

class RetryPolicy:
    """Retry policy for failed service calls"""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    async def execute(self, func: Callable, *args, **kwargs):
        """Execute function with retry policy"""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                    logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {e}")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"All {self.max_retries + 1} attempts failed")
        
        raise last_exception

class ServiceCommunicationManager:
    """Manages all service communication including HTTP and messaging"""
    
    def __init__(self, service_name: str, redis_config: Dict[str, Any]):
        self.service_name = service_name
        self.message_queue = MessageQueue(redis_config, service_name)
        self.event_bus = EventBus(self.message_queue)
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.retry_policies: Dict[str, RetryPolicy] = {}
        
    async def initialize(self):
        """Initialize communication manager"""
        await self.message_queue.initialize()
        logger.info(f"Service communication manager initialized for: {self.service_name}")
    
    async def close(self):
        """Close communication manager"""
        await self.message_queue.close()
        logger.info("Service communication manager closed")
    
    def get_circuit_breaker(self, service_name: str) -> CircuitBreaker:
        """Get or create circuit breaker for a service"""
        if service_name not in self.circuit_breakers:
            self.circuit_breakers[service_name] = CircuitBreaker()
        return self.circuit_breakers[service_name]
    
    def get_retry_policy(self, service_name: str) -> RetryPolicy:
        """Get or create retry policy for a service"""
        if service_name not in self.retry_policies:
            self.retry_policies[service_name] = RetryPolicy()
        return self.retry_policies[service_name]
    
    async def emit_event(self, event_type: EventType, data: Dict[str, Any], 
                        correlation_id: Optional[str] = None, user_id: Optional[str] = None) -> bool:
        """Emit an event to the message queue"""
        return await self.event_bus.emit(event_type, data, correlation_id, user_id)
    
    async def subscribe_to_event(self, event_type: EventType, handler: Callable[[Event], None]):
        """Subscribe to an event type"""
        await self.event_bus.on(event_type, handler)
    
    async def start_event_listener(self):
        """Start listening for events"""
        await self.message_queue.start_listening()

# Event handler decorators
def event_handler(event_type: EventType):
    """Decorator for event handlers"""
    def decorator(func):
        func._event_type = event_type
        func._is_event_handler = True
        return func
    return decorator

def async_event_handler(event_type: EventType):
    """Decorator for async event handlers"""
    def decorator(func):
        func._event_type = event_type
        func._is_event_handler = True
        func._is_async = True
        return func
    return decorator

class EventHandlerRegistry:
    """Registry for automatic event handler discovery"""
    
    def __init__(self, communication_manager: ServiceCommunicationManager):
        self.communication_manager = communication_manager
        self.registered_handlers: List[Callable] = []
    
    async def register_handlers_from_module(self, module):
        """Register all event handlers from a module"""
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            
            if hasattr(attr, '_is_event_handler') and attr._is_event_handler:
                event_type = attr._event_type
                await self.communication_manager.subscribe_to_event(event_type, attr)
                self.registered_handlers.append(attr)
                logger.info(f"Registered event handler: {attr_name} for {event_type.value}")
    
    async def register_handler(self, event_type: EventType, handler: Callable[[Event], None]):
        """Register a single event handler"""
        await self.communication_manager.subscribe_to_event(event_type, handler)
        self.registered_handlers.append(handler)
        logger.info(f"Registered event handler for {event_type.value}")

# Utility functions for common event patterns
async def emit_user_event(comm_manager: ServiceCommunicationManager, event_type: EventType, 
                         user_id: str, user_data: Dict[str, Any], correlation_id: Optional[str] = None):
    """Emit a user-related event"""
    await comm_manager.emit_event(
        event_type=event_type,
        data={
            'user_id': user_id,
            'user_data': user_data
        },
        correlation_id=correlation_id,
        user_id=user_id
    )

async def emit_trading_event(comm_manager: ServiceCommunicationManager, event_type: EventType,
                           order_data: Dict[str, Any], correlation_id: Optional[str] = None):
    """Emit a trading-related event"""
    await comm_manager.emit_event(
        event_type=event_type,
        data={
            'order_data': order_data,
            'timestamp': datetime.utcnow().isoformat()
        },
        correlation_id=correlation_id,
        user_id=order_data.get('user_id')
    )

async def emit_manufacturing_event(comm_manager: ServiceCommunicationManager, event_type: EventType,
                                 order_data: Dict[str, Any], milestone_data: Optional[Dict[str, Any]] = None,
                                 correlation_id: Optional[str] = None):
    """Emit a manufacturing-related event"""
    event_data = {
        'order_data': order_data,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if milestone_data:
        event_data['milestone_data'] = milestone_data
    
    await comm_manager.emit_event(
        event_type=event_type,
        data=event_data,
        correlation_id=correlation_id,
        user_id=order_data.get('customer_id')
    )

async def emit_blockchain_event(comm_manager: ServiceCommunicationManager, event_type: EventType,
                              transaction_data: Dict[str, Any], correlation_id: Optional[str] = None):
    """Emit a blockchain-related event"""
    await comm_manager.emit_event(
        event_type=event_type,
        data={
            'transaction_data': transaction_data,
            'timestamp': datetime.utcnow().isoformat()
        },
        correlation_id=correlation_id,
        user_id=transaction_data.get('from_address')
    )
