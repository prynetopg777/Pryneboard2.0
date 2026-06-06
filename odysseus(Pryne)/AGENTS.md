# AGENTS.md

Pryneboard is a self-hosted AI workspace designed to provide a privacy-first, local-first alternative to commercial AI platforms like ChatGPT and Claude. It leverages local hardware for model serving while providing a robust UI and integration layer.

### Technology Stack
- **Backend:** Python 3.11+, FastAPI (Web framework), Starlette (ASGI)
- **Frontend:** Responsive SPA, Vanilla HTML/JS/CSS (modular ES modules)
- **Data Persistence:** SQLite (application data), ChromaDB (Vector memory)
- **Model Orchestration:** vLLM, llama.cpp, Ollama, API integrations (OpenAI, OpenRouter, etc.)
- **Containerization:** Docker/Docker Compose

### Architecture Summary
Pryneboard follows a modular component-based architecture.
- `app.py`: Slim orchestrator, handles startup/shutdown, middleware, and route registration.
- `core/`: Shared primitives (auth, database, constants, middleware).
- `src/`: Business logic, AI interaction loops, agent tools, model processing.
- `routes/`: FastAPI request handling, mapping HTTP/API requests to services.
- `services/`: Specialized service modules (Memory, Search, TTS, STT, Research, etc.).

### Coding Conventions
- **Asynchronous First:** Heavy use of `asyncio`, especially for AI turns and IO-bound operations.
- **Functional Composition:** Logic is often separated into managers/services invoked by routes.
- **Type Safety:** Type hints are used throughout the codebase.
- **Error Handling:** Centralized custom exceptions.

### Important Constraints
- **Local-first/Privacy-first:** Data lives in `data/` (gitignored). Do not log, persist, or expose sensitive user data.
- **Windows Compatibility:** Strict requirement for Windows native support alongside Docker.
- **Performance:** Asynchronous request handling is critical to prevent UI blocking.

### Development Workflows
- **New Features:** Implement in a dedicated `service/` or `src/` module, register in `app.py` if a new route is needed.
- **Testing:** Add tests to `tests/`. Use `pytest` with `asyncio` mode.
- **Local-First:** Prioritize local model/service integration before adding API dependencies.
