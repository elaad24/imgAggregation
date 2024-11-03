# The Redis Queue Path

| #   | From                   | To                     | To Queue Name        | What is Passing        |
| --- | ---------------------- | ---------------------- | -------------------- | ---------------------- |
| 1   | upload service         | ocr_service            | ocr_queue            | []strings (file names) |
| 2   | ocr_service            | classification_service | classification_queue | string (file name)     |
| 3   | classification_service | organizer_service      | organizer_queue      | JSON <Output_Info>     |

# Output_Info

## Attributes

```python
filename: str          # Name of the file
isNewDir: bool         # Indicates if the directory is new
toDir: str             # Target directory for the file
description: str       # Description of the directory's purpose
common_words: List[str] # List of common words associated with this directory
```
