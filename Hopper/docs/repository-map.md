# Repository Map - Hopper

## Directory Tree
```text
hopper/
├── backend/                # Express server & RAG logic
│   ├── discord_bot_starter/ # Python Discord scraper
│   ├── src/
│   │   ├── core/           # Business logic (retrieval, processing, prompts)
│   │   ├── services/       # External integrations (Pinecone, Groq)
│   │   ├── utils/          # Config helpers & logic utilities
│   │   ├── index.ts        # CLI & Orchestration
│   │   └── server.ts       # Express API entry
│   └── rawData/            # Sample documents for ingestion
├── frontend/               # Vite + React + Tailwind frontend
│   ├── public/
│   └── src/
│       ├── assets/
│       ├── store/          # Zustand state (contextStore)
│       ├── App.tsx         # Main Chat UI
│       └── main.tsx        # React entry
└── data/                   # Scraped Discord logs & processed text
```

## Major Folders & Purpose

### `backend/src/core/`
The heart of the application.
- **`documentProcessor.ts`**: Universal parser for all supported formats. Handles the transformation of raw data into LangChain `Document` objects.
- **`retriever.ts`**: Orchestrates vector search and reranking. Logic for choosing between standard search and reranked search lives here.
- **`prompts.ts`**: Contains the complex system prompts for different personas (Concierge, Product Expert, Discord Analyst).

### `backend/src/services/`
External service abstractions.
- **`embedding.ts`**: Interface for Pinecone's Inference API for both vector generation and upserting.
- **`llm.ts`**: Interface for Groq (LangChain wrapper) and prompt formatting logic.

### `backend/discord_bot_starter/`
- **`hopper_harvest.py`**: A standalone Python bot. It's the "harvester" that feeds the system with Discord chat data. It includes sophisticated logic to detect dates and client names within chat messages.

### `frontend/src/store/`
- **`contextStore.ts`**: Manages the `selectedNamespace`. Persisted to localStorage so users stay in their chosen context across sessions.

## Important Files

- `backend/src/index.ts`: The central orchestration file. It contains the logic for `ingestDocument` and `askQuestion`, which are used by both the CLI and the Express server.
- `backend/src/server.ts`: Exposes the RAG functionality via a REST API. It handles the `/api/ask` and `/api/namespaces` endpoints.
- `frontend/src/App.tsx`: The primary user interface. Implements the chat loop, message history management, and HTML-to-React parsing for AI responses.

## Dependency Relationships
1. **Frontend -> Backend (API):** Frontend communicates with `server.ts` via HTTP POST/GET.
2. **Backend CLI -> Vector DB:** `index.ts` uses `embedding.ts` to push data to Pinecone.
3. **Discord Bot -> Backend CLI:** `hopper_harvest.py` executes `npx tsx src/index.ts ingest` as a subprocess.
4. **Backend -> Pinecone/Groq:** Services use environment variables to communicate with cloud providers.
