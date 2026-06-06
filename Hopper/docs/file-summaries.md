# File Summaries - Hopper

## Backend Core

### `backend/src/index.ts`
- **Purpose**: Main orchestrator for ingestion and querying.
- **Main Exports**: `ingestDocument`, `askQuestion`.
- **Dependencies**: `documentProcessor`, `embedding`, `retriever`, `llm`.
- **Consumers**: `server.ts`, CLI.
- **Critical Detail**: Implements "Follow-up detection" to skip Pinecone search if the user asks for a summary or clarification of the previous message.

### `backend/src/core/documentProcessor.ts`
- **Purpose**: Text extraction and chunking from various sources.
- **Main Exports**: `processFile`, `isDocumentDuplicate`.
- **Dependencies**: `pdf-parse`, `cheerio`, `crypto`.
- **Consumers**: `index.ts`.
- **Critical Detail**: Uses SHA-256 for hard deduplication and semantic search (Top-1 @ >0.95 score) for soft deduplication. Handles specific Discord log segmenting using `---` delimiters.

### `backend/src/core/retriever.ts`
- **Purpose**: Context retrieval from Pinecone.
- **Main Exports**: `querySimilar`, `querySimilarWithReranker`.
- **Dependencies**: `embedding.ts`, `getTopK.ts`.
- **Consumers**: `index.ts`.
- **Critical Detail**: `querySimilarWithReranker` fetches `10 * TopK` (min 50) candidates and narrows them down using Pinecone's `bge-reranker-v2-m3` model.

### `backend/src/core/prompts.ts`
- **Purpose**: Defines system instructions and rules for the LLM.
- **Main Exports**: `prompts` object.
- **Dependencies**: `@langchain/core/prompts`.
- **Consumers**: `llm.ts`.
- **Critical Detail**: Enforces mandatory source citation and HTML-only output with Tailwind CSS utility classes.

## Backend Services

### `backend/src/services/embedding.ts`
- **Purpose**: Pinecone Inference API wrapper.
- **Main Exports**: `getEmbedding`, `upsertChunks`, `pc`.
- **Dependencies**: `@pinecone-database/pinecone`.
- **Consumers**: `documentProcessor.ts`, `retriever.ts`, `index.ts`.
- **Critical Detail**: Hardcoded to use `multilingual-e5-large`. Handles batching of upserts (batch size: 50).

### `backend/src/services/llm.ts`
- **Purpose**: Groq LLM interface.
- **Main Exports**: `generateResponse`.
- **Dependencies**: `@langchain/groq`, `prompts.ts`.
- **Consumers**: `index.ts`.
- **Critical Detail**: Selects system prompt based on the namespace name (e.g., "discord", "snr").

## Utilities

### `backend/src/utils/getTopK.ts`
- **Purpose**: Retrieval parameter configuration.
- **Main Exports**: `getTopK`, `getTopN`.
- **Critical Detail**: Map of namespace to retrieval depth. Default K=5, Default N=20.

### `backend/src/utils/useReranker.ts`
- **Purpose**: Feature flag for reranking.
- **Main Exports**: `useReranker`.
- **Critical Detail**: Hardcoded boolean flag per namespace.

## Frontend

### `frontend/src/App.tsx`
- **Purpose**: Primary Chat interface.
- **Consumers**: End-users.
- **Critical Detail**: Uses `html-react-parser` to render the Tailwind-formatted HTML from the AI. Limits chat history sent to backend to the last 4 messages.

## Data Collection

### `backend/discord_bot_starter/hopper_harvest.py`
- **Purpose**: Discord channel scraper.
- **Dependencies**: `discord.py`.
- **Critical Detail**: Intelligently splits long Discord messages into chunks based on date patterns and client headers (`[Client Name]`). Directly triggers the backend ingestion CLI.
