from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.abstracts.exceptions_abstract import BaseCustomException
from app.routers import fastapi_file_router
from app.routers import fastapi_database_router, fastapi_router

app = FastAPI()


@app.get("/")
async def root():
    """This is the root endpoint of the API. It will return a simple message

    Returns:
        A message welcoming the user to the API
    """
    return {"test_1": 200, "test_value": "some more text"}


app.include_router(fastapi_file_router.router, prefix="/files", tags=["File Operations"])
app.include_router(fastapi_database_router.router, prefix="/database", tags=["Database Operations"])
app.include_router(fastapi_router.router, prefix="/full", tags=["Full API Operations"])


@app.exception_handler(BaseCustomException)
async def custom_exception_handler(request: Request, exc: BaseCustomException):
    """Custom exception handler for BaseCustomException.

    Args:
        request (Request): Request object
        exc (BaseCustomException): BaseCustomException object

    Returns:
        A JSON response with the exception details.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.description, "name": exc.name},
    )


@app.on_event('startup')  # Only runs on startup
async def on_start():
    print("Welcome!")