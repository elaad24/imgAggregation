# redis_helper.py
import json
import os

import redis

# Set up Redis connection
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
)


def push_to_queue(queue_name, message):
    """Push a JSON message to a specified Redis queue."""
    redis_client.rpush(queue_name, json.dumps(message))


def consume_from_queue(queue_name):
    """Pop a JSON message from a specified Redis queue."""
    message = redis_client.blpop(queue_name, timeout=0)
    if message:
        return json.loads(message[1])
    return None


#  the redis queue path

#   --------------------------------------------------------------------------------------------------------|
# | #  | from                   | to                     | to_queue_name        |   what_passing            |
# ----------------------------------------------------------------------------------------------------------|
# | 1  | upload service         | ocr_service            |  ocr_queue           |   []strings (file names)  |
# ----------------------------------------------------------------------------------------------------------|
# | 2  | ocr_service            | classification_service | classification_queue |   string (file name)      |
# ----------------------------------------------------------------------------------------------------------|
# | 3  | classification_service | organizer_service      |  organizer_queue     |   json <Output_Info>      |
#   --------------------------------------------------------------------------------------------------------|
# | 4  |


# Output_Info
#   filename: str
#     isNewDir: bool
#     toDir: str
#     description: str
#     common_words: List[str]


# todo: left to do -
# test it that it works
# build the docker compose
# ! make sure that the gpt does return the obejct with = , it need to return valud json format
