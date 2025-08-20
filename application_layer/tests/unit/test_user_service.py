"""
Unit tests for UserService.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta

from app.core.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.exceptions import UserNotFoundError, DuplicateUserError, ValidationError


class TestUserService:
    """Test cases for UserService."""

    @pytest.mark.asyncio
    async def test_create_user_success(self, mock_user_service, sample_user_data):
        """Test successful user creation."""
        # Arrange
        user_create_data = UserCreate(
            email="test@example.com",
            username="testuser",
            password="securepassword123",
            firstName="Test",
            lastName="User"
        )
        
        mock_user_service.db.collection().where().get.return_value = []  # No existing user
        mock_user_service.db.collection().add.return_value = (None, "test-user-id")
        
        # Act
        result = await mock_user_service.create_user(user_create_data)
        
        # Assert
        assert result["id"] == "test-user-id"
        assert result["email"] == "test@example.com"
        assert result["username"] == "testuser"
        assert "password" not in result  # Password should not be in response
        mock_user_service.db.collection().add.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self, mock_user_service):
        """Test user creation with duplicate email."""
        # Arrange
        user_create_data = UserCreate(
            email="existing@example.com",
            username="testuser",
            password="securepassword123",
            firstName="Test",
            lastName="User"
        )
        
        # Mock existing user
        existing_user_doc = Mock()
        existing_user_doc.exists = True
        mock_user_service.db.collection().where().get.return_value = [existing_user_doc]
        
        # Act & Assert
        with pytest.raises(DuplicateUserError):
            await mock_user_service.create_user(user_create_data)

    @pytest.mark.asyncio
    async def test_get_user_by_id_success(self, mock_user_service, sample_user_data):
        """Test successful user retrieval by ID."""
        # Arrange
        user_id = "test-user-id"
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = sample_user_data
        mock_user_service.db.collection().document().get.return_value = mock_doc
        
        # Act
        result = await mock_user_service.get_user_by_id(user_id)
        
        # Assert
        assert result["id"] == user_id
        assert result["email"] == sample_user_data["email"]
        mock_user_service.db.collection().document.assert_called_with(user_id)

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self, mock_user_service):
        """Test user retrieval with non-existent ID."""
        # Arrange
        user_id = "non-existent-id"
        mock_doc = Mock()
        mock_doc.exists = False
        mock_user_service.db.collection().document().get.return_value = mock_doc
        
        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await mock_user_service.get_user_by_id(user_id)

    @pytest.mark.asyncio
    async def test_update_user_success(self, mock_user_service, sample_user_data):
        """Test successful user update."""
        # Arrange
        user_id = "test-user-id"
        update_data = UserUpdate(
            firstName="Updated",
            lastName="Name",
            bio="Updated bio"
        )
        
        # Mock existing user
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = sample_user_data
        mock_user_service.db.collection().document().get.return_value = mock_doc
        
        # Act
        result = await mock_user_service.update_user(user_id, update_data)
        
        # Assert
        assert result["profile"]["firstName"] == "Updated"
        assert result["profile"]["lastName"] == "Name"
        assert result["profile"]["bio"] == "Updated bio"
        mock_user_service.db.collection().document().update.assert_called_once()

    @pytest.mark.asyncio
    async def test_verify_kyc_documents_success(self, mock_user_service, sample_user_data):
        """Test successful KYC document verification."""
        # Arrange
        user_id = "test-user-id"
        documents = ["passport.pdf", "utility_bill.pdf"]
        
        # Mock existing user
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = sample_user_data
        mock_user_service.db.collection().document().get.return_value = mock_doc
        
        # Act
        result = await mock_user_service.verify_kyc_documents(user_id, documents)
        
        # Assert
        assert result is True
        mock_user_service.db.collection().document().update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_reputation_score(self, mock_user_service, sample_user_data):
        """Test reputation score update."""
        # Arrange
        user_id = "test-user-id"
        transaction_data = {
            "success": True,
            "amount": 1000,
            "rating": 5
        }
        
        # Mock existing user
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = sample_user_data
        mock_user_service.db.collection().document().get.return_value = mock_doc
        
        # Act
        new_score = await mock_user_service.update_reputation_score(user_id, transaction_data)
        
        # Assert
        assert isinstance(new_score, float)
        assert new_score >= 0
        mock_user_service.db.collection().document().update.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_activity_history(self, mock_user_service):
        """Test user activity history retrieval."""
        # Arrange
        user_id = "test-user-id"
        mock_activities = [
            {
                "id": "activity-1",
                "type": "login",
                "timestamp": datetime.utcnow().isoformat(),
                "details": {"ip": "192.168.1.1"}
            },
            {
                "id": "activity-2",
                "type": "purchase",
                "timestamp": datetime.utcnow().isoformat(),
                "details": {"product_id": "robot-1", "amount": 1000}
            }
        ]
        
        mock_user_service.db.collection().where().order_by().limit().get.return_value = [
            Mock(to_dict=lambda: activity) for activity in mock_activities
        ]
        
        # Act
        result = await mock_user_service.get_user_activity_history(user_id)
        
        # Assert
        assert len(result) == 2
        assert result[0]["type"] == "login"
        assert result[1]["type"] == "purchase"

    @pytest.mark.asyncio
    async def test_manage_user_preferences(self, mock_user_service, sample_user_data):
        """Test user preferences management."""
        # Arrange
        user_id = "test-user-id"
        preferences = {
            "notifications": {
                "email": False,
                "push": True,
                "sms": True
            },
            "privacy": {
                "profileVisible": False,
                "transactionHistoryVisible": True
            }
        }
        
        # Mock existing user
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = sample_user_data
        mock_user_service.db.collection().document().get.return_value = mock_doc
        
        # Act
        result = await mock_user_service.manage_user_preferences(user_id, preferences)
        
        # Assert
        assert result is True
        mock_user_service.db.collection().document().update.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_user_success(self, mock_user_service, sample_user_data):
        """Test successful user deletion."""
        # Arrange
        user_id = "test-user-id"
        
        # Mock existing user
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = sample_user_data
        mock_user_service.db.collection().document().get.return_value = mock_doc
        
        # Act
        result = await mock_user_service.delete_user(user_id)
        
        # Assert
        assert result is True
        mock_user_service.db.collection().document().delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_authenticate_user_success(self, mock_user_service, sample_user_data):
        """Test successful user authentication."""
        # Arrange
        email = "test@example.com"
        password = "securepassword123"
        
        # Mock user with hashed password
        user_data = sample_user_data.copy()
        user_data["password_hash"] = "hashed_password"
        
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = user_data
        mock_user_service.db.collection().where().get.return_value = [mock_doc]
        
        with patch('app.core.services.user_service.verify_password', return_value=True):
            # Act
            result = await mock_user_service.authenticate_user(email, password)
            
            # Assert
            assert result["email"] == email
            assert "password_hash" not in result

    @pytest.mark.asyncio
    async def test_authenticate_user_invalid_credentials(self, mock_user_service):
        """Test user authentication with invalid credentials."""
        # Arrange
        email = "test@example.com"
        password = "wrongpassword"
        
        mock_user_service.db.collection().where().get.return_value = []
        
        # Act & Assert
        with pytest.raises(ValidationError):
            await mock_user_service.authenticate_user(email, password)

    @pytest.mark.asyncio
    async def test_connect_wallet_success(self, mock_user_service, sample_user_data):
        """Test successful wallet connection."""
        # Arrange
        user_id = "test-user-id"
        wallet_address = "rNewXRPLAddress123456789"
        wallet_type = "xrpl"
        
        # Mock existing user
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = sample_user_data
        mock_user_service.db.collection().document().get.return_value = mock_doc
        
        # Act
        result = await mock_user_service.connect_wallet(user_id, wallet_address, wallet_type)
        
        # Assert
        assert result is True
        mock_user_service.db.collection().document().update.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_statistics(self, mock_user_service):
        """Test user statistics retrieval."""
        # Arrange
        user_id = "test-user-id"
        
        # Mock statistics data
        mock_stats = {
            "totalOrders": 15,
            "completedOrders": 12,
            "totalSpent": 50000,
            "averageRating": 4.5,
            "joinDate": "2025-01-01T00:00:00Z"
        }
        
        with patch.object(mock_user_service, '_calculate_user_statistics', return_value=mock_stats):
            # Act
            result = await mock_user_service.get_user_statistics(user_id)
            
            # Assert
            assert result["totalOrders"] == 15
            assert result["completedOrders"] == 12
            assert result["averageRating"] == 4.5

    @pytest.mark.asyncio
    async def test_cache_user_data(self, mock_user_service, sample_user_data):
        """Test user data caching."""
        # Arrange
        user_id = "test-user-id"
        
        # Act
        await mock_user_service._cache_user_data(user_id, sample_user_data)
        
        # Assert
        mock_user_service.cache.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_cached_user_data(self, mock_user_service, sample_user_data):
        """Test cached user data retrieval."""
        # Arrange
        user_id = "test-user-id"
        mock_user_service.cache.get.return_value = sample_user_data
        
        # Act
        result = await mock_user_service._get_cached_user_data(user_id)
        
        # Assert
        assert result == sample_user_data
        mock_user_service.cache.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_validate_user_permissions(self, mock_user_service, sample_user_data):
        """Test user permission validation."""
        # Arrange
        user_id = "test-user-id"
        required_permission = "product:create"
        
        # Mock user with permissions
        user_data = sample_user_data.copy()
        user_data["permissions"] = ["product:create", "product:read"]
        
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = user_data
        mock_user_service.db.collection().document().get.return_value = mock_doc
        
        # Act
        result = await mock_user_service.validate_user_permissions(user_id, required_permission)
        
        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_search_users(self, mock_user_service):
        """Test user search functionality."""
        # Arrange
        search_query = "test"
        filters = {"role": "manufacturer", "verified": True}
        
        mock_users = [
            {"id": "user-1", "username": "testuser1", "role": "manufacturer"},
            {"id": "user-2", "username": "testuser2", "role": "manufacturer"}
        ]
        
        mock_user_service.db.collection().where().where().get.return_value = [
            Mock(to_dict=lambda: user) for user in mock_users
        ]
        
        # Act
        result = await mock_user_service.search_users(search_query, filters)
        
        # Assert
        assert len(result) == 2
        assert all("test" in user["username"] for user in result)
