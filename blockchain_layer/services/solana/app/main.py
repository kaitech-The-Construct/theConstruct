import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import methods

# Initializes FastAPI app instance
app = FastAPI(title="Solana", version="1.0.0")

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

# # Include routers from the api.routers package
app.include_router(methods.router, prefix="/methods", tags=["methods"])


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
