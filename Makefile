.PHONY: help backend-venv backend-install backend-test backend-run frontend-install frontend-test frontend-run docker-build docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  backend-venv     - Create a virtual environment for the backend"
	@echo "  backend-install  - Install backend dependencies"
	@echo "  backend-test     - Run backend tests"
	@echo "  backend-run      - Run the backend server"
	@echo "  frontend-install - Install frontend dependencies"
	@echo "  frontend-test    - Run frontend tests"
	@echo "  frontend-run     - Run the frontend server"
	@echo "  docker-build     - Build Docker images"
	@echo "  docker-up        - Start all services with Docker Compose"
	@echo "  docker-down      - Stop all services with Docker Compose"

# Backend commands
backend-venv:
	@echo "Creating virtual environment for backend..."
	cd backend && python -m venv venv
	@echo "Virtual environment created. Activate with 'source backend/venv/bin/activate' (Linux/Mac) or 'backend\venv\Scripts\activate' (Windows)"

backend-install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt

backend-test:
	@echo "Running backend tests..."
	cd backend && python -m pytest tests/

backend-run:
	@echo "Starting backend server..."
	cd backend && uvicorn main:app --reload

# Frontend commands
frontend-install:
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

frontend-test:
	@echo "Running frontend tests..."
	cd frontend && npm test

frontend-run:
	@echo "Starting frontend server..."
	cd frontend && npm run dev

# Docker commands
docker-build:
	@echo "Building Docker images..."
	docker-compose build

docker-up:
	@echo "Starting services with Docker Compose..."
	docker-compose up -d

docker-down:
	@echo "Stopping services with Docker Compose..."
	docker-compose down
