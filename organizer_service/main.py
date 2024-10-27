import json
import os
import shutil
from typing import List

from pydantic import BaseModel


class Output_Info(BaseModel):
    filename: str
    isNewDir: bool
    toDir: str
    description: str
    common_words: List[str]


def organize_function(gptReturnObj: Output_Info):
    preSortPath = os.path.join(
        os.path.dirname(__file__), "..", "imagesFolder", "preSort"
    )
    sortedPath = os.path.join(os.path.dirname(__file__), "..", "imagesFolder", "sorted")
    if gptReturnObj["isNewDir"]:
        createDir(gptReturnObj["toDir"], sortedPath)

    dirPath = os.path.join(
        os.path.dirname(__file__), "..", "imagesFolder", "sorted", gptReturnObj["toDir"]
    )

    setInFolder(gptReturnObj["filename"], preSortPath, dirPath)

    updateFolderData(
        sortedPath,
        gptReturnObj["toDir"],
        gptReturnObj["description"],
        gptReturnObj["common_words"],
    )

    cleanup(gptReturnObj["filename"], preSortPath)


def createDir(dirname, sortedPath):
    if not os.path.exists(f"{sortedPath}/{dirname}"):
        newPath = os.path.join(sortedPath, dirname)
        os.mkdir(newPath)
    return


def setInFolder(filename, preSortDir, dirpath):
    filePath = os.path.join(preSortDir, filename)
    if os.path.exists(filePath):
        shutil.move(filePath, dirpath)


def updateFolderData(sortedPath, dirname, description, common_words):
    filePath = os.path.join(sortedPath, "info.json")
    with open(filePath, "r") as file:
        fileData = json.load(file)

    fileData[dirname] = {"description": description, "common_words": common_words}

    with open(filePath, "w") as file:
        json.dump(fileData, file, indent=1)


def cleanup(filename, preSortPath):
    preSortedImgPath = os.path.join(preSortPath, filename)
    ocrFilePath = os.path.join(
        os.path.dirname(__file__),
        "..",
        "classification_service",
        "text_files",
        f"{filename}.txt",
    )
    if os.path.exists(preSortedImgPath):
        os.remove(preSortedImgPath)
    if os.path.exists(ocrFilePath):
        os.remove(ocrFilePath)


a = {
    "filename": "Screenshot 2024-10-25 at 2.25.42.png",
    "isNewDir": False,
    "toDir": "exploration",
    "description": "A collection of files related to software exploration, including tests and service images.",
    "common_words": [
        "explorer",
        "classify",
        "tests",
        "images",
        "upload",
        "service",
        "docker",
        "cache",
        "venv",
        "repository",
    ],
}

organize_function(a)
