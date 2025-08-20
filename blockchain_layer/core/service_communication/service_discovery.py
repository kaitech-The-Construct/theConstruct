"""
Service discovery and registration for The Construct blockchain layer
"""
import asyncio
import json
import logging
from typing import Dict, Any, Optional, List, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import redis.asyncio as redis
import uuid
import os

logger = logging.getLogger(__name__)

@dataclass
class ServiceInfo:
    """Service information for discovery"""
    service_id: str
    service_name: str
    service_type: str
    host: str
    port: int
    version: str
    health_endpoint: str
    ready_endpoint: str
    metadata: Dict[str, Any]
    registered_at: datetime
    last_heartbeat: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'service_id': self.service_id,
            'service_name': self.service_name,
            'service_type': self.service_type,
            'host': self.host,
            'port': self.port,
            'version': self.version,
            'health_endpoint': self.health_endpoint,
            'ready_endpoint': self.ready_endpoint,
            'metadata': self.metadata,
            'registered_at': self.registered_at.isoformat(),
            'last_heartbeat': self.last_heartbeat.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ServiceInfo':
        """Create from dictionary"""
        return cls(
            service_id=data['service_id'],
            service_name=data['service_name'],
            service_type=data['service_type'],
            host=data['host'],
            port=data['port'],
            version=data['version'],
            health_endpoint=data['health_endpoint'],
            ready_endpoint=data['ready_endpoint'],
            metadata=data['metadata'],
            registered_at=datetime.fromisoformat(data['registered_at']),
            last_heartbeat=datetime.fromisoformat(data['last_heartbeat'])
        )
    
    @property
    def base_url(self) -> str:
        """Get base URL for the service"""
        return f"http://{self.host}:{self.port}"
    
    @property
    def is_healthy(self) -> bool:
        """Check if service is considered healthy based on heartbeat"""
        return (datetime.utcnow() - self.last_heartbeat).seconds < 60

