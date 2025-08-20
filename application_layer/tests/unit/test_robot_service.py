"""
Unit tests for RobotService.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from app.core.services.robot_service import RobotService
from app.schemas.robot import RobotCreate, RobotUpdate, RobotResponse
from app.core.exceptions import RobotNotFoundError, ValidationError


class TestRobotService:
    """Test cases for RobotService."""

    @pytest.mark.asyncio
    async def test_create_robot_success(self, mock_robot_service, sample_robot_data):
        """Test successful robot creation."""
        # Arrange
        robot_create_data = RobotCreate(
            name="Industrial Robot Arm",
            description="6-axis industrial robot arm for manufacturing",
            type="robot",
            specifications={
                "technical": {
                    "payload": "10kg",
                    "reach": "1.5m",
                    "repeatability": "±0.1mm"
                }
            },
            pricing={
                "basePrice": 50000,
                "currency": "USD"
            }
        )
        
        mock_robot_service.db.collection().add.return_value = (None, "test-robot-id")
        
        # Act
        result = await mock_robot_service.create_robot(robot_create_data, "test-seller-id")
        
        # Assert
        assert result["id"] == "test-robot-id"
        assert result["name"] == "Industrial Robot Arm"
        assert result["sellerId"] == "test-seller-id"
        mock_robot_service.db.collection().add.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_robot_by_id_success(self, mock_robot_service, sample_robot_data):
        """Test successful robot retrieval by ID."""
        # Arrange
        robot_id = "test-robot-id"
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = sample_robot_data
        mock_robot_service.db.collection().document().get.return_value = mock_doc
        
        # Act
        result = await mock_robot_service.get_robot_by_id(robot_id)
        
        # Assert
        assert result["id"] == robot_id
        assert result["name"] == sample_robot_data["name"]
        mock_robot_service.db.collection().document.assert_called_with(robot_id)

    @pytest.mark.asyncio
    async def test_get_robot_by_id_not_found(self, mock_robot_service):
        """Test robot retrieval with non-existent ID."""
        # Arrange
        robot_id = "non-existent-id"
        mock_doc = Mock()
        mock_doc.exists = False
        mock_robot_service.db.collection().document().get.return_value = mock_doc
        
        # Act & Assert
        with pytest.raises(RobotNotFoundError):
            await mock_robot_service.get_robot_by_id(robot_id)

    @pytest.mark.asyncio
    async def test_update_robot_success(self, mock_robot_service, sample_robot_data):
        """Test successful robot update."""
        # Arrange
        robot_id = "test-robot-id"
        update_data = RobotUpdate(
            name="Updated Robot Name",
            description="Updated description",
            pricing={
                "basePrice": 55000,
                "currency": "USD"
            }
        )
        
        # Mock existing robot
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = sample_robot_data
        mock_robot_service.db.collection().document().get.return_value = mock_doc
        
        # Act
        result = await mock_robot_service.update_robot(robot_id, update_data, "test-seller-id")
        
        # Assert
        assert result["name"] == "Updated Robot Name"
        assert result["description"] == "Updated description"
        assert result["pricing"]["basePrice"] == 55000
        mock_robot_service.db.collection().document().update.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_robot_success(self, mock_robot_service, sample_robot_data):
        """Test successful robot deletion."""
        # Arrange
        robot_id = "test-robot-id"
        seller_id = "test-seller-id"
        
        # Mock existing robot
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = sample_robot_data
        mock_robot_service.db.collection().document().get.return_value = mock_doc
        
        # Act
        result = await mock_robot_service.delete_robot(robot_id, seller_id)
        
        # Assert
        assert result is True
        mock_robot_service.db.collection().document().delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_robots_with_filters(self, mock_robot_service):
        """Test robot search with filters."""
        # Arrange
        search_filters = {
            "type": "robot",
            "minPrice": 10000,
            "maxPrice": 100000,
            "category": "industrial"
        }
        
        mock_robots = [
            {"id": "robot-1", "name": "Robot 1", "type": "robot", "pricing": {"basePrice": 50000}},
            {"id": "robot-2", "name": "Robot 2", "type": "robot", "pricing": {"basePrice": 75000}}
        ]
        
        mock_robot_service.db.collection().where().where().get.return_value = [
            Mock(to_dict=lambda: robot) for robot in mock_robots
        ]
        
        # Act
        result = await mock_robot_service.search_robots(search_filters)
        
        # Assert
        assert len(result) == 2
        assert all(robot["type"] == "robot" for robot in result)

    @pytest.mark.asyncio
    async def test_get_recommendations_for_user(self, mock_robot_service):
        """Test robot recommendations for user."""
        # Arrange
        user_id = "test-user-id"
        
        mock_recommendations = [
            {"id": "robot-1", "name": "Recommended Robot 1", "score": 0.95},
            {"id": "robot-2", "name": "Recommended Robot 2", "score": 0.87}
        ]
        
        with patch.object(mock_robot_service, '_calculate_recommendations', return_value=mock_recommendations):
            # Act
            result = await mock_robot_service.get_recommendations(user_id)
            
            # Assert
            assert len(result) == 2
            assert result[0]["score"] > result[1]["score"]  # Should be sorted by score

    @pytest.mark.asyncio
    async def test_manage_inventory_success(self, mock_robot_service, sample_robot_data):
        """Test inventory management."""
        # Arrange
        robot_id = "test-robot-id"
        inventory_data = {
            "available": 8,
            "reserved": 1,
            "total": 9
        }
        
        # Mock existing robot
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = sample_robot_data
        mock_robot_service.db.collection().document().get.return_value = mock_doc
        
        # Act
        result = await mock_robot_service.manage_inventory(robot_id, inventory_data)
        
        # Assert
        assert result is True
        mock_robot_service.db.collection().document().update.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_product_review(self, mock_robot_service, sample_robot_data):
        """Test adding product review."""
        # Arrange
        robot_id = "test-robot-id"
        review_data = {
            "userId": "test-user-id",
            "rating": 5,
            "comment": "Excellent robot, works perfectly!",
            "verified": True
        }
        
        # Mock existing robot
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = sample_robot_data
        mock_robot_service.db.collection().document().get.return_value = mock_doc
        
        # Act
        result = await mock_robot_service.handle_product_reviews(robot_id, review_data)
        
        # Assert
        assert result is True
        mock_robot_service.db.collection().document().update.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_product_analytics(self, mock_robot_service):
        """Test product analytics retrieval."""
        # Arrange
        robot_id = "test-robot-id"
        
        mock_analytics = {
            "views": 1250,
            "favorites": 45,
            "inquiries": 23,
            "purchases": 8,
            "conversionRate": 0.64,
            "averageRating": 4.5,
            "totalReviews": 12
        }
        
        with patch.object(mock_robot_service, '_calculate_product_analytics', return_value=mock_analytics):
            # Act
            result = await mock_robot_service.track_product_analytics(robot_id)
            
            # Assert
            assert result["views"] == 1250
            assert result["conversionRate"] == 0.64
            assert result["averageRating"] == 4.5

    @pytest.mark.asyncio
    async def test_get_robots_by_seller(self, mock_robot_service):
        """Test retrieving robots by seller."""
        # Arrange
        seller_id = "test-seller-id"
        
        mock_robots = [
            {"id": "robot-1", "sellerId": seller_id, "name": "Robot 1"},
            {"id": "robot-2", "sellerId": seller_id, "name": "Robot 2"}
        ]
        
        mock_robot_service.db.collection().where().get.return_value = [
            Mock(to_dict=lambda: robot) for robot in mock_robots
        ]
        
        # Act
        result = await mock_robot_service.get_robots_by_seller(seller_id)
        
        # Assert
        assert len(result) == 2
        assert all(robot["sellerId"] == seller_id for robot in result)

    @pytest.mark.asyncio
    async def test_update_robot_status(self, mock_robot_service, sample_robot_data):
        """Test robot status update."""
        # Arrange
        robot_id = "test-robot-id"
        new_status = "inactive"
        
        # Mock existing robot
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = sample_robot_data
        mock_robot_service.db.collection().document().get.return_value = mock_doc
        
        # Act
        result = await mock_robot_service.update_robot_status(robot_id, new_status)
        
        # Assert
        assert result is True
        mock_robot_service.db.collection().document().update.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_featured_robots(self, mock_robot_service):
        """Test featured robots retrieval."""
        # Arrange
        mock_featured_robots = [
            {"id": "robot-1", "name": "Featured Robot 1", "featured": True},
            {"id": "robot-2", "name": "Featured Robot 2", "featured": True}
        ]
        
        mock_robot_service.db.collection().where().limit().get.return_value = [
            Mock(to_dict=lambda: robot) for robot in mock_featured_robots
        ]
        
        # Act
        result = await mock_robot_service.get_featured_robots(limit=10)
        
        # Assert
        assert len(result) == 2
        assert all(robot["featured"] for robot in result)

    @pytest.mark.asyncio
    async def test_validate_robot_ownership(self, mock_robot_service, sample_robot_data):
        """Test robot ownership validation."""
        # Arrange
        robot_id = "test-robot-id"
        seller_id = "test-seller-id"
        
        # Mock existing robot
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = sample_robot_data
        mock_robot_service.db.collection().document().get.return_value = mock_doc
        
        # Act
        result = await mock_robot_service.validate_robot_ownership(robot_id, seller_id)
        
        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_robot_ownership_invalid(self, mock_robot_service, sample_robot_data):
        """Test robot ownership validation with invalid owner."""
        # Arrange
        robot_id = "test-robot-id"
        wrong_seller_id = "wrong-seller-id"
        
        # Mock existing robot
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = sample_robot_data
        mock_robot_service.db.collection().document().get.return_value = mock_doc
        
        # Act
        result = await mock_robot_service.validate_robot_ownership(robot_id, wrong_seller_id)
        
        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_cache_robot_data(self, mock_robot_service, sample_robot_data):
        """Test robot data caching."""
        # Arrange
        robot_id = "test-robot-id"
        
        # Act
        await mock_robot_service._cache_robot_data(robot_id, sample_robot_data)
        
        # Assert
        mock_robot_service.cache.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_cached_robot_data(self, mock_robot_service, sample_robot_data):
        """Test cached robot data retrieval."""
        # Arrange
        robot_id = "test-robot-id"
        mock_robot_service.cache.get.return_value = sample_robot_data
        
        # Act
        result = await mock_robot_service._get_cached_robot_data(robot_id)
        
        # Assert
        assert result == sample_robot_data
        mock_robot_service.cache.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_bulk_update_robots(self, mock_robot_service):
        """Test bulk robot updates."""
        # Arrange
        robot_ids = ["robot-1", "robot-2", "robot-3"]
        update_data = {"status": "inactive"}
        
        # Act
        result = await mock_robot_service.bulk_update_robots(robot_ids, update_data)
        
        # Assert
        assert result is True
        # Should call update for each robot
        assert mock_robot_service.db.collection().document().update.call_count == len(robot_ids)

    @pytest.mark.asyncio
    async def test_get_robot_categories(self, mock_robot_service):
        """Test robot categories retrieval."""
        # Arrange
        mock_categories = [
            {"name": "Industrial", "count": 25},
            {"name": "Service", "count": 18},
            {"name": "Educational", "count": 12}
        ]
        
        with patch.object(mock_robot_service, '_get_categories_with_counts', return_value=mock_categories):
            # Act
            result = await mock_robot_service.get_robot_categories()
            
            # Assert
            assert len(result) == 3
            assert result[0]["name"] == "Industrial"
            assert result[0]["count"] == 25
