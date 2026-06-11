# service_a/main.py
from fastapi import FastAPI, HTTPException

# Create the FastAPI application. This is our "server" object.
app = FastAPI()

# A simple "database" using a Python dictionary.
# In a real app, this would be a real database like PostgreSQL or MongoDB.
USER_DATABASE = {
    1: {"name": "Alice", "role": "Admin"},
    2: {"name": "Bob", "role": "Developer"}
}

# Endpoint 1: The Root/Home endpoint
# This is what you see if you just visit the base URL (e.g., http://localhost:8000/)
@app.get("/")
def read_root():
    return {"message": "Welcome to Service A (The User Data Service)"}

# Endpoint 2: The Health Check
# Other services or load balancers call this to check if our service is alive.
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Endpoint 3: Get a user by their ID
# The {user_id} in the path is a variable that FastAPI will read for us.
@app.get("/users/{user_id}")
def get_user(user_id: int):
    # Try to find the user in our simple dictionary
    user = USER_DATABASE.get(user_id)
    
    # If the user is not found, return a 404 Error (Not Found)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # If found, return the user data as a JSON response
    return user
