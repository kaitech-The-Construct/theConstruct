import os
from datetime import datetime
from typing import Dict, Any

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import methods

# Initializes FastAPI app instance
app = FastAPI(
    title="XRPL Service", 
    version="1.0.0",
    description="XRPL blockchain integration service for The Construct platform"
)

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

# Standardized response format
class StandardResponse:
    @staticmethod
    def success(data: Any = None, message: str = "Success") -> Dict[str, Any]:
        return {
            "success": True,
            "message": message,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
            "service": "xrpl_service"
        }
    
    @staticmethod
    def error(message: str, error_code: str = "GENERAL_ERROR", details: Any = None) -> Dict[str, Any]:
        return {
            "success": False,
            "message": message,
            "error_code": error_code,
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
            "service": "xrpl_service"
        }

# Health check endpoints
@app.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return StandardResponse.success(
        data={"status": "healthy", "service": "xrpl_service"},
        message="Service is healthy"
    )

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint - checks if service is ready to handle requests"""
    try:
        # Add actual readiness checks here (database connection, XRPL connection, etc.)
        # For now, we'll just return ready
        return StandardResponse.success(
            data={
                "status": "ready",
                "service": "xrpl_service",
                "checks": {
                    "xrpl_connection": "healthy",
                    "database": "healthy"
                }
            },
            message="Service is ready"
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=StandardResponse.error(
                message="Service not ready",
                error_code="SERVICE_NOT_READY",
                details=str(e)
            )
        )

# Include routers from the api.routers package
app.include_router(methods.router, prefix="/api/v1", tags=["xrpl-methods"])

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=StandardResponse.error(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            details=str(exc)
        )
    )

# Define root route
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Return a friendly HTTP greeting."""
    message = "Welcome to The Construct XRPL Service API"

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "message": message,
        },
    )

if __name__ == "__main__":
    # Get the server port from the environment variable
    server_port = os.environ.get("PORT", "8001")

    # Run the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=int(server_port))
