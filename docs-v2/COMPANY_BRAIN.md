# COMPANY BRAIN: Pryneboard 2.0 Knowledge Base

## Strategic Context
Pryneboard 2.0 was initiated to solve the fragmentation between the high-precision data processing of the **Hopper** project and the broad assistant capabilities of **Odysseus (Pryneboard 1.0)**.

### Historical Pivots
1. **Backend Consolidation:** The project moved from a split Node.js/Python architecture to a unified Python (FastAPI) backend to simplify model orchestration and leverage Python's superior AI ecosystem.
2. **RAG Evolution:** Moved from simple hybrid search to a mandatory Reranking pipeline to reduce "hallucination by poor context."
3. **UI Modernization:** Transitioned from Vanilla JS to React to manage the increasing complexity of the "workspace" UI (multi-window, complex state).

---

## Core Values & Principles
- **Correctness over Speed:** It is better for the RAG engine to take 2 seconds longer if it results in a more accurate, cited response.
- **Surgical Changes:** When modifying the system, maintain existing conventions. Do not refactor unrelated code.
- **Documentation as Truth:** The code must reflect the architecture defined in `ARCHITECTURE.md`. Any divergence must be justified and the docs updated.
- **Privacy First:** Never introduce a feature that requires mandatory cloud connectivity without a local fallback.

---

## Decision Log (Foundational)
- **Vector DB:** ChromaDB selected for its ease of local deployment and strong Python integration.
- **Frontend:** React/Tailwind selected to allow for a rich, component-based UI that can handle streaming HTML responses effectively. (Postponed for MVP).
- **Agent Framework:** Built on a custom "Agent Loop" logic (from Odysseus) rather than high-level frameworks (AutoGPT/CrewAI) to maintain strict control over tool execution and context budget.
- **Reranker:** `BAAI/bge-reranker-base` selected as the default local reranking model for its high performance-to-VRAM ratio.
- **Deduplication:** Mandatory SHA-256 content hashing implemented at the database level to prevent vector index pollution.
