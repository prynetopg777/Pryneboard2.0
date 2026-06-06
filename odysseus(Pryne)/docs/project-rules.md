# Project Rules (docs/project-rules.md)

## Architectural Rules
- **Modular Services:** All domain logic MUST live in `services/`.
- **Slim Entry Point:** Keep `app.py` free of business logic; it is for orchestration and configuration only.
- **Asynchronicity:** All IO-bound operations (DB access, AI calls, file operations) MUST be `async`.

## Coding Standards
- Type hinting is mandatory for all functions and class attributes.
- Centralized custom exceptions (in `core/exceptions.py`) must be used for error handling.
- Gitignore all generated and user-specific data (everything in `data/`).

## Anti-Patterns
- DO NOT add business logic to FastAPI route handlers.
- DO NOT perform synchronous blocking IO within request handlers.
- DO NOT expose internal ports/services to the public network without a reverse proxy.