class ServiceDiscovery:
    """Redis-based service discovery mechanism"""
    
    def __init__(self, redis_config: Dict[str, Any], service_info: ServiceInfo):
        self.redis_config = redis_config
        self.service_info = service_info
        self.redis_client: Optional[redis.Redis] = None
        self.heartbeat_task: Optional[asyncio.Task] = None
        self.cleanup_task: Optional[asyncio.Task] = None
        self.running = False
        
        # Redis keys
        self.services_key = "services:registry"
        self.service_key = f"service:{service_info.service_id}"
        self.heartbeat_key = f"heartbeat:{service_info.service_id}"
        
    async def initialize(self):
        """Initialize service discovery"""
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
            
            logger.info(f"Service discovery initialized for: {self.service_info.service_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize service discovery: {e}")
            raise
    
    async def register(self):
        """Register this service in the discovery registry"""
        if not self.redis_client:
            raise RuntimeError("Service discovery not initialized")
        
        try:
            # Register service in the main registry
            await self.redis_client.hset(
                self.services_key,
                self.service_info.service_id,
                json.dumps(self.service_info.to_dict())
            )
            
            # Set service-specific key with TTL
            await self.redis_client.setex(
                self.service_key,
                120,  # 2 minutes TTL
                json.dumps(self.service_info.to_dict())
            )
            
            # Start heartbeat
            await self._send_heartbeat()
            
            logger.info(f"Service registered: {self.service_info.service_name} ({self.service_info.service_id})")
            
        except Exception as e:
            logger.error(f"Failed to register service: {e}")
            raise
    
    async def deregister(self):
        """Deregister this service from the discovery registry"""
        if not self.redis_client:
            return
        
        try:
            # Remove from main registry
            await self.redis_client.hdel(self.services_key, self.service_info.service_id)
            
            # Remove service-specific key
            await self.redis_client.delete(self.service_key)
            
            # Remove heartbeat
            await self.redis_client.delete(self.heartbeat_key)
            
            logger.info(f"Service deregistered: {self.service_info.service_name}")
            
        except Exception as e:
            logger.error(f"Failed to deregister service: {e}")
    
    async def discover_services(self, service_type: Optional[str] = None) -> List[ServiceInfo]:
        """Discover available services"""
        if not self.redis_client:
            raise RuntimeError("Service discovery not initialized")
        
        try:
            # Get all registered services
            services_data = await self.redis_client.hgetall(self.services_key)
            services = []
            
            for service_id, service_json in services_data.items():
                try:
                    service_data = json.loads(service_json)
                    service_info = ServiceInfo.from_dict(service_data)
                    
                    # Filter by service type if specified
                    if service_type is None or service_info.service_type == service_type:
                        # Check if service is still alive
                        if await self._is_service_alive(service_info.service_id):
                            services.append(service_info)
                        else:
                            # Clean up dead service
                            await self._cleanup_dead_service(service_info.service_id)
                
                except Exception as e:
                    logger.warning(f"Failed to parse service data for {service_id}: {e}")
            
            return services
            
        except Exception as e:
            logger.error(f"Failed to discover services: {e}")
            return []
    
    async def get_service(self, service_id: str) -> Optional[ServiceInfo]:
        """Get specific service by ID"""
        if not self.redis_client:
            raise RuntimeError("Service discovery not initialized")
        
        try:
            service_json = await self.redis_client.hget(self.services_key, service_id)
            if service_json:
                service_data = json.loads(service_json)
                return ServiceInfo.from_dict(service_data)
        except Exception as e:
            logger.error(f"Failed to get service {service_id}: {e}")
        
        return None
    
    async def get_services_by_type(self, service_type: str) -> List[ServiceInfo]:
        """Get all services of a specific type"""
        return await self.discover_services(service_type)
    
    async def start_heartbeat(self, interval: int = 30):
        """Start sending periodic heartbeats"""
        if self.heartbeat_task and not self.heartbeat_task.done():
            return
        
        self.running = True
        self.heartbeat_task = asyncio.create_task(self._heartbeat_loop(interval))
        logger.info(f"Started heartbeat with {interval}s interval")
    
    async def stop_heartbeat(self):
        """Stop sending heartbeats"""
        self.running = False
        
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
            try:
                await self.heartbeat_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Stopped heartbeat")
    
    async def start_cleanup_task(self, interval: int = 60):
        """Start periodic cleanup of dead services"""
        if self.cleanup_task and not self.cleanup_task.done():
            return
        
        self.cleanup_task = asyncio.create_task(self._cleanup_loop(interval))
        logger.info(f"Started cleanup task with {interval}s interval")
    
    async def stop_cleanup_task(self):
        """Stop cleanup task"""
        if self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Stopped cleanup task")
    
    async def _heartbeat_loop(self, interval: int):
        """Periodic heartbeat loop"""
        while self.running:
            try:
                await self._send_heartbeat()
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Heartbeat failed: {e}")
                await asyncio.sleep(interval)
    
    async def _send_heartbeat(self):
        """Send heartbeat to indicate service is alive"""
        if not self.redis_client:
            return
        
        try:
            # Update last heartbeat time
            self.service_info.last_heartbeat = datetime.utcnow()
            
            # Update service info in registry
            await self.redis_client.hset(
                self.services_key,
                self.service_info.service_id,
                json.dumps(self.service_info.to_dict())
            )
            
            # Set heartbeat key with TTL
            await self.redis_client.setex(
                self.heartbeat_key,
                90,  # 90 seconds TTL
                datetime.utcnow().isoformat()
            )
            
            logger.debug(f"Heartbeat sent for service: {self.service_info.service_name}")
            
        except Exception as e:
            logger.error(f"Failed to send heartbeat: {e}")
    
    async def _cleanup_loop(self, interval: int):
        """Periodic cleanup of dead services"""
        while self.running:
            try:
                await self._cleanup_dead_services()
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Cleanup failed: {e}")
                await asyncio.sleep(interval)
    
    async def _cleanup_dead_services(self):
        """Remove dead services from registry"""
        if not self.redis_client:
            return
        
        try:
            services_data = await self.redis_client.hgetall(self.services_key)
            dead_services = []
            
            for service_id, service_json in services_data.items():
                if not await self._is_service_alive(service_id):
                    dead_services.append(service_id)
            
            # Remove dead services
            for service_id in dead_services:
                await self._cleanup_dead_service(service_id)
                logger.info(f"Cleaned up dead service: {service_id}")
            
        except Exception as e:
            logger.error(f"Failed to cleanup dead services: {e}")
    
    async def _is_service_alive(self, service_id: str) -> bool:
        """Check if a service is alive based on heartbeat"""
        try:
            heartbeat_key = f"heartbeat:{service_id}"
            heartbeat = await self.redis_client.get(heartbeat_key)
            return heartbeat is not None
        except Exception:
            return False
    
    async def _cleanup_dead_service(self, service_id: str):
        """Clean up a dead service"""
        try:
            await self.redis_client.hdel(self.services_key, service_id)
            await self.redis_client.delete(f"service:{service_id}")
            await self.redis_client.delete(f"heartbeat:{service_id}")
        except Exception as e:
            logger.error(f"Failed to cleanup service {service_id}: {e}")
    
    async def close(self):
        """Close service discovery"""
        await self.stop_heartbeat()
        await self.stop_cleanup_task()
        await self.deregister()
        
        if self.redis_client:
            await self.redis_client.close()

