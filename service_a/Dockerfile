# Use official, lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies (no-cache-dir keeps the image small)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose port 8000 (This is mostly for documentation, it doesn't publish the port)
EXPOSE 8000

# Command to run the application when the container starts
# We use 0.0.0.0 so it accepts connections from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
