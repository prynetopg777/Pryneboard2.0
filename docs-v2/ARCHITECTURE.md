# ARCHITECTURE: Pryneboard 2.0 (Product-Aligned)

## System Overview
Pryneboard 2.0 is a production-ready, enterprise-grade intelligence workspace functioning as a "Cognitive Operating System." It consolidates disconnected information silos, automates data ingestion, and provides an agentic interface for knowledge retrieval and task execution.

## Core Architecture
The architecture is structured around five production subsystems:

1.  **Odysseus Core (FastAPI Backend):** The unified API orchestrator. Handles routing, authentication, and service coordination.
2.  **Ingestion Pipeline:** Automated subsystem monitoring `data/` directories via `Watchdog`. Extracts, chunks, and deduplicates data (SHA-256) before indexing in ChromaDB.
3.  **Knowledgebase (RAG Layer):** Multi-tenant vector store (ChromaDB) providing semantic retrieval and reranking.
4.  **Agentic Runtime:** An LLM-based loop supporting Thought/Action/Observation cycles. Routes tasks to Tools (MCP/Bash/Vision).
5.  **Cookbook Infrastructure:** A minimal service layer for local model lifecycle management (serving, downloading) and GPU abstraction.

---

## 2. Web UI Integration
The Web UI (React) interacts with Odysseus Core via:
*   **Chat:** SSE (Server-Sent Events) for streaming responses.
*   **Ingestion:** Status polling (`GET /api/ingest/status`).
*   **Knowledge/SOPs:** RESTful API (`GET /api/rag/sources`).
*   **Task Monitor:** SSE or WebSockets for real-time tracking.

---

## 3. Workflow Integration
Pryneboard 2.0 automates the "Context Switching" tax. By integrating automated ingestion and agent-led reasoning, it functions as an "invisible teammate," allowing users to query, analyze, and update documentation in real-time.
