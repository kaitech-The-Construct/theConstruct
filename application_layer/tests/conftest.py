"""
Test configuration and fixtures for The Construct application layer tests.
"""

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import Mock, AsyncMock
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app
from app.core.config.settings import get_settings
from app.core.services.user_service import UserService
from app.core.services.robot_service import RobotService
from app.core.services.trade_service import TradeService
from app.core.services.design_service import DesignService
from app.core.services.software_service import SoftwareService
from app.core.services.governance_service import GovernanceService
from app.core.services.analytics_service import AnalyticsService
from app.core.services.notification_service import NotificationService
from app.core.services.manufacturing_service import ManufacturingService
from app.core.services.blockchain_service import BlockchainService


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_settings():
    """Test settings configuration."""
    settings = get_settings()
    settings.ENVIRONMENT = "testing"
    settings.DATABASE_URL = "firestore://test-project"
    settings.REDIS_URL = "redis://localhost:6379/1"
    settings.JWT_SECRET_KEY = "test-secret-key"
    return settings


@pytest.fixture
def client() -> TestClient:
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_firestore():
    """Mock Firestore database."""
    mock_db = Mock()
    mock_collection = Mock()
    mock_document = Mock()
    
    # Configure mock chain
    mock_db.collection.return_value = mock_collection
    mock_collection.document.return_value = mock_document
    mock_collection.add.return_value = (None, "test-doc-id")
    mock_collection.get.return_value = []
    mock_document.get.return_value = Mock(exists=True, to_dict=lambda: {"id": "test-id"})
    mock_document.set.return_value = None
    mock_document.update.return_value = None
    mock_document.delete.return_value = None
    
    return mock_db


@pytest.fixture
def mock_redis():
    """Mock Redis cache."""
    mock_redis = AsyncMock()
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True
    mock_redis.delete.return_value = True
    mock_redis.exists.return_value = False
    return mock_redis


@pytest.fixture
def mock_blockchain_service():
    """Mock blockchain service."""
    mock_service = AsyncMock(spec=BlockchainService)
    mock_service.create_asset_token.return_value = {
        "transaction_hash": "test-tx-hash",
        "token_id": "test-token-id"
    }
    mock_service.execute_trade.return_value = {
        "transaction_hash": "test-trade-hash",
        "status": "completed"
    }
    mock_service.create_escrow.return_value = {
        "escrow_id": "test-escrow-id",
        "status": "created"
    }
    return mock_service


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "id": "test-user-id",
        "email": "test@example.com",
        "username": "testuser",
        "profile": {
            "firstName": "Test",
            "lastName": "User",
            "avatar": "https://example.com/avatar.jpg",
            "bio": "Test user bio"
        },
        "wallets": {
            "xrpl": "rTestXRPLAddress123456789",
            "solana": "TestSolanaAddress123456789"
        },
        "kyc": {
            "status": "verified",
            "documents": ["passport.pdf", "utility_bill.pdf"],
            "verifiedAt": "2025-01-01T00:00:00Z"
        },
        "reputation": {
            "score": 85,
            "totalTransactions": 10,
            "successRate": 0.95
        },
        "preferences": {
            "notifications": {
                "email": True,
                "push": True,
                "sms": False
            },
            "privacy": {
                "profileVisible": True,
                "transactionHistoryVisible": False
            }
        },
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:00:00Z"
    }


@pytest.fixture
def sample_robot_data():
    """Sample robot data for testing."""
    return {
        "id": "test-robot-id",
        "sellerId": "test-seller-id",
        "type": "robot",
        "name": "Industrial Robot Arm",
        "description": "6-axis industrial robot arm for manufacturing",
        "specifications": {
            "technical": {
                "payload": "10kg",
                "reach": "1.5m",
                "repeatability": "±0.1mm"
            },
            "compatibility": ["ROS", "Modbus", "Ethernet/IP"],
            "dimensions": {
                "length": "1.2m",
                "width": "0.8m",
                "height": "1.5m",
                "weight": "150kg"
            }
        },
        "pricing": {
            "basePrice": 50000,
            "currency": "USD",
            "subscriptionModel": {
                "available": True,
                "monthlyPrice": 2000,
                "features": ["maintenance", "support", "updates"]
            }
        },
        "inventory": {
            "available": 5,
            "reserved": 2,
            "total": 7
        },
        "media": {
            "images": ["robot1.jpg", "robot2.jpg"],
            "videos": ["demo.mp4"],
            "documents": ["manual.pdf", "specs.pdf"]
        },
        "ratings": {
            "average": 4.5,
            "count": 20,
            "reviews": ["review1", "review2"]
        },
        "blockchain": {
            "tokenId": "test-token-id",
            "chain": "xrpl",
            "contractAddress": "rContractAddress123456789"
        },
        "status": "active",
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:00:00Z"
    }