class LoadBalancer:
    """Simple load balancer for service instances"""
    
    def __init__(self, service_discovery: ServiceDiscovery):
        self.service_discovery = service_discovery
        self.round_robin_counters: Dict[str, int] = {}
    
    async def get_service_instance(self, service_type: str, strategy: str = "round_robin") -> Optional[ServiceInfo]:
        """Get a service instance using the specified load balancing strategy"""
        services = await self.service_discovery.get_services_by_type(service_type)
        
        if not services:
            return None
        
        if strategy == "round_robin":
            return self._round_robin_select(service_type, services)
        elif strategy == "random":
            import random
            return random.choice(services)
        elif strategy == "least_connections":
            # For now, just return the first service
            # In a real implementation, you'd track connection counts
            return services[0]
        else:
            return services[0]
    
    def _round_robin_select(self, service_type: str, services: List[ServiceInfo]) -> ServiceInfo:
        """Round-robin service selection"""
        if service_type not in self.round_robin_counters:
            self.round_robin_counters[service_type] = 0
        
        index = self.round_robin_counters[service_type] % len(services)
        self.round_robin_counters[service_type] += 1
        
        return services[index]

class ServiceMesh:
    """Service mesh for managing service-to-service communication"""
    
    def __init__(self, service_name: str, service_type: str, redis_config: Dict[str, Any]):
        self.service_name = service_name
        self.service_type = service_type
        self.redis_config = redis_config
        
        # Create service info
        self.service_info = ServiceInfo(
            service_id=str(uuid.uuid4()),
            service_name=service_name,
            service_type=service_type,
            host=os.getenv('SERVICE_HOST', 'localhost'),
            port=int(os.getenv('SERVICE_PORT', 8080)),
            version=os.getenv('SERVICE_VERSION', '1.0.0'),
            health_endpoint='/health',
            ready_endpoint='/ready',
            metadata={
                'started_at': datetime.utcnow().isoformat(),
                'environment': os.getenv('ENVIRONMENT', 'development'),
                'region': os.getenv('REGION', 'local')
            },
            registered_at=datetime.utcnow(),
            last_heartbeat=datetime.utcnow()
        )
        
        self.service_discovery = ServiceDiscovery(redis_config, self.service_info)
        self.load_balancer = LoadBalancer(self.service_discovery)
        
    async def initialize(self):
        """Initialize service mesh"""
        await self.service_discovery.initialize()
        await self.service_discovery.register()
        await self.service_discovery.start_heartbeat()
        await self.service_discovery.start_cleanup_task()
        
        logger.info(f"Service mesh initialized for: {self.service_name}")
    
    async def close(self):
        """Close service mesh"""
        await self.service_discovery.close()
        logger.info("Service mesh closed")
    
    async def discover_service(self, service_type: str, strategy: str = "round_robin") -> Optional[ServiceInfo]:
        """Discover and select a service instance"""
        return await self.load_balancer.get_service_instance(service_type, strategy)
    
    async def get_all_services(self) -> List[ServiceInfo]:
        """Get all registered services"""
        return await self.service_discovery.discover_services()
    
    async def get_service_health(self) -> Dict[str, Any]:
        """Get health status of all services"""
        services = await self.get_all_services()
        health_status = {}
        
        for service in services:
            health_status[service.service_id] = {
                'service_name': service.service_name,
                'service_type': service.service_type,
                'host': service.host,
                'port': service.port,
                'is_healthy': service.is_healthy,
                'last_heartbeat': service.last_heartbeat.isoformat()
            }
        
        return health_status

