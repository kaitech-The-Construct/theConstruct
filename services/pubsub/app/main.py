from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import asyncio
import requests
from pydantic import BaseModel
from typing import List
from starlette.middleware.cors import CORSMiddleware

from concurrent.futures import ThreadPoolExecutor
from publisher.publisher import send_message_to_pubsub

from subscriptions.subscription_handler import process_pubsub_messages

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="app/templates")


class UrlData(BaseModel):
    urls: List[str]
    topic: str

@app.post("/scrape")
async def scrape(request: UrlData):
    # Send each URL as a message to Pub/Sub
    for url in request.urls:
        send_message_to_pubsub(url,request.topic)
        # print("Link: " + url)

    return {"message": "URLs queued for scraping"}

@app.get('/', response_class=HTMLResponse)
async def hello(request: Request):
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    return templates.TemplateResponse("index.html", {"request": request, "message": message, })


# Function to start the FastAPI application
def start_fastapi_server():
    # Get the server port from the environment variable
    server_port = os.environ.get("PORT", "8080")

    # Run the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=int(server_port))

if __name__ == "__main__":
    # Create a ThreadPoolExecutor to run the FastAPI server and Pub/Sub message processing concurrently
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Start the FastAPI server in one thread
        executor.submit(start_fastapi_server)

        # Start Pub/Sub message processing in another thread
        asyncio.run(process_pubsub_messages())
