Real-Time Sentiment Analysis MLOps Pipeline

Project Overview

This project demonstrates a complete end-to-end MLOps pipeline for deploying a pre-trained sentiment analysis model as a containerized web service. The entire stack is fully observable and production-ready, featuring real-time monitoring and a CI/CD pipeline for cloud deployment.

Key Technologies

Machine Learning: HuggingFace DistilBERT (Sentiment Analysis)

API Framework: FastAPI

Containerization: Docker

Orchestration: Docker Compose (for local development)

Observability Stack: Prometheus (Time-series metrics) and Grafana (Real-time dashboards)

CI/CD & Cloud: GitHub Actions for automated build and push to Azure Container Registry (ACR) and deployment to Azure App Service.

Architecture (Local Stack)

The local stack consists of three interconnected services running inside a single Docker network:

api: The FastAPI application that hosts the ML model and exposes /predict and /metrics endpoints.

prometheus: Scrapes the /metrics endpoint of the API every 5 seconds to collect operational and model drift data.

grafana: Visualizes the data scraped by Prometheus into dashboards, showing request latency and sentiment distribution.

Running the Project Locally

To run the full stack (API, Prometheus, and Grafana) locally, ensure Docker is running and execute the following command in the root directory:

docker compose up --build


Endpoints

API Docs (Swagger UI): http://localhost:8000/docs

Grafana Dashboards: http://localhost:3000 (User: admin, Pass: admin)

Prometheus UI: http://localhost:9090

Note: This project is intended as a demonstration of MLOps deployment practices and does not include model training.