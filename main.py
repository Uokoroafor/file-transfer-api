from fastapi import FastAPI
from api.fastapi_router import router as fastapi_router

app = FastAPI()
app.include_router(fastapi_router, prefix="/files")


@app.get("/")
async def root():
    return {"message": "Hello World"}
