# AGENTS.md - AI Agent Knowledge Base

## Project Overview
**Hopper** is a Retrieval-Augmented Generation (RAG) system designed as a knowledgeable AI concierge. it enables users to chat with documents (PDF, JSON, TXT, URLs) and Discord chat logs. The system is multi-tenant via Pinecone namespaces, allowing for domain-specific knowledge bases (e.g., Grocery/Product, Discord reports, General docs).

## Technology Stack
- **Backend:** Node.js (Express), TypeScript, LangChain.
- **Frontend:** React (Vite), Tailwind CSS, Zustand.
- **Vector Database:** Pinecone (Inference API for Embeddings & Reranking).
- **LLM:** Groq (`openai/gpt-oss-120b`).
- **Data Collection:** Python (Discord Bot for scraping and chunking).
- **Core Libraries:** `cheerio` (web scraping), `pdf-parse` (PDF extraction), `tsx` (runtime).

## Architecture Summary
The system follows a classic RAG architecture:
1. **Ingestion Pipeline:** Documents/URLs are fetched, parsed, chunked, hashed (for deduplication), embedded, and stored in Pinecone namespaces.
2. **Retrieval Pipeline:** User queries are embedded, matched against Pinecone (Top-K), optionally reranked (Top-N), and formatted into a context block.
3. **Generation:** LLM processes the context, chat history, and question using namespace-specific system prompts.

## Coding Conventions
- **TypeScript:** Strict typing preferred.
- **Service Pattern:** External integrations (Pinecone, Groq) are encapsulated in `backend/src/services`.
- **Core Logic:** Processing and retrieval logic reside in `backend/src/core`.
- **Prompts:** Centralized in `backend/src/core/prompts.ts`.
- **HTML Output:** AI responses MUST be HTML (not Markdown) with Tailwind CSS classes for structure.

## Important Constraints
- **Strict Contextual Integrity:** Agents must NEVER use outside knowledge. If the answer isn't in the context, they must say so.
- **Mandatory Sources:** Every response must end with a "Sources:" section.
- **Deduplication:** Content hashing (SHA-256) is used to prevent redundant ingestion.
- **Batching:** Pinecone upserts are batched (size 50) due to Inference API limits.

## Common Development Workflows
- **Local Ingestion:** `npx tsx src/index.ts ingest <path> <namespace>`
- **Local Query:** `npx tsx src/index.ts ask "<question>" <namespace>`
- **Frontend Dev:** `cd frontend && npm run dev`
- **Backend Dev:** `cd backend && npm run dev`

## Critical Files
- `backend/src/index.ts`: Orchestration entry point.
- `backend/src/core/documentProcessor.ts`: Parsing and hashing logic.
- `backend/src/core/prompts.ts`: System personalities and rules.
- `backend/src/services/embedding.ts`: Pinecone Inference bridge.
- `backend/discord_bot_starter/hopper_harvest.py`: Discord ingestion source.
