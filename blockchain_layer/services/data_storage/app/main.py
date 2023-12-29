"""
Firestore Database Service
"""
import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from firestore_db import write_data_to_firestore, write_wallet_address_to_firestore
from schema import DataModel, EventModel


app = FastAPI()

baseUrl = os.getenv("_BASEURL")
defaultUrl = os.getenv("_DEFAULT_URL")

# Enable CORS for all origins (testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.post("/saveAddress")
async def save_address(request:DataModel):
    """Saves a wallet address to Firestore.

    Args:
        request (Request): The request object.

    Returns:
        dict: The response object.
    """
    try:

        # Extract the wallet address from the body
        wallet_address = request

        # Write the wallet address to Firestore
        response = write_wallet_address_to_firestore(wallet_address)

        return {"message": response}
    except Exception as e:
        return {"error": str(e)}


@app.post("/saveData")
async def save_data(request: EventModel):
    """Saves data to Firestore.

    Args:
        request (Request): The request object.

    Returns:
        dict: The response object.
    """
    try:
  
        # Write data to database
        response = write_data_to_firestore(request)
        return response
    except Exception as e:
        return {"error": str(e)}


@app.get("/", response_class=HTMLResponse)
async def hello(request: Request):
    """Return a friendly HTTP greeting."""
    message = "This service is running!"

    return templates.TemplateResponse(
        "index.html", {"request": request, "message": message}
    )


# Execute the application when the script is run
if __name__ == "__main__":
    # Get the server port from the environment variable
    server_port = os.environ.get("PORT", "8080")

    # Run the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=int(server_port))
