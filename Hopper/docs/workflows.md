# Workflows - Hopper

## Document Ingestion Flow
1. **Source Identification:** User provides a file path or URL to `index.ts` (CLI) or through an internal process.
2. **Text Extraction:** `documentProcessor.ts` determines the type (PDF, JSON, URL, TXT).
3. **Deduplication Check:**
   - SHA-256 hash of full content is checked against Pinecone metadata.
   - If no hash match, a semantic search of the first chunk is performed.
4. **Chunking:** Text is split into chunks of ~1000 characters with 200 overlap (standard) or by Discord message blocks.
5. **Embedding:** Chunks are sent to Pinecone Inference (`multilingual-e5-large`).
6. **Upsert:** Embeddings and metadata are pushed to Pinecone in batches of 50.

## Discord Harvesting Flow
1. **Trigger:** User runs `/scrape` command in Discord.
2. **Fetch:** Bot fetches channel history (default 500 messages).
3. **Chunking:** `split_message` in Python logic identifies dates and clients.
4. **Temporary Storage:** Chunks are written to a local `.txt` file with `---` separators.
5. **Ingestion Trigger:** Bot calls `npx tsx src/index.ts ingest` on the temporary file.
6. **Cleanup:** Bot deletes the temporary file after successful ingestion.

## Request Lifecycle (Ask Question)
1. **Client Request:** Frontend sends `{ question, history, namespace }` to `/api/ask`.
2. **Namespace Selection:** Backend uses `namespace` to determine `TopK`, `Reranker` status, and `System Prompt`.
3. **Follow-up Check:** If the question is a follow-up (e.g., "Summarize that"), retrieval is skipped and the last assistant message is used as context.
4. **Retrieval Phase:**
   - **Vector Search:** Fetch Top-K candidates from Pinecone.
   - **Rerank (Optional):** If enabled, send candidates to Pinecone Reranker.
5. **Context Assembly:** Matches are formatted into a structured string with metadata labels (DATA TYPE, SOURCE, CONFIDENCE).
6. **LLM Generation:** `llm.ts` formats the prompt using the selected template and calls Groq.
7. **Response:** HTML-formatted answer is returned to the frontend.

## State Management Flow
1. **Initialization:** Frontend loads, fetches available namespaces from `/api/namespaces`.
2. **Persistence:** `contextStore.ts` (Zustand + Persist) retrieves the last used namespace from `localStorage`.
3. **Update:** User changes the dropdown, `selectedNamespace` is updated in the store and persisted.
4. **Synchronization:** All subsequent API calls use the current store value.
