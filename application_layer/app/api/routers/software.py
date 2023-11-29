from typing import List

from api.samples.sample_data import software_repository
from core.services.software_service import SoftwareService
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from schemas.software import SoftwareCreate, SoftwareResponse, SoftwareUpdate
from utils.common import count_unique_items_by_key

router = APIRouter()


software_service = SoftwareService()


@router.get("/software_listings")
async def get_services():
    """Service Response"""
    catalog_count = len(software_repository)
    developer_count = count_unique_items_by_key(
        json_list=software_repository, key="author"
    )
    return JSONResponse(
        content={
            "message": "Welcome to Software Catalog Service!",
            "count": f"There are currently {catalog_count} available software services.",
            "developer_count": f"Number of developers: {developer_count}",
        }
    )


@router.post(
    "/create", response_model=SoftwareResponse, status_code=status.HTTP_201_CREATED
)
async def create_software(
    software_data: SoftwareCreate,
):
    """
    Create a new software listing.
    """
    new_software = software_service.create_software(software_data)
    if not new_software:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating software"
        )
    return new_software


@router.get("/", response_model=List[SoftwareResponse])
async def list_software():
    """
    Retrieve a list of all available software in the marketplace.
    """
    all_software = software_service.get_all_software()
    return all_software


@router.get("/{software_id}", response_model=SoftwareResponse)
async def get_software(software_id: str):
    """
    Get software details by software ID.
    """
    software = software_service.get_software_by_id(software_id)
    if not software:
        raise HTTPException(status_code=404, detail="Software not found")
    return software


@router.put("/{software_id}", response_model=SoftwareResponse)
async def update_software(
    software_id: str,
    software_data: SoftwareUpdate,
):
    """
    Update software details by software ID.
    """
    updated_software = software_service.update_software(software_id, software_data)
    if updated_software is None:
        raise HTTPException(status_code=404, detail="Software not found")
    return updated_software


@router.delete("/{version_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_software(version_id: str):
    """
    Delete software listing by version ID.
    """
    success = software_service.delete_software(version_id)
    if not success:
        raise HTTPException(status_code=404, detail="Software version not found")
    return {"ok": True}


# @router.get("/developers", response_model=List[RobotResponse])
# async def list_developers():
#     """
#     Retrieve a list of all developers in the marketplace.
#     """
#     developers = software_service.get_all_developers()
#     return developers