@pytest.fixture
def sample_order_data():
    """Sample order data for testing."""
    return {
        "id": "test-order-id",
        "buyerId": "test-buyer-id",
        "sellerId": "test-seller-id",
        "productId": "test-product-id",
        "orderType": "purchase",
        "quantity": 1,
        "pricing": {
            "unitPrice": 50000,
            "totalPrice": 50000,
            "currency": "USD"
        },
        "payment": {
            "method": "escrow",
            "status": "pending",
            "transactionHash": None,
            "escrowId": "test-escrow-id"
        },
        "shipping": {
            "address": {
                "street": "123 Test St",
                "city": "Test City",
                "state": "TS",
                "zipCode": "12345",
                "country": "US"
            },
            "method": "standard",
            "trackingNumber": None,
            "estimatedDelivery": "2025-01-15T00:00:00Z"
        },
        "status": "created",
        "milestones": [
            {
                "id": "milestone-1",
                "description": "Order confirmation",
                "status": "completed",
                "completedAt": "2025-01-01T00:00:00Z"
            },
            {
                "id": "milestone-2",
                "description": "Payment processing",
                "status": "pending",
                "completedAt": None
            }
        ],
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:00:00Z"
    }


@pytest.fixture
def sample_manufacturing_order_data():
    """Sample manufacturing order data for testing."""
    return {
        "id": "test-mfg-order-id",
        "customerId": "test-customer-id",
        "manufacturerId": "test-manufacturer-id",
        "specifications": {
            "cadFiles": ["part1.step", "part2.step"],
            "materials": ["aluminum", "steel"],
            "quantity": 100,
            "tolerances": {
                "dimensional": "±0.1mm",
                "surface": "Ra 1.6"
            },
            "qualityRequirements": ["ISO9001", "AS9100"]
        },
        "quotes": [
            {
                "manufacturerId": "test-manufacturer-id",
                "price": 10000,
                "timeline": 30,
                "capabilities": ["CNC", "3D Printing", "Assembly"],
                "certifications": ["ISO9001", "AS9100"]
            }
        ],
        "selectedQuote": "test-manufacturer-id",
        "contract": {
            "solanaContractId": "test-contract-id",
            "milestones": [
                {
                    "description": "Material procurement",
                    "paymentPercentage": 25,
                    "dueDate": "2025-01-10T00:00:00Z",
                    "status": "pending"
                },
                {
                    "description": "Manufacturing completion",
                    "paymentPercentage": 50,
                    "dueDate": "2025-01-20T00:00:00Z",
                    "status": "pending"
                },
                {
                    "description": "Quality inspection",
                    "paymentPercentage": 20,
                    "dueDate": "2025-01-25T00:00:00Z",
                    "status": "pending"
                },
                {
                    "description": "Delivery",
                    "paymentPercentage": 5,
                    "dueDate": "2025-01-30T00:00:00Z",
                    "status": "pending"
                }
            ]
        },
        "production": {
            "startDate": None,
            "estimatedCompletion": "2025-01-30T00:00:00Z",
            "actualCompletion": None,
            "qualityReports": []
        },
        "status": "rfq",
        "createdAt": "2025-01-01T00:00:00Z",
        "updatedAt": "2025-01-01T00:00:00Z"
    }


@pytest.fixture
def mock_user_service(mock_firestore, mock_redis):
    """Mock user service with dependencies."""
    service = UserService()
    service.db = mock_firestore
    service.cache = mock_redis
    return service


@pytest.fixture
def mock_robot_service(mock_firestore, mock_redis):
    """Mock robot service with dependencies."""
    service = RobotService()
    service.db = mock_firestore
    service.cache = mock_redis
    return service


@pytest.fixture
def mock_trade_service(mock_firestore, mock_redis, mock_blockchain_service):
    """Mock trade service with dependencies."""
    service = TradeService()
    service.db = mock_firestore
    service.cache = mock_redis
    service.blockchain_service = mock_blockchain_service
    return service


@pytest.fixture
def mock_manufacturing_service(mock_firestore, mock_redis, mock_blockchain_service):
    """Mock manufacturing service with dependencies."""
    service = ManufacturingService()
    service.db = mock_firestore
    service.cache = mock_redis
    service.blockchain_service = mock_blockchain_service
    return service


@pytest.fixture
def jwt_token():
    """Sample JWT token for authentication testing."""
    return "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidGVzdC11c2VyLWlkIiwiZXhwIjoxNjQwOTk1MjAwfQ.test-signature"


@pytest.fixture
def auth_headers(jwt_token):
    """Authentication headers for API testing."""
    return {"Authorization": f"Bearer {jwt_token}"}


# Test data cleanup
@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Cleanup test data after each test."""
    yield
    # Add cleanup logic here if needed
    pass


# Performance testing fixtures
@pytest.fixture
def performance_test_config():
    """Configuration for performance tests."""
    return {
        "concurrent_users": 10,
        "test_duration": 30,  # seconds
        "ramp_up_time": 5,    # seconds
        "endpoints": [
            "/api/v1/robots",
            "/api/v1/users/profile",
            "/api/v1/trades"
        ]
    }


# Database transaction fixtures
@pytest.fixture
def db_transaction(mock_firestore):
    """Database transaction for testing."""
    transaction = Mock()
    mock_firestore.transaction.return_value = transaction
    return transaction