class ServiceProxy:
    """Proxy for making calls to discovered services"""
    
    def __init__(self, service_mesh: ServiceMesh, target_service_type: str):
        self.service_mesh = service_mesh
        self.target_service_type = target_service_type
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        import aiohttp
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def call(self, method: str, path: str, data: Optional[Dict[str, Any]] = None, 
                  params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a call to the target service"""
        # Discover service instance
        service_instance = await self.service_mesh.discover_service(self.target_service_type)
        
        if not service_instance:
            raise RuntimeError(f"No healthy instances found for service type: {self.target_service_type}")
        
        url = f"{service_instance.base_url}{path}"
        
        if not self.session:
            import aiohttp
            self.session = aiohttp.ClientSession()
        
        try:
            if method.upper() == "GET":
                async with self.session.get(url, params=params) as response:
                    response.raise_for_status()
                    return await response.json()
            elif method.upper() == "POST":
                async with self.session.post(url, json=data, params=params) as response:
                    response.raise_for_status()
                    return await response.json()
            elif method.upper() == "PUT":
                async with self.session.put(url, json=data, params=params) as response:
                    response.raise_for_status()
                    return await response.json()
            elif method.upper() == "DELETE":
                async with self.session.delete(url, params=params) as response:
                    response.raise_for_status()
                    if response.content_length and response.content_length > 0:
                        return await response.json()
                    else:
                        return {"status": "success"}
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
        except Exception as e:
            logger.error(f"Service call failed to {self.target_service_type}{path}: {e}")
            raise

# Utility functions
def create_service_info(service_name: str, service_type: str, port: int, 
                       metadata: Optional[Dict[str, Any]] = None) -> ServiceInfo:
    """Create service info with default values"""
    return ServiceInfo(
        service_id=str(uuid.uuid4()),
        service_name=service_name,
        service_type=service_type,
        host=os.getenv('SERVICE_HOST', 'localhost'),
        port=port,
        version=os.getenv('SERVICE_VERSION', '1.0.0'),
        health_endpoint='/health',
        ready_endpoint='/ready',
        metadata=metadata or {},
        registered_at=datetime.utcnow(),
        last_heartbeat=datetime.utcnow()
    )

async def wait_for_service(service_discovery: ServiceDiscovery, service_type: str, 
                          timeout: int = 60) -> Optional[ServiceInfo]:
    """Wait for a service of the specified type to become available"""
    start_time = datetime.utcnow()
    
    while (datetime.utcnow() - start_time).seconds < timeout:
        services = await service_discovery.get_services_by_type(service_type)
        if services:
            return services[0]
        
        await asyncio.sleep(5)  # Check every 5 seconds
    
    return None
