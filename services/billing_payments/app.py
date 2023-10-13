import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

templates=Jinja2Templates(directory="app/templates")

# Create invoice for a service
@app.post('/invoices')
async def func():
    try:
        response = createInvoice()
        return JSONResponse(response)
    except Exception as e:
        return JSONResponse({"error": str(e)})

# Retrieve invoice details
@app.get('/invoices/{invoiceId}')
async def func(serviceId: str):
    try:
        response = getInvoiceDetails(serviceId)
        return JSONResponse(response)
    except Exception as e:
        return JSONResponse({"error": str(e)})

# Initiate a payment
@app.post('/payments')
async def func():
    try:
        response = initiatePayment()
        return JSONResponse(response)
    except Exception as e:
        return JSONResponse({"error": str(e)})

# Retrieve details on a payment
@app.get('/payments/{paymentsId}')
async def func(serviceId: str):
    try:
        response = getPayments(serviceId)
        return JSONResponse(response)
    except Exception as e:
        return JSONResponse({"error": str(e)})


# Retrieve users invoices
@app.put('/user/{userId}/{invoices}')
async def func(serviceId: str):
    try:
        response = getUserInvoice(serviceId)
        return JSONResponse(response)
    except Exception as e:
        return JSONResponse({"error": str(e)})
    
# Retrieve user payment history
@app.put('/user/{userId}/{payments}')
async def func(serviceId: str):
    try:
        response = getUserPaymentHistory(serviceId)
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
