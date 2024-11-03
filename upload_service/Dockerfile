# Step 1: Use an official Python image as the base image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file and install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the entire microservice code into the container
COPY . .

# Step 5: copy the entrypoint .sh script from the build context 
COPY ./entry_scripts/imagesFolder.sh /app/entrypoint.sh

# Step 6: Ensure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Step 7: Expose the port your FastAPI app will run on (e.g., 8000)
EXPOSE 8000

# Step 9: Specify the command to start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]