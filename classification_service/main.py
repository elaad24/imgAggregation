import json
import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
client = OpenAI(api_key=os.getenv("CHAT_GPT_SECRET"))


class Output_Info(BaseModel):
    isNewDir: bool
    toDir: str
    description: str
    common_words: List[str]


def send_data_to_gpt(file_name):
    dirs_path = Path(
        os.path.join(os.path.dirname(__file__), "..", "imagesFolder", "sorted")
    )

    directories_object_array = get_directories(dirs_path)

    dir_info_file_path = os.path.join(
        os.path.dirname(__file__), "..", "imagesFolder", "sorted", "info.json"
    )

    with open(dir_info_file_path, "r") as info_file:
        dir_info_file = info_file.read()

    ocr_file_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "classification_service",
        "text_files",
        f"{file_name}.txt",
    )

    with open(ocr_file_path, "r") as ocr_file:
        ocr_file_text = ocr_file.read()

    gpt_input_data = {
        "dir_data": {
            "directories": directories_object_array,
            "directories_info": dir_info_file,
        },
        "file_text": ocr_file_text,
    }

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are a helpful assistant that its task it to decide in which directory the file should be stored.
                you get array of objects.

                example input structure:
                {
                    "dir_data": {
                        "directories": [
                        {"name": "string"},
                        {"name": "string"},
                        {"name": "string"}
                        ],
                        "directories_info": {
                        ["dir_name"] : {
                            "description": "string",
                            "common_words": "string"
                        }
                        }
                    },
                    "file_text": "string"
                    }


                each object contain.
                name: the name of folder ,
                description: what  kind of data in the files that in it,
                common_words: array of common words that in the files in that folder.
                and also you get - 
                file_text: the text that in that file.

                your job is to decide in which folder the file should be stored base on it context and by the common_words,
                after that new file is added to that folder, update the description , and the common_words so it will be include the new file data as well,
                in the description update it so, it be general description of the files AND the new file ,
                in the common_words add pick just couple (less then 10) words from the file that in the essence of the file.
                and if you think that the file doesn't fit in any of the folders,
                you can decide to open new folder and pick it name, and create its description, and common_words.
                
                output:          
                you need to return the data as following,
                  {
                    isNewDir:boolean, // if you decide that need to open new directory for the file.
                    toDir:string,  // the name of the directory that the file needs to be stored in.
                    description:string,  // the description of the directory that you got in the request, or the updated one in case you decide to change it.
                    common_words:[]string // array or strings, the common words that you get in the request, or the updated one in case you change it, 
                  }
                   *** return only the output object and nothing more then that and as json format . 
                     ** the common_words should be include determiner words and numbers, common_words should be words that could help you to determine if the file is in common with the folder as well of the description.

                    *** how to decide where the file should be stored:
                        use the description and the common_words and decide if it fit in that directory.
                    """,
            },
            {
                "role": "user",
                "content": json.dumps(gpt_input_data),
            },
        ],
        response_format=Output_Info,
    )
    print("-------------------------")
    print(completion.choices[0].message.parsed)
    return completion.choices[0].message.parsed


def get_directories(path):
    items = os.listdir(path)

    directories = [
        {"name": dir_name}
        for dir_name in items
        if os.path.isdir(os.path.join(path, dir_name))
    ]
    return directories


send_data_to_gpt("Screenshot 2024-10-25 at 2.25.42.png")
