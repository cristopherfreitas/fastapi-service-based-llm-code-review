# FastAPI Service-Based User Management API

A simple FastAPI application demonstrating service-based architecture for user management with PostgreSQL database.

## Features

- **Service-Based Architecture**: Clean separation of concerns with repositories, services, and API layers
- **User Management**: Create and retrieve users with validation
- **PostgreSQL Integration**: Uses SQLAlchemy ORM with PostgreSQL database
- **Docker Support**: PostgreSQL runs in a Docker container for easy setup
- **Automated Code Review**: Integrated Claude Code review on pull requests for code quality assurance

## Project Structure

```
app/
├── __init__.py
├── database.py          # Database configuration and session management
├── models/
│   ├── __init__.py
│   └── user.py          # SQLAlchemy User model
├── repositories/
│   ├── __init__.py
│   └── user_repository.py  # Data access layer
├── schemas/
│   ├── __init__.py
│   └── user.py          # Pydantic models for validation
└── services/
    ├── __init__.py
    └── user_service.py  # Business logic layer
main.py                  # FastAPI application and endpoints
docker-compose.yml       # PostgreSQL container setup
requirements.txt         # Python dependencies
run.sh                   # Quick start script
```

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi-service-based-llm-code-review
   ```

2. **Start PostgreSQL with Docker**
   ```bash
   docker compose up -d
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI application**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### GET /
Welcome message

### POST /users/
Create a new user
```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john.doe@example.com"}'
```

### GET /users/{user_id}
Get user by ID
```bash
curl -X GET http://localhost:8000/users/1
```

## Architecture Overview

This application follows a service-based architecture pattern:

1. **API Layer** (`main.py`): FastAPI endpoints that handle HTTP requests/responses
2. **Service Layer** (`services/`): Business logic and validation
3. **Repository Layer** (`repositories/`): Data access and database operations
4. **Model Layer** (`models/`): SQLAlchemy database models
5. **Schema Layer** (`schemas/`): Pydantic models for request/response validation

## Database Configuration

The application connects to PostgreSQL with these default settings:
- Host: localhost
- Port: 5432
- Database: userdb
- Username: user
- Password: password

## Development

To stop the services:
```bash
# Stop FastAPI (Ctrl+C in the terminal)
# Stop PostgreSQL
docker compose down
```

For development with auto-reload:
```bash
uvicorn main:app --reload
```