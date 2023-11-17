import os
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from functions import count_unique_items_by_key
from models import SoftwareDetails
from sample_data import software_repository
from starlette.responses import JSONResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/services")
async def get_services():
    """Return service details"""
    repository_count = len(software_repository)
    author_count = count_unique_items_by_key(
        json_list=software_repository, key="author"
    )
    return JSONResponse(
        content={
            "message": "Welcome to the Software Repository Service!",
            "count": f"Number of software items: {repository_count}",
            "author_count": f"Number of authors: {author_count}",
        }
    )


@app.get("/software", response_model=List[SoftwareDetails])
async def get_all_software():
    """Return Software Repository List"""
    return software_repository


@app.get("/software/{software_id}", response_model=SoftwareDetails)
async def get_software(software_id: int):
    """Search by software ID"""
    if software_id <= 0 or software_id > len(software_repository):
        raise HTTPException(status_code=404, detail="Software not found")
    return software_repository[software_id - 1]


@app.post("/software", response_model=SoftwareDetails)
async def create_software(software: SoftwareDetails):
    """Create new software listing"""
    new_software = software.dict()
    new_software["documentation_url"] = ""
    software_repository.append(new_software)
    return new_software


@app.put("/software/{software_id}", response_model=SoftwareDetails)
async def update_software(software_id: int, updated_software: SoftwareDetails):
    """Update existing software listing"""
    if software_id <= 0 or software_id > len(software_repository):
        raise HTTPException(status_code=404, detail="Software not found")
    software_repository[software_id - 1] = updated_software.dict()
    return updated_software


@app.delete("/software/{software_id}", response_model=SoftwareDetails)
async def delete_software(software_id: int):
    """Remove software item from listing"""
    if software_id <= 0 or software_id > len(software_repository):
        raise HTTPException(status_code=404, detail="Software not found")
    deleted_software = software_repository.pop(software_id - 1)
    return deleted_software


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
