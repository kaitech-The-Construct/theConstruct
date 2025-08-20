"""
Service communication package for The Construct blockchain layer
"""
from .service_client import ServiceClient, ServiceRegistry, ServiceType, ServiceEndpoint
from .message_queue import (
    MessageQueue, EventBus, ServiceCommunicationManager, EventType, Event,
    EventHandlerRegistry, event_handler, async_event_handler,
    emit_user_event, emit_trading_event, emit_manufacturing_event, emit_blockchain_event
)
from .service_discovery import (
    ServiceDiscovery, ServiceInfo, ServiceMesh, LoadBalancer, ServiceProxy,
    create_service_info, wait_for_service
)
from .communication_framework import (
    CommunicationFramework, ServiceOrchestrator, TradingWorkflow, ManufacturingWorkflow,
    ServiceEventHandlers, ServiceHealthMonitor, create_communication_framework,
    communication_context, auto_register_handlers
)

__all__ = [
    # Service client
    'ServiceClient',
    'ServiceRegistry', 
    'ServiceType',
    'ServiceEndpoint',
    
    # Message queue
    'MessageQueue',
    'EventBus',
    'ServiceCommunicationManager',
    'EventType',
    'Event',
    'EventHandlerRegistry',
    'event_handler',
    'async_event_handler',
    'emit_user_event',
    'emit_trading_event', 
    'emit_manufacturing_event',
    'emit_blockchain_event',
    
    # Service discovery
    'ServiceDiscovery',
    'ServiceInfo',
    'ServiceMesh',
    'LoadBalancer',
    'ServiceProxy',
    'create_service_info',
    'wait_for_service',
    
    # Communication framework
    'CommunicationFramework',
    'ServiceOrchestrator',
    'TradingWorkflow',
    'ManufacturingWorkflow',
    'ServiceEventHandlers',
    'ServiceHealthMonitor',
    'create_communication_framework',
    'communication_context',
    'auto_register_handlers'
]
