from fastapi import FastAPI
from file_transfer_api.src.api.routers.fastapi_router import router as fastapi_router

app = FastAPI()
app.include_router(fastapi_router, prefix="/files")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event('startup')  # Only runs on startup
async def on_start():
    print("Welcome!")
    # Eventually, this will take care of connecting to the database and the file system and testing the connection
