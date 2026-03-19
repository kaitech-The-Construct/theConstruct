"""
Integrated service communication framework for The Construct blockchain layer
"""
import asyncio
import logging
from typing import Dict, Any, Optional, List, Callable
from contextlib import asynccontextmanager
import os

from .service_client import ServiceClient, ServiceRegistry, ServiceType
from .message_queue import (
    MessageQueue, EventBus, ServiceCommunicationManager, 
    EventType, Event, EventHandlerRegistry
)
from .service_discovery import ServiceMesh, ServiceInfo, create_service_info

logger = logging.getLogger(__name__)

class CommunicationFramework:
    """Unified communication framework for services"""
    
    def __init__(self, service_name: str, service_type: str, port: int):
        self.service_name = service_name
        self.service_type = service_type
        self.port = port
        
        # Redis configuration
        self.redis_config = {
            'host': os.getenv('REDIS_HOST', 'localhost'),
            'port': int(os.getenv('REDIS_PORT', 6379)),
            'password': os.getenv('REDIS_PASSWORD', None),
            'db': int(os.getenv('REDIS_DB', 0))
        }
        
        # Initialize components
        self.service_registry = ServiceRegistry()
        self.service_client = ServiceClient(self.service_registry)
        self.communication_manager = ServiceCommunicationManager(service_name, self.redis_config)
        self.service_mesh = ServiceMesh(service_name, service_type, self.redis_config)
        self.event_handler_registry = EventHandlerRegistry(self.communication_manager)
        
        # Event listener task
        self.event_listener_task: Optional[asyncio.Task] = None
        
    async def initialize(self):
        """Initialize the communication framework"""
        try:
            # Initialize service mesh (includes service discovery)
            await self.service_mesh.initialize()
            
            # Initialize communication manager (includes message queue)
            await self.communication_manager.initialize()
            
            # Start event listener
            self.event_listener_task = asyncio.create_task(
                self.communication_manager.start_event_listener()
            )
            
            logger.info(f"Communication framework initialized for: {self.service_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize communication framework: {e}")
            raise
    
    async def close(self):
        """Close the communication framework"""
        try:
            # Stop event listener
            if self.event_listener_task:
                self.event_listener_task.cancel()
                try:
                    await self.event_listener_task
                except asyncio.CancelledError:
                    pass
            
            # Close components
            await self.communication_manager.close()
            await self.service_mesh.close()
            await self.service_client.__aexit__(None, None, None)
            
            logger.info("Communication framework closed")
            
        except Exception as e:
            logger.error(f"Error closing communication framework: {e}")
    
    # HTTP Communication Methods
    async def call_service(self, service_type: ServiceType, method: str, path: str, 
                          data: Optional[Dict[str, Any]] = None, 
                          params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make HTTP call to a service"""
        async with self.service_client as client:
            if method.upper() == "GET":
                return await client.get(service_type, path, params)
            elif method.upper() == "POST":
                return await client.post(service_type, path, data)
            elif method.upper() == "PUT":
                return await client.put(service_type, path, data)
            elif method.upper() == "DELETE":
                return await client.delete(service_type, path)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
    
    async def health_check_service(self, service_type: ServiceType) -> Dict[str, Any]:
        """Check health of a specific service"""
        async with self.service_client as client:
            return await client.health_check(service_type)
    
    async def health_check_all_services(self) -> Dict[ServiceType, Dict[str, Any]]:
        """Check health of all services"""
        async with self.service_client as client:
            return await client.health_check_all()
    
    # Event-Driven Communication Methods
    async def emit_event(self, event_type: EventType, data: Dict[str, Any], 
                        correlation_id: Optional[str] = None, user_id: Optional[str] = None) -> bool:
        """Emit an event to the message queue"""
        return await self.communication_manager.emit_event(event_type, data, correlation_id, user_id)
    
    async def subscribe_to_event(self, event_type: EventType, handler: Callable[[Event], None]):
        """Subscribe to an event type"""
        await self.communication_manager.subscribe_to_event(event_type, handler)
    
    async def register_event_handlers(self, handlers_module):
        """Register event handlers from a module"""
        await self.event_handler_registry.register_handlers_from_module(handlers_module)
    
    # Service Discovery Methods
    async def discover_services(self, service_type: Optional[str] = None) -> List[ServiceInfo]:
        """Discover available services"""
        return await self.service_mesh.service_discovery.discover_services(service_type)
    
    async def get_service_by_type(self, service_type: str, strategy: str = "round_robin") -> Optional[ServiceInfo]:
        """Get a service instance using load balancing"""
        return await self.service_mesh.discover_service(service_type, strategy)
    
    async def get_service_mesh_health(self) -> Dict[str, Any]:
        """Get health status of the service mesh"""
        return await self.service_mesh.get_service_health()
    
    # Utility Methods
    def create_correlation_id(self) -> str:
        """Create a new correlation ID for request tracing"""
        import uuid
        return str(uuid.uuid4())
    
    async def wait_for_service(self, service_type: str, timeout: int = 60) -> Optional[ServiceInfo]:
        """Wait for a service to become available"""
        from .service_discovery import wait_for_service
        return await wait_for_service(self.service_mesh.service_discovery, service_type, timeout)

# High-level service communication patterns
class ServiceOrchestrator:
    """Orchestrates complex workflows across multiple services"""
    
    def __init__(self, communication_framework: CommunicationFramework):
        self.framework = communication_framework
        self.active_workflows: Dict[str, Dict[str, Any]] = {}
    
    async def start_workflow(self, workflow_id: str, workflow_type: str, 
                           initial_data: Dict[str, Any]) -> str:
        """Start a new workflow"""
        correlation_id = self.framework.create_correlation_id()
        
        self.active_workflows[workflow_id] = {
            'workflow_id': workflow_id,
            'workflow_type': workflow_type,
            'correlation_id': correlation_id,
            'status': 'started',
            'steps': [],
            'data': initial_data,
            'started_at': datetime.utcnow().isoformat()
        }
        
        # Emit workflow started event
        await self.framework.emit_event(
            EventType.SERVICE_STARTED,
            {
                'workflow_id': workflow_id,
                'workflow_type': workflow_type,
                'initial_data': initial_data
            },
            correlation_id=correlation_id
        )
        
        return correlation_id
    
    async def add_workflow_step(self, workflow_id: str, step_name: str, 
                              step_data: Dict[str, Any], status: str = 'completed'):
        """Add a step to an active workflow"""
        if workflow_id in self.active_workflows:
            self.active_workflows[workflow_id]['steps'].append({
                'step_name': step_name,
                'step_data': step_data,
                'status': status,
                'timestamp': datetime.utcnow().isoformat()
            })
    
    async def complete_workflow(self, workflow_id: str, final_data: Dict[str, Any]):
        """Complete a workflow"""
        if workflow_id in self.active_workflows:
            workflow = self.active_workflows[workflow_id]
            workflow['status'] = 'completed'
            workflow['completed_at'] = datetime.utcnow().isoformat()
            workflow['final_data'] = final_data
            
            # Emit workflow completed event
            await self.framework.emit_event(
                EventType.SERVICE_STOPPED,
                {
                    'workflow_id': workflow_id,
                    'workflow_type': workflow['workflow_type'],
                    'final_data': final_data
                },
                correlation_id=workflow['correlation_id']
            )
    
    async def fail_workflow(self, workflow_id: str, error: str):
        """Mark a workflow as failed"""
        if workflow_id in self.active_workflows:
            workflow = self.active_workflows[workflow_id]
            workflow['status'] = 'failed'
            workflow['failed_at'] = datetime.utcnow().isoformat()
            workflow['error'] = error
            
            # Emit workflow failed event
            await self.framework.emit_event(
                EventType.ERROR_OCCURRED,
                {
                    'workflow_id': workflow_id,
                    'workflow_type': workflow['workflow_type'],
                    'error': error
                },
                correlation_id=workflow['correlation_id']
            )

# Common workflow patterns
class TradingWorkflow:
    """Workflow for trading operations"""
    
    def __init__(self, orchestrator: ServiceOrchestrator):
        self.orchestrator = orchestrator
    
    async def execute_order_workflow(self, order_data: Dict[str, Any]) -> str:
        """Execute complete order workflow"""
        workflow_id = f"order_{order_data['order_id']}"
        correlation_id = await self.orchestrator.start_workflow(
            workflow_id, "trading_order", order_data
        )
        
        try:
            # Step 1: Validate order
            await self.orchestrator.framework.call_service(
                ServiceType.DATA_STORAGE, "POST", "/api/trading/validate", order_data
            )
            await self.orchestrator.add_workflow_step(workflow_id, "validate_order", order_data)
            
            # Step 2: Create order in database
            created_order = await self.orchestrator.framework.call_service(
                ServiceType.DATA_STORAGE, "POST", "/api/trading/orders", order_data
            )
            await self.orchestrator.add_workflow_step(workflow_id, "create_order", created_order)
            
            # Step 3: Submit to XRPL
            xrpl_result = await self.orchestrator.framework.call_service(
                ServiceType.XRPL_SERVICE, "POST", "/api/orders", order_data
            )
            await self.orchestrator.add_workflow_step(workflow_id, "submit_to_xrpl", xrpl_result)
            
            # Step 4: Send notifications
            await self.orchestrator.framework.call_service(
                ServiceType.NOTIFICATIONS, "POST", "/api/notify", {
                    "user_id": order_data["user_id"],
                    "message": f"Order {order_data['order_id']} created successfully",
                    "type": "order_created"
                }
            )
            await self.orchestrator.add_workflow_step(workflow_id, "send_notification", {})
            
            await self.orchestrator.complete_workflow(workflow_id, {"order_id": order_data["order_id"]})
            return correlation_id
            
        except Exception as e:
            await self.orchestrator.fail_workflow(workflow_id, str(e))
            raise

class ManufacturingWorkflow:
    """Workflow for manufacturing operations"""
    
    def __init__(self, orchestrator: ServiceOrchestrator):
        self.orchestrator = orchestrator
    
    async def execute_manufacturing_order_workflow(self, order_data: Dict[str, Any]) -> str:
        """Execute complete manufacturing order workflow"""
        workflow_id = f"mfg_order_{order_data['order_id']}"
        correlation_id = await self.orchestrator.start_workflow(
            workflow_id, "manufacturing_order", order_data
        )
        
        try:
            # Step 1: Create manufacturing order
            created_order = await self.orchestrator.framework.call_service(
                ServiceType.DATA_STORAGE, "POST", "/api/manufacturing/orders", order_data
            )
            await self.orchestrator.add_workflow_step(workflow_id, "create_order", created_order)
            
            # Step 2: Create escrow for payment
            escrow_data = {
                "creator_id": order_data["customer_id"],
                "destination_address": order_data.get("manufacturer_wallet"),
                "amount": order_data["max_price"],
                "condition_hash": f"manufacturing_order_{order_data['order_id']}"
            }
            
            escrow_result = await self.orchestrator.framework.call_service(
                ServiceType.XRPL_SERVICE, "POST", "/api/escrow", escrow_data
            )
            await self.orchestrator.add_workflow_step(workflow_id, "create_escrow", escrow_result)
            
            # Step 3: Create milestones
            milestones = order_data.get("milestones", [])
            for milestone in milestones:
                milestone["order_id"] = created_order["id"]
                milestone_result = await self.orchestrator.framework.call_service(
                    ServiceType.DATA_STORAGE, "POST", "/api/manufacturing/milestones", milestone
                )
            await self.orchestrator.add_workflow_step(workflow_id, "create_milestones", {"count": len(milestones)})
            
            # Step 4: Notify relevant parties
            await self.orchestrator.framework.call_service(
                ServiceType.NOTIFICATIONS, "POST", "/api/notify", {
                    "user_id": order_data["customer_id"],
                    "message": f"Manufacturing order {order_data['order_id']} created",
                    "type": "manufacturing_order_created"
                }
            )
            
            await self.orchestrator.complete_workflow(workflow_id, {"order_id": order_data["order_id"]})
            return correlation_id
            
        except Exception as e:
            await self.orchestrator.fail_workflow(workflow_id, str(e))
            raise

# Event-driven service integration
class ServiceEventHandlers:
    """Common event handlers for service integration"""
    
    def __init__(self, communication_framework: CommunicationFramework):
        self.framework = communication_framework
    
    async def handle_user_created(self, event: Event):
        """Handle user created event"""
        user_data = event.data.get('user_data', {})
        
        # Update reputation system
        await self.framework.emit_event(
            EventType.USER_REPUTATION_CHANGED,
            {
                'user_id': event.user_id,
                'old_score': 0,
                'new_score': user_data.get('reputation_score', 0),
                'reason': 'user_created'
            },
            correlation_id=event.correlation_id
        )
        
        logger.info(f"Processed user created event for user: {event.user_id}")
    
    async def handle_order_filled(self, event: Event):
        """Handle order filled event"""
        order_data = event.data.get('order_data', {})
        
        # Update user reputation for successful trade
        await self.framework.emit_event(
            EventType.USER_REPUTATION_CHANGED,
            {
                'user_id': order_data.get('user_id'),
                'reputation_delta': 1,
                'reason': 'successful_trade'
            },
            correlation_id=event.correlation_id
        )
        
        # Send notification
        try:
            await self.framework.call_service(
                ServiceType.NOTIFICATIONS, "POST", "/api/notify", {
                    "user_id": order_data.get('user_id'),
                    "message": f"Order {order_data.get('order_id')} has been filled",
                    "type": "order_filled"
                }
            )
        except Exception as e:
            logger.error(f"Failed to send order filled notification: {e}")
        
        logger.info(f"Processed order filled event for order: {order_data.get('order_id')}")
    
    async def handle_milestone_completed(self, event: Event):
        """Handle manufacturing milestone completed event"""
        milestone_data = event.data.get('milestone_data', {})
        order_data = event.data.get('order_data', {})
        
        # Release payment for milestone
        try:
            payment_data = {
                'order_id': order_data.get('order_id'),
                'milestone_id': milestone_data.get('id'),
                'amount': milestone_data.get('payment_amount'),
                'recipient': order_data.get('manufacturer_wallet')
            }
            
            payment_result = await self.framework.call_service(
                ServiceType.XRPL_SERVICE, "POST", "/api/payments/release", payment_data
            )
            
            # Emit payment released event
            await self.framework.emit_event(
                EventType.PAYMENT_RELEASED,
                {
                    'order_data': order_data,
                    'milestone_data': milestone_data,
                    'payment_result': payment_result
                },
                correlation_id=event.correlation_id
            )
            
        except Exception as e:
            logger.error(f"Failed to release payment for milestone: {e}")
            await self.framework.emit_event(
                EventType.ERROR_OCCURRED,
                {
                    'error': str(e),
                    'context': 'milestone_payment_release',
                    'order_id': order_data.get('order_id'),
                    'milestone_id': milestone_data.get('id')
                },
                correlation_id=event.correlation_id
            )
        
        logger.info(f"Processed milestone completed event for order: {order_data.get('order_id')}")
    
    async def handle_transaction_confirmed(self, event: Event):
        """Handle blockchain transaction confirmed event"""
        tx_data = event.data.get('transaction_data', {})
        
        # Update transaction status in database
        try:
            await self.framework.call_service(
                ServiceType.DATA_STORAGE, "PUT", 
                f"/api/blockchain/transactions/{tx_data.get('transaction_hash')}", 
                {'status': 'confirmed'}
            )
        except Exception as e:
            logger.error(f"Failed to update transaction status: {e}")
        
        # Send confirmation notification
        if tx_data.get('from_address'):
            try:
                await self.framework.call_service(
                    ServiceType.NOTIFICATIONS, "POST", "/api/notify", {
                        "wallet_address": tx_data.get('from_address'),
                        "message": f"Transaction {tx_data.get('transaction_hash')} confirmed",
                        "type": "transaction_confirmed"
                    }
                )
            except Exception as e:
                logger.error(f"Failed to send transaction confirmation notification: {e}")
        
        logger.info(f"Processed transaction confirmed event: {tx_data.get('transaction_hash')}")

# Factory function for creating communication framework
def create_communication_framework(service_name: str, service_type: str, port: int) -> CommunicationFramework:
    """Factory function to create communication framework"""
    return CommunicationFramework(service_name, service_type, port)

# Context manager for framework lifecycle
@asynccontextmanager
async def communication_context(service_name: str, service_type: str, port: int):
    """Context manager for communication framework lifecycle"""
    framework = create_communication_framework(service_name, service_type, port)
    
    try:
        await framework.initialize()
        yield framework
    finally:
        await framework.close()

# Decorator for automatic event handler registration
def auto_register_handlers(framework: CommunicationFramework):
    """Decorator to automatically register event handlers"""
    def decorator(cls):
        original_init = cls.__init__
        
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            
            # Register event handlers
            asyncio.create_task(framework.register_event_handlers(self))
        
        cls.__init__ = new_init
        return cls
    
    return decorator

# Service health monitoring
class ServiceHealthMonitor:
    """Monitors health of all services in the mesh"""
    
    def __init__(self, communication_framework: CommunicationFramework):
        self.framework = communication_framework
        self.monitoring_task: Optional[asyncio.Task] = None
        self.running = False
    
    async def start_monitoring(self, interval: int = 30):
        """Start health monitoring"""
        self.running = True
        self.monitoring_task = asyncio.create_task(self._monitoring_loop(interval))
        logger.info(f"Started service health monitoring with {interval}s interval")
    
    async def stop_monitoring(self):
        """Stop health monitoring"""
        self.running = False
        
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Stopped service health monitoring")
    
    async def _monitoring_loop(self, interval: int):
        """Periodic health monitoring loop"""
        while self.running:
            try:
                await self._check_all_services_health()
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health monitoring failed: {e}")
                await asyncio.sleep(interval)
    
    async def _check_all_services_health(self):
        """Check health of all services"""
        try:
            health_status = await self.framework.get_service_mesh_health()
            
            unhealthy_services = []
            for service_id, status in health_status.items():
                if not status.get('is_healthy', False):
                    unhealthy_services.append(status)
            
            if unhealthy_services:
                # Emit unhealthy services event
                await self.framework.emit_event(
                    EventType.ERROR_OCCURRED,
                    {
                        'error_type': 'unhealthy_services',
                        'unhealthy_services': unhealthy_services,
                        'total_services': len(health_status),
                        'unhealthy_count': len(unhealthy_services)
                    }
                )
                
                logger.warning(f"Found {len(unhealthy_services)} unhealthy services")
            
        except Exception as e:
            logger.error(f"Failed to check services health: {e}")
