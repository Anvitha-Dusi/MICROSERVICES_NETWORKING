# service_b/main.py
from fastapi import FastAPI, HTTPException
import requests
import os

# Create the FastAPI application for Service B.
app = FastAPI()

# This is the URL where Service A will be running. 
# We use an Environment Variable so it works in the Cloud (Render) or locally.
SERVICE_A_URL = os.getenv("SERVICE_A_URL", "http://service-a:8000")

# Endpoint 1: The Root/Home endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Service B (The Greeting Service)"}

# Endpoint 2: The Health Check
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Endpoint 3: Greet a user by their ID
# This endpoint shows how MICROSERVICES COMMUNICATE.
@app.get("/greet/{user_id}")
def greet_user(user_id: int):
    # Step 1: Make a network request to Service A to get the user's details.
    # We use the Python 'requests' library to act like a client calling an API.
    try:
        response = requests.get(f"{SERVICE_A_URL}/users/{user_id}")
    except requests.exceptions.ConnectionError:
        # If Service A is not running, we catch the error gracefully
        raise HTTPException(status_code=500, detail="Could not connect to Service A. Is it running?")

    # Step 2: Check if Service A successfully found the user
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="User not found in Service A")
        
    # Step 3: Extract the JSON data from Service A's response
    # Service A returned: {"name": "Alice", "role": "Admin"}
    user_data = response.json()
    user_name = user_data.get("name")
    
    # Step 4: Create a greeting and return it as our own JSON response
    return {"greeting": f"Hello {user_name}! Welcome to the microservices world."}
