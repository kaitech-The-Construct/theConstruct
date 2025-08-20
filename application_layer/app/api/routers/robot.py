from typing import List

from core.services.robot_service import RobotService
from fastapi import APIRouter, HTTPException, status
from schemas.robot import RobotCreate, RobotResponse, RobotUpdate

router = APIRouter()
robot_service = RobotService()


@router.post("/", response_model=RobotResponse, status_code=status.HTTP_201_CREATED)
def create_robot(robot: RobotCreate):
    """
    Create a new robot and store it in the marketplace.
    """
    new_robot = robot_service.create_robot(robot_data=robot)
    return new_robot


@router.get("/", response_model=List[RobotResponse])
async def list_robots():
    """
    Retrieve a list of all available robots in the marketplace.
    """
    robots = robot_service.get_all_robots()
    return robots


@router.get("/{robot_id}", response_model=RobotResponse)
def get_robot(robot_id: str):
    """
    Get a single robot details by its ID.
    """
    robot = robot_service.get_robot_by_id(robot_id)
    if not robot:
        raise HTTPException(status_code=404, detail="Robot not found")
    return robot


@router.put("/{robot_id}", response_model=RobotResponse)
async def update_robot(robot_id: str, robot: RobotUpdate):
    """
    Update a robot's information.
    """
    updated_robot = robot_service.update_robot(robot_id, robot)
    if not updated_robot:
        raise HTTPException(status_code=404, detail="Unable to update listing")
    return updated_robot


@router.delete("/{robot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_robot(robot_id: str):
    """
    Delete a robot from the marketplace.
    """
    deleted = robot_service.delete_robot(robot_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Robot not found")
    return {"ok": True}


@router.get("/search", response_model=List[RobotResponse])
async def search_robots(
    min_price: float = None,
    max_price: float = None,
    manufacturer: str = None,
    category: str = None,
    min_rating: float = None
):
    """
    Advanced search for robots with filters.
    """
    filters = {}
    if min_price is not None:
        filters["min_price"] = min_price
    if max_price is not None:
        filters["max_price"] = max_price
    if manufacturer:
        filters["manufacturer"] = manufacturer
    if category:
        filters["category"] = category
    if min_rating is not None:
        filters["min_rating"] = min_rating
    
    robots = robot_service.advanced_search(filters)
    return robots


@router.get("/recommendations/{user_id}", response_model=List[RobotResponse])
async def get_recommendations(user_id: str):
    """
    Get product recommendations for a user.
    """
    recommendations = robot_service.get_recommendations(user_id)
    return recommendations


@router.post("/{robot_id}/reviews")
async def create_review(robot_id: str, review_data: dict):
    """
    Create a review for a robot.
    """
    success = robot_service.handle_product_reviews(robot_id, review_data)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create review"
        )
    return {"message": "Review created successfully"}


@router.get("/{robot_id}/reviews")
async def get_reviews(robot_id: str):
    """
    Get reviews for a robot.
    """
    # This would typically query the reviews collection
    # For now, return empty list as placeholder
    return {"reviews": []}


@router.get("/{robot_id}/analytics")
async def get_product_analytics(robot_id: str):
    """
    Get analytics for a product.
    """
    analytics = robot_service.track_product_analytics(robot_id)
    return analytics
