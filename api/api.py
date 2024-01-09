from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from api.routers.fastapi_router import router as fastapi_router

app = FastAPI()
app.include_router(fastapi_router, prefix="/files")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.exception_handler(HTTPException)
async def custom_exception_handler(request: Request, exc: HTTPException):
    """Custom exception handler for BaseCustomException.

    Args:
        request (Request): Request object
        exc (BaseCustomException): BaseCustomException object

    Returns:
        A JSON response with the exception details.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


@app.on_event('startup')  # Only runs on startup
async def on_start():
    print("Welcome!")
    # Eventually this will take care of connecting to the database and the file system and testing the connection
