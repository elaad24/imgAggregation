# Step 1: Use an official Python image as the base image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file and install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the entire microservice code into the container
COPY . .

# Step 5: Specify the command to start the application
CMD ["python","-u", "main.py"]
