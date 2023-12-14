from typing import List, Dict
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse
from pathlib import Path
from routers import fastapi_file_router, fastapi_database_router, fastapi_router
from abstracts.exceptions_abstract import BaseCustomException

app = FastAPI()


@app.get("/")
async def root() :
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

#
# @dataclass
# class MyResponse:
#     filename: str
#     file_type: str
#     status: str
#     message: str
#
#
# @app.get("/")
# async def root() -> Dict[str, str]:
#     """This is the root endpoint of the API. It will return a simple message
#
#     Returns:
#         Dict: Message
#     """
#     return {"message": "Welcome to the API"}
#
#
# # @app.post("/files/")
#
#
# # @app.get("/download/{file_name}")
#
#
# @app.put("/files/{file_name}")
# async def update_file(file_name: str, file: UploadFile = File(...)) -> MyResponse:
#     """Updates a file on the server with a new file
#
#     Args:
#         file_name (str): Name of the file to update
#         file (UploadFile, optional): File to update. Defaults to File(...).
#
#     Returns:
#         Dict: File metadata and status or it will raise an exception if the file doesn't exist or the upload fails"""
#
#     # Check if the file exists
#     file_location = upload_dir / file_name
#     if file_location.is_file():
#         # Check if the new file is an image
#         if file.content_type.startswith("image/"):
#             # Save the file to the upload directory
#             with open(file_location, "wb") as f:
#                 f.write(await file.read())
#
#             return MyResponse(filename=file.filename, file_type=file.content_type, status="ok",
#                               message="File updated")
#         else:
#             # return {"status": "error", "message": "File must be an image"}
#             raise HTTPException(status_code=400, detail="File must be an image")
#     else:
#         raise HTTPException(status_code=404, detail=f"File {file_name} not found")
#
#

# @app.delete("/files/{file_name}")
# async def delete_file(file_name: str) -> Dict:
#     """Deletes a file
#
#     Args:
#         file_name (str): Name of the file to delete
#
#     Returns:
#         Dict: Status of the deletion"""
#     file_location = upload_dir / file_name
#     if file_location.is_file():
#         file_location.unlink()
#         return {"status": "ok", "message": f"File {file_name} deleted"}
#     else:
#         raise HTTPException(status_code=404, detail=f"File {file_name} not found")
#

#
#
# @app.get("/files/")
# async def list_all_files() -> List[Dict]:
#     """List all the files in the upload directory
#
#     Returns:
#         List[Dict]: List of file details in the upload directory"""
#     files_list = []
#     for file in upload_dir.iterdir():
#         files_list.append({"filename": file.name, "file_type": file.suffix, "file_size": file.stat().st_size})
#     return files_list
#
#
# @app.post("/upload_multi/")
# async def upload_multiple_files(files: List[UploadFile] = File(...)) -> List[Dict]:
#     """Upload multiple files to the server
#
#     Args:
#         files (List[UploadFile], optional): List of files to upload. Defaults to File(...).
#
#     Returns:
#         List[Dict]: List of file metadata and status"""
#     results = []
#     for file in files:
#         try:
#             results.append(await upload_file(file))
#         except HTTPException as e:
#             results.append({"status": "error", "message": str(e.detail)})
#     return results
#
#
# # Rationalise the endpoints - get rid of /files
#
# @app.delete("/delete_multi/")
# async def delete_multiple_files(files: List[str]) -> List[Dict]:
#     """Delete multiple files from the server
#
#     Args:
#         files (List[str]): List of files to delete
#
#     Returns:
#         List[Dict]: List of file metadata and status"""
#     results = []
#     for file in files:
#         try:
#             results.append(await delete_file(file))
#         except HTTPException as e:
#             results.append({"status": "error", "message": str(e.detail)})
#     # What would happen if I wanted to do a consistent delete - how would I handle this?
#     return results
#
#
# @app.on_event('startup')  # Only runs on startup
# async def on_start():
#     print("Hello!")
#
#
# # A fake comment
#
# # Fastapi routers
# # Try to keep your roots (routes) clear.
# # root = app.router
#

#
# # Create a small singleton pattern as below to write to the database
# class Test:
#     b = 'string'
#
#     def __init__(self, a):
#         self.a = a
#
