from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from typing import Optional, List, Dict, Union
from pathlib import Path

app = FastAPI()
upload_dir = Path("data/uploads")


@app.post("/files/")
async def upload_file(file: UploadFile = File(...)) -> Dict:
    """Upload a file to the server

    Args:
        file (UploadFile, optional): File to upload. Defaults to File(...) but will largely be images.

    Returns:
        Dict: File metadata and status"""

    # Create the upload directory if it doesn't exist
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Check if the file is an image
    if file.content_type.startswith("image/"):

        # Save the file to the upload directory
        file_location = upload_dir / file.filename
        with open(file_location, "wb") as f:
            f.write(await file.read())

        return {"filename": file.filename, "file_type": file.content_type, "status": "ok", "message": "File uploaded"}
    else:
        # return {"status": "error", "message": "File must be an image"}
        raise HTTPException(status_code=400, detail="File must be an image")


@app.get("/download/{file_name}")
async def download_file(file_name:str) -> FileResponse:
    """Downloads a file from the server

    Args:
        file_name (str): Name of the file to download

    Returns:
        FileResponse: File to download or it will raise an exception if the file doesn't exist"""

    # Check if the file exists
    file_location = upload_dir / file_name
    if file_location.is_file():
        return FileResponse(file_location)
    else:
        raise HTTPException(status_code=404, detail=f"File {file_name} not found")


@app.put("/files/{file_name}")
async def update_file(file_name: str, file: UploadFile = File(...)) -> Dict:
    """Updates a file on the server with a new file

    Args:
        file_name (str): Name of the file to update
        file (UploadFile, optional): File to update. Defaults to File(...).

    Returns:
        Dict: File metadata and status or it will raise an exception if the file doesn't exist or the upload fails"""

    # Check if the file exists
    file_location = upload_dir / file_name
    if file_location.is_file():
        # Check if the new file is an image
        if file.content_type.startswith("image/"):
            # Save the file to the upload directory
            with open(file_location, "wb") as f:
                f.write(await file.read())

            return {"filename": file.filename, "file_type": file.content_type, "status": "ok", "message": "File updated"}
        else:
            # return {"status": "error", "message": "File must be an image"}
            raise HTTPException(status_code=400, detail="File must be an image")
    else:
        raise HTTPException(status_code=404, detail=f"File {file_name} not found")


@app.get("/files/")
async def list_all_files() -> List[Dict]:
    """List all the files in the upload directory

    Returns:
        List[Dict]: List of file details in the upload directory"""
    files_list = []
    for file in upload_dir.iterdir():
        files_list.append({"filename": file.name, "file_type": file.suffix, "file_size": file.stat().st_size})
    return files_list


@app.delete("/files/{file_name}")
async def delete_file(file_name: str) -> Dict:
    """Deletes a file

    Args:
        file_name (str): Name of the file to delete

    Returns:
        Dict: Status of the deletion"""
    file_location = upload_dir / file_name
    if file_location.is_file():
        file_location.unlink()
        return {"status": "ok", "message": "File deleted"}
    else:
        raise HTTPException(status_code=404, detail=f"File {file_name} not found")

