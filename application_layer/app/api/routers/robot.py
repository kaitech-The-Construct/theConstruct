from typing import List

from api.samples.sample_data import robot_catalog
from core.services.robot_service import RobotService
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from schemas.robot import RobotCreate, RobotResponse, RobotUpdate
from utils.common import count_unique_items_by_key

router = APIRouter()
robot_service = RobotService()


@router.get("/")
async def get_services():
    """Service Response"""
    catalog_count = len(robot_catalog)
    manufacturer_count = count_unique_items_by_key(
        json_list=robot_catalog, key="manufacturer_id"
    )
    return JSONResponse(
        content={
            "message": "Welcome to Robot Catalog Service!",
            "count": f"There are currently {catalog_count} robot models.",
            "manufacturer_count": f"Number of manufacturers: {manufacturer_count}",
        }
    )


@router.post("/")
def create_robot(robot: RobotCreate):
    """
    Create a new robot and store it in the marketplace.
    """
    new_robot = robot_service.create_robot(robot_data=robot)
    return new_robot


@router.get("/list", response_model=List[RobotResponse])
async def list_robots():
    """
    Retrieve a list of all available robots in the marketplace.
    """
    robots = robot_service.get_all_robots()
    return robots


@router.get("/{robot_id}")
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


@router.get("/manufacturers", response_model=List[RobotResponse])
async def list_manufacturers():
    """
    Retrieve a list of all manufacturers in the marketplace.
    """
    manufacturers = robot_service.get_all_manufacturers()
    return manufacturers
