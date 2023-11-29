from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from api.responses.errors import BadRequest, Forbidden, NotFound, ServerError, Unauthorized

app = FastAPI()

# Exception handler for BadRequest
@app.exception_handler(BadRequest)
async def bad_request_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Exception handler for Unauthorized
@app.exception_handler(Unauthorized)
async def unauthorized_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Exception handler for Forbidden
@app.exception_handler(Forbidden)
async def forbidden_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Exception handler for NotFound
@app.exception_handler(NotFound)
async def not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Exception handler for ServerError
@app.exception_handler(ServerError)
async def server_error_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

