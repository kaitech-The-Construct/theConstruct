import os
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# Retrieve list of all available services
@app.get('/services')
async def getServices():
    try:
        response = getServiceList()
        return JSONResponse(response)
    except Exception as e:
        return JSONResponse({"error": str(e)})

# Retrieve details on specific service
@app.get('/services/{serviceId}')
async def getService(serviceId: str):
    try:
        response = getServiceDetails(serviceId)
        return JSONResponse(response)
    except Exception as e:
        return JSONResponse({"error": str(e)})

# Update service details
@app.put('/services/update/{serviceId}')
async def updateService(serviceId: str):
    try:
        response = updateServiceDetails(serviceId)
        return JSONResponse(response)
    except Exception as e:
        return JSONResponse({"error": str(e)})
    
# Create new service listing
@app.put('/services/update/{serviceId}')
async def createService(serviceId: str):
    try:
        response = createServiceListing(serviceId)
        return JSONResponse(response)
    except Exception as e:
        return JSONResponse({"error": str(e)})



###
###
###
@app.get('/', response_class=HTMLResponse)
async def hello(request: Request):
    """Return a friendly HTTP greeting."""
    message="It's running!"

    """Get Cloud Run environment variables."""
    service=os.environ.get('K_SERVICE', 'Unknown service')
    revision=os.environ.get('K_REVISION', 'Unknown revision')

    return templates.TemplateResponse("index.html", {"request": request, "message": message, "Service": service, "Revision": revision})


# Execute the application when the script is run
if __name__ == "__main__":
    # Get the server port from the environment variable
    server_port=os.environ.get("PORT", "8080")

    # Run the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=int(server_port))
