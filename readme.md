# Images Organiser

A sophisticated microservices architecture for sorting images based on scraped file information and then implementing queries to OpenAI's ChatGPT for cataloging the files. This system integrates Redis queues, Docker, Python for internal processes, FastAPI for handling requests, and a Node.js service for Optical Character Recognition (OCR) using Tesseract.

## Overview

The **Images Organiser** project automates the process of sorting and cataloging images by scraping metadata and file information, then sending this data to OpenAI's ChatGPT to generate meaningful categorizations. The entire architecture is built on microservices, leveraging Redis for queuing tasks, Docker for containerization, and OCR capabilities for image content analysis. This project is designed to handle a high volume of images asynchronously, ensuring scalability and modularity.

### Key Components:

- **Redis Queue**: Manages the asynchronous processing of tasks, ensuring images and their metadata are handled efficiently across different microservices.
- **Docker**: Containerization of the entire system, including Python-based microservices, FastAPI, Redis, and Node.js OCR service.
- **Microservices in Python**: Handle scraping metadata, querying OpenAI’s ChatGPT, and processing image categorization tasks asynchronously.
- **FastAPI**: Serves as the entry point for external API requests, routing image data to the appropriate internal services.
- **Node.js OCR Service**: Runs an internal process using Tesseract to extract text from images when necessary, contributing additional metadata for categorization.

## Architecture

This system is built around a microservices architecture, with each service focused on a specific part of the image processing pipeline. The Redis queue ensures tasks such as scraping metadata, querying ChatGPT, and categorizing images are handled efficiently in the background. FastAPI serves as the interface for file uploads and initiates the processing workflow.

### Core Services:

1. **Python Microservices**:

   - **File Scraping & Metadata Extraction**: Extracts useful metadata from image files, which is then used to query OpenAI’s ChatGPT to generate insightful categorizations.
   - **Redis Queue Listener**: A background process that listens to Redis queues for incoming image processing tasks.

2. **FastAPI Server**:

   - Acts as the central interface for uploading images and initiating the sorting and cataloging workflow.
   - Sends extracted metadata to OpenAI's ChatGPT for further categorization and stores results for easy access.

3. **Node.js OCR Service**:
   - Extracts text from images using Tesseract when relevant metadata is missing or incomplete.
   - Adds OCR results to the image’s metadata, which can further enhance the categorization process via ChatGPT.

## Redis Queue Implementation

Redis plays a crucial role in ensuring tasks are handled asynchronously, allowing multiple images to be processed concurrently without blocking the system. Redis queues ensure that the system can scale efficiently, even under a heavy load of image files.

### Queue Process:

- **Image Upload**: When an image is uploaded, metadata is scraped and the data is pushed to a Redis queue for processing.
- **Task Distribution**: The Python microservices listen to Redis queues, waiting for tasks to arrive. Upon receiving a task, they query OpenAI’s ChatGPT and return the categorization results.
- **OCR Integration**: If an image requires text extraction, the task is forwarded to the Node.js OCR service, which processes it and updates the queue.

## Docker Setup

All services are containerized using Docker, allowing for easy deployment and scalability. Each service runs in its own container, ensuring that they remain isolated and can be managed independently.

- **Docker Compose**: Orchestrates the multi-container setup. FastAPI, Redis, Python microservices, and the Node.js OCR service run in their own containers, communicating through the Docker network.

### Starting the Services

To run the entire system, use the following command:

```bash
docker-compose up --build
```

This will build and start all containers, making the system ready to handle image uploads and categorization.

## How it Works

1. **Uploading an Image**: Users can upload images through the FastAPI interface. The file is processed to extract metadata (file name, size, etc.), and the information is pushed to a Redis queue.
2. **Metadata Scraping & ChatGPT Querying**: Python microservices listen for new tasks in the queue. Once they receive a task, they scrape metadata and use it to query OpenAI’s ChatGPT, which returns categorization information.
3. **OCR for Text Extraction**: If the image contains text, or additional metadata is needed, the image is processed by the Node.js OCR service using Tesseract. The extracted text is included in the metadata sent to ChatGPT.

4. **Cataloging Results**: The final categorization results are stored and made available for further use, providing structured, searchable data for each image.

5. **Organizer And cleanup**: The final stage that it get the info based on the response form open ai api, and put the file in the correct place and update the files and remove the un nurseries files

## The Redis Queue Path dataflow

| #   | From                   | To                     | To Queue Name        | What is Passing        |
| --- | ---------------------- | ---------------------- | -------------------- | ---------------------- |
| 1   | upload service         | ocr_service            | ocr_queue            | []strings (file names) |
| 2   | ocr_service            | classification_service | classification_queue | string (file name)     |
| 3   | classification_service | organizer_service      | organizer_queue      | JSON <Output_Info>     |

---

### Output_Info object

```python
filename: str          # Name of the file
isNewDir: bool         # Indicates if the directory is new
toDir: str             # Target directory for the file
description: str       # Description of the directory's purpose
common_words: List[str] # List of common words associated with this directory
```

---

## Features

- **Automated Image Categorization**: Metadata scraping combined with ChatGPT queries ensures that each image is accurately categorized based on its content and metadata.
- **Asynchronous Processing**: Redis queues ensure that large volumes of images can be processed asynchronously, improving performance and scalability.
- **OCR Integration**: Text is extracted from images using Tesseract, which adds to the image’s metadata and enhances the categorization process.
- **Fully Containerized**: Docker ensures that each service runs in its own container, making it easy to manage, deploy, and scale.

## Technologies Used

- **Python**: For microservices handling scraping, task processing, and interaction with OpenAI’s ChatGPT.
- **FastAPI**: For building the API that handles file uploads and routes tasks to the appropriate microservices.
- **Node.js**: Running the OCR service using the Tesseract library to extract text from images.
- **Redis**: For asynchronous task queuing and communication between services.
- **Docker**: For containerizing all services and orchestrating them via Docker Compose.
- **Tesseract**: Open-source OCR engine used to extract text from images in the Node.js service.
- **OpenAI's ChatGPT**: Used to intelligently categorize images based on their metadata.

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose

### Steps to Run

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Start the application with Docker Compose:

   ```bash
   docker-compose up --build
   ```

3. The services will now be running, and you can interact with the FastAPI server at:
   ```bash
   http://localhost:8000
   ```

## Conclusion

The **Images Organiser** project showcases a highly modular microservices architecture designed to automate the process of image categorization. It integrates Redis for asynchronous task processing, Docker for easy deployment, and advanced AI-driven categorization through OpenAI’s ChatGPT. By leveraging OCR and metadata scraping, this system provides a robust solution for organizing large volumes of image files.

---

Let me know if you need any further adjustments!
