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


# ocr queue - getting : arr of fileNames
# ocr queue - ocr_queue -> passing: arr of fileNames
# classification queue - classification_queue -> passing object Output_Info as a string
# organizer queue - organizer_queue
#

# Output_Info
#   filename: str
#     isNewDir: bool
#     toDir: str
#     description: str
#     common_words: List[str]


# todo: left to do -
# add redis to the type script part (ocr)
# test it that it works
# build the docker compose
# ! make sure that the gpt does return the obejct with = , it need to return valud json format
