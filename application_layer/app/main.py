import os

import uvicorn
from api.routers import robot, software, trade
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Initializes FastAPI app instance
app = FastAPI(title="The Construct DEX", version="1.0.0")

# Mount the static directory to serve the index.html file
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handler for error responses
def error_response_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


# Register exception handlers
app.add_exception_handler(HTTPException, error_response_handler)

# # Include routers from the api.routers package
app.include_router(robot.router, prefix="/robots", tags=["robots"])
app.include_router(software.router, prefix="/software", tags=["software"])
# app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(trade.router, prefix="/trades", tags=["trades"])
# app.include_router(governance.router, prefix="/governance", tags=["governance"])


# Define root route
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Return a friendly HTTP greeting."""
    message = "Welcome to The Construct DEX API"

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "message": message,
        },
    )


if __name__ == "__main__":
    # Get the server port from the environment variable
    server_port = os.environ.get("PORT", "8080")

    # Run the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=int(server_port))
