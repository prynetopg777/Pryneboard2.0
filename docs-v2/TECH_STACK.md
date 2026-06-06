# TECH STACK: Pryneboard 2.0

## Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI (Asynchronous execution)
- **AI Orchestration:** LangChain / Custom Agent Loops
- **RAG Engine:** ChromaDB (Vector Store), `markitdown` / `pdf-parse` (Ingestion)
- **Local Model Serving:** Ollama, vLLM, llama.cpp
- **External Providers:** Groq, Anthropic, OpenAI (Optional)

## Frontend
- **Framework:** React 18 (Vite)
- **Styling:** Tailwind CSS (Modern, utility-first)
- **State Management:** Zustand (Lightweight, performant)
- **Interactions:** Server-Sent Events (SSE) for streaming responses

## Data & Persistence
- **Relational DB:** SQLite
- **Vector DB:** ChromaDB (Local), Pinecone (Optional/Remote)
- **Cache:** Redis or local file-based cache for model outputs

## Infrastructure
- **Containerization:** Docker & Docker Compose
- **MCP:** Model Context Protocol for tool extensions
- **Platform Support:** Windows (Native + WSL), Linux, macOS (M-series)
