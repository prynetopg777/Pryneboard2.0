# Project Rules - Hopper

## Architectural Rules
1. **Source Grounding:** The system MUST prioritize the provided context over LLM internal weights. Hallucinations are strictly forbidden via system prompts and low temperatures.
2. **Namespace Isolation:** Data MUST be stored and queried within specific namespaces. The `__default__` namespace should only be used for general documentation.
3. **Stateless Backend:** The backend should remain stateless. User session data (history) is managed by the client and passed with each request.
4. **Service Abstraction:** All third-party AI services (Pinecone, Groq) must be wrapped in service modules in `backend/src/services` to allow for future provider switching.

## Coding Standards
1. **HTML Output:** All LLM responses must be semantic HTML with Tailwind CSS utility classes. Avoid Markdown in the final response.
2. **Type Safety:** Use TypeScript interfaces for all API payloads and internal data structures (e.g., `ChatHistoryEntry`, `Document`).
3. **Environment Variables:** Never hardcode API keys or index names. Use `dotenv` and validate presence at startup.
4. **Error Handling:** API endpoints must return descriptive error messages and appropriate HTTP status codes (400 for client errors, 500 for service failures).

## Patterns to Preserve
1. **Follow-up Detection:** The logic in `index.ts` that skips Pinecone retrieval for follow-up questions must be preserved to save on latency and costs.
2. **Dual-Stage Deduplication:** The combination of content hashing and semantic similarity checking ensures a clean vector store and should be maintained.
3. **Namespace-Based Config:** Using namespace names as keys for configuration (TopK, Reranker, Prompts) is a core pattern for multi-tenancy.

## Anti-Patterns to Avoid
1. **Direct Pinecone Access:** Never call Pinecone methods directly from `index.ts` or `server.ts`. Use the `embedding.ts` or `retriever.ts` services.
2. **Global CSS:** Avoid adding global CSS files in the frontend. Prefer Tailwind utility classes for all styling.
3. **Large Embeddings Batches:** Do not exceed a batch size of 96 for Pinecone Inference embeddings (current limit is 50 in `embedding.ts`).
4. **Markdown in Prompts:** Do not instruct the LLM to use Markdown; this will break the frontend's `html-react-parser` integration.

## Mandatory Implementation Details
- **Sources Section:** Every LLM response MUST end with a "Sources:" list.
- **Source Hyperlinks:** URL sources MUST be formatted as `<a href="..." target="_blank">` tags.
- **PDF Citations:** PDF sources MUST include title and page number as plain text.
