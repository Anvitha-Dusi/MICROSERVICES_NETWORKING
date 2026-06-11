from fastapi import FastAPI, Request, HTTPException
import requests
import time
from datetime import datetime
import os

app = FastAPI()

# --- CONFIGURATION ---

# IP Whitelist: Only these IP addresses are allowed to use our Gateway.
# 127.0.0.1 is your local computer (localhost).
ALLOWED_IPS = ["127.0.0.1"]

# Rate Limiter Data Store
# We will use a simple dictionary to keep track of requests.
# Format: {"127.0.0.1": {"count": 1, "last_request_time": 1690000000.0}}
RATE_LIMIT_STORE = {}

# Backend Services Destinations (Using Environment Variables for Cloud readiness)
# It will default to the local Docker Compose URLs if the variables are not set.
SERVICE_A_URL = os.getenv("SERVICE_A_URL", "http://service-a:8000")
SERVICE_B_URL = os.getenv("SERVICE_B_URL", "http://service-b:8001")


# --- MIDDLEWARE (Security & Logging) ---

# Middleware is a function that runs before every single request.
@app.middleware("http")
async def security_and_logging_middleware(request: Request, call_next):
    client_ip = request.client.host

    # 1. IP WHITELIST CHECK (Disabled for Docker Phase)
    # Because Docker routes traffic through an internal virtual network,
    # the client IP changes to a Docker Bridge IP, so we disable this strict check for now.
    # if client_ip not in ALLOWED_IPS:
    #     print(f"[{datetime.now()}] BLOCKING: Unauthorized IP address: {client_ip}")
    #     from fastapi.responses import JSONResponse
    #     return JSONResponse(status_code=403, content={"detail": "IP address not allowed"})

    # 2. RATE LIMITER CHECK
    current_time = time.time()
    
    # If we haven't seen this IP before, add it to our store
    if client_ip not in RATE_LIMIT_STORE:
        RATE_LIMIT_STORE[client_ip] = {"count": 0, "last_request_time": current_time}

    ip_data = RATE_LIMIT_STORE[client_ip]
    
    # Check if 1 second has passed since their last request.
    # If yes, reset their count to 0.
    if current_time - ip_data["last_request_time"] > 1.0:
        ip_data["count"] = 0
        ip_data["last_request_time"] = current_time

    # Increment the request count
    ip_data["count"] += 1

    # Check if they exceeded 5 requests in the last second
    if ip_data["count"] > 5:
        print(f"[{datetime.now()}] RATE LIMIT EXCEEDED: Blocking IP {client_ip}")
        # Return 429 Too Many Requests
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=429, content={"detail": "Too many requests. Slow down!"})

    # 3. LATENCY TRACKING (Start time)
    start_time = time.time()

    # Pass the request to the actual route handler (the API Gateway logic below)
    response = await call_next(request)

    # 4. LATENCY TRACKING (End time)
    end_time = time.time()
    latency_ms = (end_time - start_time) * 1000
    
    print(f"[{datetime.now()}] REQUEST LOG: IP: {client_ip} | Path: {request.url.path} | Latency: {latency_ms:.2f}ms")

    return response


# --- API GATEWAY & REVERSE PROXY ROUTING ---

# This is a "catch-all" route. It intercepts any URL path sent to the Gateway.
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def reverse_proxy(request: Request, path: str):
    
    # Step 1: Inspect the request path to decide where to route it
    if path.startswith("service-a"):
        # Example: /service-a/users/1 -> /users/1
        # We strip the "service-a" part to get the real endpoint for Service A
        forward_path = path.replace("service-a", "", 1) 
        target_url = f"{SERVICE_A_URL}{forward_path}"
        
    elif path.startswith("service-b"):
        forward_path = path.replace("service-b", "", 1)
        target_url = f"{SERVICE_B_URL}{forward_path}"
        
    else:
        # If the path doesn't match our services, return a 404 Not Found
        raise HTTPException(status_code=404, detail="Service not found in Gateway")

    # Step 2: Forward the request internally (The Proxy part)
    try:
        # We use standard synchronous requests library (beginner friendly)
        # We also pass along any query parameters (like ?search=hello)
        response = requests.request(
            method=request.method,
            url=target_url,
            params=request.query_params
        )
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=502, detail="Bad Gateway. The target service is down.")

    # Step 3: Return the response back to the client
    # We return the exact JSON that the backend service gave us.
    return response.json()
