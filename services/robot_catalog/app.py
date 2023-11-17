import os
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from functions import count_unique_items_by_key
from models import RobotDetails
from sample_data import robot_catalog
from starlette.responses import JSONResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/services")
async def get_services():
    """Service Response"""
    catalog_count = len(robot_catalog)
    manufacturer_count = count_unique_items_by_key(json_list=robot_catalog, key="manufacturer_id")
    return JSONResponse(
        content={
            "message": "Welcome to Robot Catalog Service!",
            "count": f"There are currently {catalog_count} robot models.",
            "manufacturer_count": f"Number of manufacturers: {manufacturer_count}"
        }
    )


@app.get("/robots", response_model=List[RobotDetails])
async def get_robots():
    """Retrieve Robot List"""
    return robot_catalog


@app.get("/robots/{robot_id}", response_model=RobotDetails)
async def get_robot(robot_id: int):
    """Search by robot ID"""
    if robot_id <= 0 or robot_id > len(robot_catalog):
        raise HTTPException(status_code=404, detail="Robot not found")
    return robot_catalog[robot_id - 1]


@app.post("/robots", response_model=RobotDetails)
async def create_robot(robot: RobotDetails):
    """Create new robot listing"""
    new_robot = robot.dict()
    new_robot["id"] = len(robot_catalog) + 1
    robot_catalog.append(new_robot)
    return new_robot


@app.put("/robots/{robot_id}", response_model=RobotDetails)
async def update_robot(robot_id: int, updated_robot: RobotDetails):
    """Update existing robot item"""
    if robot_id <= 0 or robot_id > len(robot_catalog):
        raise HTTPException(status_code=404, detail="Robot not found")
    robot_catalog[robot_id - 1] = updated_robot.dict()
    robot_catalog[robot_id - 1]["id"] = robot_id
    return updated_robot


@app.delete("/robots/{robot_id}", response_model=RobotDetails)
async def delete_robot(robot_id: int):
    """Remove robot item from catalog"""
    if robot_id <= 0 or robot_id > len(robot_catalog):
        raise HTTPException(status_code=404, detail="Robot not found")
    deleted_robot = robot_catalog.pop(robot_id - 1)
    return deleted_robot


@app.get("/", response_class=HTMLResponse)
async def hello(request: Request):
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    service = os.environ.get("K_SERVICE", "Unknown service")
    revision = os.environ.get("K_REVISION", "Unknown revision")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "message": message,
            "Service": service,
            "Revision": revision,
        },
    )


# Execute the application when the script is run
if __name__ == "__main__":
    # Get the server port from the environment variable
    server_port = os.environ.get("PORT", "8080")

    # Run the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=int(server_port))
