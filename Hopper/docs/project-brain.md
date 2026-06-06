# Project Brain - Hopper

## Executive Summary
Hopper is a specialized RAG (Retrieval-Augmented Generation) engine tailored for two primary use cases: processing structured/unstructured documents and analyzing Discord-based team activity logs. It leverages modern AI infrastructure (Pinecone Inference, Groq) to provide low-latency, context-aware responses with strict factual grounding.

## Core Features
- **Multi-Source Ingestion:** Supports PDF, JSON, Web URLs, and plain text.
- **Discord Intelligence:** Custom Discord bot specifically designed to scrape, date-tag, and chunk chat history into reportable segments (Daily/Weekly).
- **Semantic Deduplication:** Uses SHA-256 hashing and semantic similarity (95% threshold) to prevent duplicate content in the vector store.
- **Advanced Retrieval:**
  - **Dynamic Top-K:** Configurable retrieval depth per namespace.
  - **Reranking:** Integration with `bge-reranker-v2-m3` for high-precision context matching.
  - **Follow-up Optimization:** Skips expensive retrieval if the question can be answered from the immediate chat history.
- **HTML-First UI:** Responses are rendered in semantic HTML with Tailwind CSS, optimized for modern web frontends.

## System Architecture
Hopper is divided into three layers:
1.  **Collection Layer:** `hopper_harvest.py` (Discord) and `documentProcessor.ts` (Local/URL).
2.  **Intelligence Layer:** `embedding.ts` (Pinecone Embeddings), `retriever.ts` (Pinecone Search + Rerank), `llm.ts` (Groq).
3.  **Interface Layer:** React Frontend and Express API.

## Data Flow
1.  **Ingestion:** Source -> Text Extraction -> SHA-256 Hashing -> Chunking -> Pinecone Upsert (Batched).
2.  **Query:** User Question -> Namespace Detection -> Search (Pinecone) -> [Rerank] -> Context Assembly -> LLM Prompt Injection -> HTML Response.

## Major Modules
- **`documentProcessor.ts`**: The "Digestive System". Handles all file format nuances, especially the unique `---` separated Discord log format.
- **`retriever.ts`**: The "Librarian". Implements dual-stage retrieval (Vector Search -> Reranking).
- **`prompts.ts`**: The "Persona Engine". Maps namespaces to specific system instructions (e.g., `product` for grocery, `discord` for chat logs).

## Key Design Decisions
- **Pinecone Inference API:** Chosen over local embedding models to minimize backend resource requirements and simplify deployment.
- **HTML over Markdown:** Decided to use HTML + Tailwind to ensure consistent rendering across the specific React frontend components without needing a complex markdown parser.
- **Namespace-Based Tenancy:** Utilizes Pinecone namespaces to separate logically different datasets (e.g., SNR grocery vs. internal team logs) within a single index.

## Known Technical Debt
- **Hardcoded Top-K/Reranker Config:** Configuration for Top-K and Reranker usage is currently hardcoded in `getTopK.ts` and `useReranker.ts` as a switch-case instead of a dynamic database/config file.
- **Synchronous Ingestion CLI:** The ingestion process via CLI is blocking and doesn't provide progress events via WebSocket for the frontend.
- **Discord Bot Coupling:** The Python bot relies on a specific `---` delimiter which must be matched by the TypeScript `documentProcessor`.

## Current Limitations
- **File Size:** PDF parsing might struggle with extremely large or image-heavy PDFs (using `pdf-parse`).
- **Context Window:** While using `gpt-oss-120b`, history is currently truncated to the last 4 messages in the frontend.
- **Reranker Latency:** Enabling the reranker adds a second network hop to Pinecone, increasing response time by ~500ms-1s.

## Future Roadmap
- **Streaming Responses:** Implement Server-Sent Events (SSE) for real-time LLM output.
- **Visual Citations:** Show PDF thumbnails or Discord message links in the "Sources" section.
- **Admin Dashboard:** A UI to manage namespaces, view ingestion logs, and adjust retrieval parameters dynamically.
