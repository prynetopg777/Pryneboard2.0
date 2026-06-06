# File Summaries (docs/file-summaries.md)

This document provides high-level summaries for key files and modules.

## `app.py`
- **Purpose:** Entry point for FastAPI application, orchestrates component initialization and route registration.
- **Main Exports:** `app` (FastAPI instance).
- **Consumers:** ASGI server (uvicorn).

## `core/auth.py`
- **Purpose:** Handles user authentication and session management.
- **Main Exports:** `AuthManager`.

## `core/database.py`
- **Purpose:** SQL Alchemy database setup and model definitions.
- **Main Exports:** `SessionLocal`, Database models.

## `src/agent_loop.py`
- **Purpose:** Core agent execution loop for multi-step task completion.
- **Main Exports:** `AgentLoop` class.

## `src/rag_singleton.py`
- **Purpose:** Lazy initialization of vector RAG manager.
- **Main Exports:** `get_rag_manager()`.
