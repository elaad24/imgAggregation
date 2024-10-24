import os
import shutil
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI()


@app.get("/")
def root():
    return {"all good": "still running"}


UPLOAD_DIR = Path("../imagesFolder/preSort")


@app.post("/uploadImg")
async def upload_file(files: list[UploadFile] = File(...)):
    saved_file_info = []
    for file in files:
        file_extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
        if not file_extension:
            return HTTPException(
                status_code=400,
                detail=f"File format not supported for file {file.filename}",
            )
        file_path = UPLOAD_DIR / file.filename

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            file_size = file_path.stat().st_size
            saved_file_info.append(
                {
                    "filename": file.filename,
                    "file_size": file_size,
                    "message": "File upload successful",
                }
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error saving file {file.filename} : {str(e)}"
            )

    return saved_file_info
