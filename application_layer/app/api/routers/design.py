from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from utils.common import count_unique_items_by_key

from core.services.design_service import DesignService
from schemas.designs import (DesignCreate,
                                                   DesignResponse,
                                                   DesignUpdate)

from ..samples.sample_data import design_catalog

router = APIRouter()
design_service = DesignService()


@router.get("/")
async def get_services():
    """Service Response"""
    catalog_count = len(design_catalog)
    manufacturer_count = count_unique_items_by_key(
        json_list=design_catalog, key="manufacturer_id"
    )
    return JSONResponse(
        content={
            "message": "Welcome to Design Catalog Service!",
            "count": f"There are currently {catalog_count} design models.",
            "manufacturer_count": f"Number of designers: {manufacturer_count}",
        }
    )


@router.post("/")
def create_design(design: DesignCreate):
    """
    Create a new design and store it in the marketplace.
    """
    new_design = design_service.create_design(design_data=design)
    return new_design


@router.get("/list", response_model=List[DesignResponse])
async def list_designs():
    """
    Retrieve a list of all available designs in the marketplace.
    """
    designs = design_service.get_all_designs()
    return designs


@router.get("/{design_id}")
def get_design(design_id: str):
    """
    Get a single design details by its ID.
    """
    design = design_service.get_design_by_id(design_id)
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    return design


@router.put("/{design_id}", response_model=DesignResponse)
async def update_design(design_id: str, design: DesignUpdate):
    """
    Update a design's information.
    """
    updated_design = design_service.update_design(design_id, design)
    if not updated_design:
        raise HTTPException(status_code=404, detail="Unable to update listing")
    return updated_design


@router.delete("/{design_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_design(design_id: str):
    """
    Delete a design from the marketplace.
    """
    deleted = design_service.delete_design(design_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Design not found")
    return {"ok": True}


@router.get("/designers", response_model=List[DesignResponse])
async def list_designers():
    """
    Retrieve a list of all designers in the marketplace.
    """
    designers = design_service.get_all_designers()
    return designers
