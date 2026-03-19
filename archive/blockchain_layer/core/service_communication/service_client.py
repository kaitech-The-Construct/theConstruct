"""
Service communication client for inter-service communication
"""
import asyncio
import aiohttp
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import os

logger = logging.getLogger(__name__)

class ServiceType(Enum):
    """Enumeration of available services"""
    DATA_STORAGE = "data_storage"
    XRPL_SERVICE = "xrpl_service"
    API_GATEWAY = "api_gateway"
    NOTIFICATIONS = "notifications"
    PUBSUB = "pubsub"
    SECURITY = "security"
    SUBSCRIPTION_MANAGEMENT = "subscription_management"

@dataclass
class ServiceEndpoint:
    """Service endpoint configuration"""
    name: str
    host: str
    port: int
    health_path: str = "/health"
    ready_path: str = "/ready"
    base_path: str = ""
    
    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}{self.base_path}"
    
    @property
    def health_url(self) -> str:
        return f"{self.base_url}{self.health_path}"
    
    @property
    def ready_url(self) -> str:
        return f"{self.base_url}{self.ready_path}"

class ServiceRegistry:
    """Registry for service endpoints and discovery"""
    
    def __init__(self):
        self.services: Dict[ServiceType, ServiceEndpoint] = {}
        self._load_default_services()
    
    def _load_default_services(self):
        """Load default service configurations from environment"""
        default_services = {
            ServiceType.DATA_STORAGE: ServiceEndpoint(
                name="data_storage",
                host=os.getenv("DATA_STORAGE_HOST", "localhost"),
                port=int(os.getenv("DATA_STORAGE_PORT", 8003))
            ),
            ServiceType.XRPL_SERVICE: ServiceEndpoint(
                name="xrpl_service",
                host=os.getenv("XRPL_SERVICE_HOST", "localhost"),
                port=int(os.getenv("XRPL_SERVICE_PORT", 8001))
            ),
            ServiceType.API_GATEWAY: ServiceEndpoint(
                name="api_gateway",
                host=os.getenv("API_GATEWAY_HOST", "localhost"),
                port=int(os.getenv("API_GATEWAY_PORT", 8000))
            ),
            ServiceType.NOTIFICATIONS: ServiceEndpoint(
                name="notifications",
                host=os.getenv("NOTIFICATIONS_HOST", "localhost"),
                port=int(os.getenv("NOTIFICATIONS_PORT", 8004))
            ),
            ServiceType.PUBSUB: ServiceEndpoint(
                name="pubsub",
                host=os.getenv("PUBSUB_HOST", "localhost"),
                port=int(os.getenv("PUBSUB_PORT", 8005))
            ),
            ServiceType.SECURITY: ServiceEndpoint(
                name="security",
                host=os.getenv("SECURITY_HOST", "localhost"),
                port=int(os.getenv("SECURITY_PORT", 8006))
            ),
            ServiceType.SUBSCRIPTION_MANAGEMENT: ServiceEndpoint(
                name="subscription_management",
                host=os.getenv("SUBSCRIPTION_MANAGEMENT_HOST", "localhost"),
                port=int(os.getenv("SUBSCRIPTION_MANAGEMENT_PORT", 8007))
            )
        }
        
        self.services.update(default_services)
    
    def register_service(self, service_type: ServiceType, endpoint: ServiceEndpoint):
        """Register a service endpoint"""
        self.services[service_type] = endpoint
        logger.info(f"Registered service: {service_type.value} at {endpoint.base_url}")
    
    def get_service(self, service_type: ServiceType) -> Optional[ServiceEndpoint]:
        """Get service endpoint by type"""
        return self.services.get(service_type)
    
    def list_services(self) -> Dict[ServiceType, ServiceEndpoint]:
        """List all registered services"""
        return self.services.copy()

class ServiceClient:
    """HTTP client for inter-service communication"""
    
    def __init__(self, service_registry: ServiceRegistry, timeout: int = 30):
        self.registry = service_registry
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def _ensure_session(self):
        """Ensure session is available"""
        if not self.session:
            self.session = aiohttp.ClientSession(timeout=self.timeout)
    
    async def health_check(self, service_type: ServiceType) -> Dict[str, Any]:
        """Check health of a specific service"""
        service = self.registry.get_service(service_type)
        if not service:
            return {"status": "unknown", "error": "Service not registered"}
        
        await self._ensure_session()
        
        try:
            async with self.session.get(service.health_url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {"status": "healthy", "data": data}
                else:
                    return {"status": "unhealthy", "status_code": response.status}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    async def readiness_check(self, service_type: ServiceType) -> Dict[str, Any]:
        """Check readiness of a specific service"""
        service = self.registry.get_service(service_type)
        if not service:
            return {"status": "unknown", "error": "Service not registered"}
        
        await self._ensure_session()
        
        try:
            async with self.session.get(service.ready_url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {"status": "ready", "data": data}
                else:
                    return {"status": "not_ready", "status_code": response.status}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    async def get(self, service_type: ServiceType, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request to a service"""
        service = self.registry.get_service(service_type)
        if not service:
            raise ValueError(f"Service {service_type.value} not registered")
        
        url = f"{service.base_url}{path}"
        await self._ensure_session()
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=error_text
                    )
        except Exception as e:
            logger.error(f"GET request failed to {service_type.value}{path}: {e}")
            raise
    
    async def post(self, service_type: ServiceType, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make POST request to a service"""
        service = self.registry.get_service(service_type)
        if not service:
            raise ValueError(f"Service {service_type.value} not registered")
        
        url = f"{service.base_url}{path}"
        await self._ensure_session()
        
        try:
            async with self.session.post(url, json=data) as response:
                if response.status in [200, 201]:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=error_text
                    )
        except Exception as e:
            logger.error(f"POST request failed to {service_type.value}{path}: {e}")
            raise
    
    async def put(self, service_type: ServiceType, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make PUT request to a service"""
        service = self.registry.get_service(service_type)
        if not service:
            raise ValueError(f"Service {service_type.value} not registered")
        
        url = f"{service.base_url}{path}"
        await self._ensure_session()
        
        try:
            async with self.session.put(url, json=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=error_text
                    )
        except Exception as e:
            logger.error(f"PUT request failed to {service_type.value}{path}: {e}")
            raise
    
    async def delete(self, service_type: ServiceType, path: str) -> Dict[str, Any]:
        """Make DELETE request to a service"""
        service = self.registry.get_service(service_type)
        if not service:
            raise ValueError(f"Service {service_type.value} not registered")
        
        url = f"{service.base_url}{path}"
        await self._ensure_session()
        
        try:
            async with self.session.delete(url) as response:
                if response.status in [200, 204]:
                    if response.content_length and response.content_length > 0:
                        return await response.json()
                    else:
                        return {"status": "success"}
                else:
                    error_text = await response.text()
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=error_text
                    )
        except Exception as e:
            logger.error(f"DELETE request failed to {service_type.value}{path}: {e}")
            raise
    
    async def health_check_all(self) -> Dict[ServiceType, Dict[str, Any]]:
        """Check health of all registered services"""
        health_results = {}
        
        tasks = []
        for service_type in self.registry.services.keys():
            tasks.append(self.health_check(service_type))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for service_type, result in zip(self.registry.services.keys(), results):
            if isinstance(result, Exception):
                health_results[service_type] = {"status": "error", "error": str(result)}
            else:
                health_results[service_type] = result
        
        return health_results

# Global service registry and client
service_registry = ServiceRegistry()

async def get_service_client() -> ServiceClient:
    """Get service client instance"""
    return ServiceClient(service_registry)
