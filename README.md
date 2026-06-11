# Cloud-Native Microservices Architecture 🚀

A robust, beginner-friendly cloud infrastructure project demonstrating modern backend architecture, containerization, and Continuous Integration/Continuous Deployment (CI/CD). This project simulates a real-world enterprise backend using decoupled services communicating via HTTP protocols over a custom API Gateway.

## 🌟 Architecture Overview

The system consists of three independent microservices deployed on the Cloud:
1. **API Gateway (Reverse Proxy):** Acts as the single entry point for all external traffic. It intercepts incoming HTTP requests, applies rate limiting and logging middleware, and securely routes traffic to the appropriate internal backend service.
2. **Service A (User Data Service):** An independent REST API responsible for handling data. It acts as the source of truth for user information.
3. **Service B (Greeting Service):** A dependent REST API that demonstrates inter-service communication. It receives a request, internally queries Service A for user data, formats a response, and returns it to the client.

## 🛠️ Technology Stack
* **Language:** Python 3.10
* **Framework:** FastAPI (High-performance async REST framework)
* **Containerization:** Docker (Multi-stage builds)
* **Orchestration:** Docker Compose (Local) / Kubernetes-ready
* **Cloud Deployment:** Render.com (PaaS)
* **CI/CD:** GitHub Webhooks

## ☁️ Cloud Deployment & CI/CD
This project is engineered to be fully environment-agnostic. Instead of hardcoding internal IP addresses, the services use injected **Environment Variables** (`os.getenv`) for service discovery.

The CI/CD pipeline is fully automated:
1. Code is pushed to the `main` branch on GitHub.
2. Render.com detects the commit via Webhooks.
3. Render independently builds three separate Docker images for the Gateway, Service A, and Service B.
4. The containers are deployed with zero-downtime rollouts. 

## 🔌 API Endpoints
All traffic must flow through the API Gateway.

**Get User Data (Routes to Service A):**
`GET /service-a/users/{user_id}`

**Get Custom Greeting (Routes to Service B -> queries Service A):**
`GET /service-b/greet/{user_id}`

**Health Checks:**
`GET /service-b/health`

## 🚀 Running Locally (Docker Compose)
To spin up the entire architecture on your local machine:
```bash
# Clone the repository
git clone https://github.com/Anvitha-Dusi/MICROSERVICES_NETWORKING.git

# Navigate to the project directory
cd MICROSERVICES_NETWORKING

# Build and run the containers in detached mode
docker-compose up -d --build
```
The Gateway will be accessible locally at `http://localhost:8080`.

---
*This project was built to demonstrate proficiency in Microservice Architecture, Cloud Networking, and Docker Containerization for Backend Engineering roles.*
