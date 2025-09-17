# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Start the application
```bash
# Start PostgreSQL database
docker compose up -d

# Run FastAPI with auto-reload
uvicorn main:app --reload

# Or use the convenience script
./run.sh
```

### Stop services
```bash
# Stop PostgreSQL
docker compose down
```

## Architecture

This FastAPI application follows a **service-based architecture** with clear separation of concerns:

### Layer Responsibilities

1. **API Layer** (`main.py`): FastAPI endpoints handle HTTP requests/responses and dependency injection
2. **Service Layer** (`app/services/`): Business logic, orchestration, and domain-specific validation
3. **Repository Layer** (`app/repositories/`): Data access abstraction, all database queries
4. **Model Layer** (`app/models/`): SQLAlchemy ORM models defining database schema
5. **Schema Layer** (`app/schemas/`): Pydantic models for request/response validation and serialization

### Data Flow Pattern
Request → API Endpoint → Service (business logic) → Repository (data access) → Database
Response ← API Endpoint ← Service (validation) ← Repository ← Database

### Key Design Decisions

- **Dependency Injection**: Database sessions are injected via FastAPI's `Depends()` in main.py
- **Service Pattern**: Each service class receives a database session in its constructor and creates its own repository instance
- **Error Handling**: Services raise `ValueError` for business logic errors, which are converted to appropriate HTTP exceptions in the API layer
- **Validation**: Pydantic schemas handle input validation, services handle business rule validation

## Database Configuration

PostgreSQL connection (defined in `app/database.py`):
- Connection string: `postgresql://user:password@localhost/userdb`
- Tables are auto-created on startup via `User.metadata.create_all(bind=engine)`