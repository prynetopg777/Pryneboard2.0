# ARCHITECTURE: Pryneboard 2.0

## System Overview
Pryneboard 2.0 follows a **Modular Service-Oriented Architecture**. It consolidates the broad utility of Odysseus (Pryneboard 1.0) with the high-precision RAG engine of Hopper.

---

## 1. The Intelligence Layer (Python/FastAPI)
The central orchestrator that manages state, background tasks, and AI interaction loops.

### Agent Orchestrator
- **Agent Loop:** Manages multi-turn reasoning and tool execution.
- **MCP Manager:** Interfaces with Model Context Protocol servers for extensible toolsets (Browser, Filesystem, Google Maps, etc.).
- **Task Scheduler:** Handles long-running background jobs like Discord scraping or Deep Research.

### Unified RAG Pipeline
- **Ingestion Harvesters:** Modular scrapers (Discord Bot, Web Crawler, File Watcher).
- **Processing:** SHA-256 Hashing -> Semantic Deduplication -> Sentence-aware Chunking.
- **Two-Stage Retrieval:** 
    1. **Vector Search (ChromaDB):** Broad semantic matching.
    2. **Cross-Encoder Reranking:** High-precision scoring of candidates before LLM injection.

---

## 2. The Persistence Layer
- **SQLite:** Stores relational data (Conversations, Tasks, Settings, Metadata).
- **ChromaDB:** Local vector database for semantic memory and document storage.
- **Optional Cloud Bridge:** Integration for Pinecone (high-scale) or external LLM providers (Groq, Anthropic) for users with limited local hardware.

---

## 3. The Interface Layer (React/Tailwind)
A unified, component-based Single Page Application (SPA).
- **Context Store (Zustand):** Manages active namespaces and UI state.
- **HTML-First Rendering:** AI responses are streamed in semantic HTML with Tailwind utility classes for consistent, rich formatting.
- **Tool UI:** Dedicated views for the Editor, Cookbook, Gallery, and Research reports.

---

## 4. Data Flow
1. **Data Acquisition:** `Harvester` -> `Raw Storage`.
2. **Knowledge Integration:** `Processor` -> `Vector DB` (with content hashing).
3. **Query Execution:** `User Query` -> `Retrieval` (Vector + Rerank) -> `Prompt Assembly` -> `LLM` -> `HTML Stream`.
4. **Action Execution:** `User Intent` -> `Agent Loop` -> `Tool Selection` -> `MCP Execution` -> `Result Feedback`.
