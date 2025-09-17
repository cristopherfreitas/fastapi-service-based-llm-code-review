#!/bin/bash

echo "Starting PostgreSQL with Docker Compose..."
docker compose up -d

echo "Waiting for PostgreSQL to be ready..."
sleep 5

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Starting FastAPI application..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload