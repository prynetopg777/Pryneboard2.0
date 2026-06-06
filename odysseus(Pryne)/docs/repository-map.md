# Repository Map (docs/repository-map.md)

## Directory Structure Overview
- `core/`: Fundamental infrastructure (auth, db, exceptions, middleware).
- `src/`: Core business logic, agent tools, RAG, interaction processors.
- `routes/`: FastAPI request handlers, API endpoints.
- `services/`: Domain-specific backend services (Memory, Search, Research, HW management).
- `static/`: Frontend SPA assets.
- `data/`: User data, databases, uploads (gitignored).

## Key Files
- `app.py`: Main entry point and orchestrator.
- `pyproject.toml`: Project dependencies and configuration.
- `docker-compose.yml`: Main container orchestration.

## Dependency Relationships
`app.py` → `routes/` (imports and mounts) → `services/` (domain logic) → `src/` (core AI logic) → `core/` (shared infrastructure).
