import json
import os
import shutil
from typing import List

from pydantic import BaseModel
from redis_helper import consume_from_queue


class Output_Info(BaseModel):
    filename: str
    isNewDir: bool
    toDir: str
    description: str
    common_words: List[str]


# Path to the volume directory
basePathForImagesFolder = "/app/imagesFolder"
base_path_for_output_textFiles = "/app/text_files"


def organize_function(gptReturnObj: Output_Info):
    #  for local usage
    # preSortPath = os.path.join(
    #     os.path.dirname(__file__), "..", "imagesFolder", "preSort"
    # )
    preSortPath = os.path.join(basePathForImagesFolder, "preSort")
    #  for local usage
    # sortedPath = os.path.join(os.path.dirname(__file__), "..", "imagesFolder", "sorted")
    sortedPath = os.path.join(basePathForImagesFolder, "sorted")

    if gptReturnObj["isNewDir"]:
        createDir(gptReturnObj["toDir"], sortedPath)
    # for local usage
    # dirPath = os.path.join(
    #     os.path.dirname(__file__), "..", "imagesFolder", "sorted", gptReturnObj["toDir"]
    # )

    # for local usage
    # dirPath = os.path.join(
    #     os.path. dirname(__file__), "..", "imagesFolder", "sorted", gptReturnObj["toDir"]
    # )
    dirPath = os.path.join(basePathForImagesFolder, "sorted", gptReturnObj["toDir"])

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
    # for local usage
    # ocrFilePath = os.path.join(
    #     os.path.dirname(__file__),
    #     "..",
    #     "classification_service",
    #     "text_files",
    #     f"{filename}.txt",

    ocrFilePath = os.path.join(
        base_path_for_output_textFiles,
        f"{filename}.txt",
    )
    if os.path.exists(preSortedImgPath):
        os.remove(preSortedImgPath)
    if os.path.exists(ocrFilePath):
        os.remove(ocrFilePath)


# handle the listening for message and trigger them
def listen_to_queue(queue_name):
    print(f"Listening to {queue_name} queue...")
    while True:
        message = consume_from_queue(queue_name)
        if message:
            print("new message is here ", message)
            organize_function(json.loads(message))


listen_to_queue("organizer_queue")
