import os

import uvicorn
from modules.identity import auth_router, user_router
from modules.market import trade_router, analytics_router, supply_chain_router, bounty_router
from modules.robotics import robot_router, design_router, manufacturing_router, software_router
from modules.ledger import blockchain_router
from modules.notifications import notifications_router
from modules.ai import ai_router
from modules.mcp import mcp_router
from core.middleware import rate_limit_middleware, security_headers_middleware, error_handling_middleware, request_logging_middleware
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Initializes FastAPI app instance
app = FastAPI(
    title="The Construct DEX", 
    version="1.0.0",
    description="Decentralized Robotics Exchange Platform",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mount the static directory to serve the index.html file
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Add security and utility middleware
app.middleware("http")(error_handling_middleware)
app.middleware("http")(security_headers_middleware)
app.middleware("http")(rate_limit_middleware)
app.middleware("http")(request_logging_middleware)

# Set up CORS middleware
from core.config.settings import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
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

# # Include routers from the new modules package
app.include_router(ai_router, prefix="/ai", tags=["ai"])
app.include_router(mcp_router, prefix="/mcp", tags=["mcp"])
app.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(blockchain_router, prefix="/blockchain", tags=["blockchain"])
app.include_router(manufacturing_router, prefix="/manufacturing", tags=["manufacturing"])
app.include_router(notifications_router, prefix="/notifications", tags=["notifications"])
app.include_router(robot_router, prefix="/robots", tags=["robots"])
app.include_router(software_router, prefix="/software", tags=["software"])
app.include_router(supply_chain_router, prefix="/supply-chain", tags=["supply_chain"])
app.include_router(design_router, prefix="/design", tags=["design"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(bounty_router, prefix="/bounties", tags=["bounties"])
app.include_router(trade_router, prefix="/trades", tags=["trades"])


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
