# ⚓ Pryneboard 2.0: Master Project Manifest

## 1. Executive Summary
Pryneboard 2.0 is a local-first, privacy-sovereign AI workspace. It merges the **high-precision RAG pipeline of Hopper** with the **robust agent orchestration of Odysseus**. The goal is to move beyond a "chatbot" into a structured **Organizational Intelligence Layer** that runs entirely on user hardware.

---

## 2. The Vision: "Privacy is a Feature"
*   **Sovereignty by Default:** Data never leaves the local machine.
*   **Precision over Speed:** Retrieval-Augmented Generation (RAG) uses two-stage scoring (Vector + Cross-Encoder) to eliminate hallucinations.
*   **The Company Brain:** Raw conversations and documents are distilled into a structured graph of Decisions, SOPs, and Expertise.

---

## 3. Staff Architecture Review: The "Brutal Truth"
*   **The Missing:** We need a unified schema migration path and hardware-aware load balancing for VRAM.
*   **The Fat:** Rigid "Namespaces" are overengineered for solo users; we will move to metadata-based tagging.
*   **The Bottleneck:** The Python GIL and ChromaDB I/O on Windows are the primary risks to velocity.
*   **The Pivot:** We will **postpone the React rewrite** to focus 100% on the Intelligence Layer (Backend/RAG) for the 60-day MVP.

---

## 4. Subsystem Design: The Company Brain
The "Company Brain" transforms raw episodic memory into declarative organizational truth.

### Domain Map
*   **Entities:** Employees, Teams, Projects, Decisions, SOPs, Policies, Meetings.
*   **Storage:** 
    *   **SQLite:** Structural relationships (e.g., `Decision --approved_by--> Employee`).
    *   **ChromaDB:** Semantic text chunks for RAG.
*   **Retrieval:** **Traverse-then-Search.** The system filters the graph for relevant nodes first, then performs vector search within that specific context.

---

## 5. The 60-Day MVP Roadmap

| Category | Features | Decision Logic |
| :--- | :--- | :--- |
| **Must Have** | FastAPI Merge, Discord Harvester, Two-Stage RAG, Source Citations. | Core utility. Without these, it's not "2.0". |
| **Should Have** | Basic Relationship Extraction, MCP Tools, Local Reranker Serving. | Moves the needle from Search to Reasoning. |
| **Nice To Have** | Deep Research UI, Visual Citations. | High value, but can be done post-MVP. |
| **Future** | React Frontend Rewrite, Mobile PWA, Local Vision/STT. | Too high-effort for a 60-day solo sprint. |

---

## 6. Implementation Guide (Incremental)

### Phase 1: The Precision Engine (Weeks 1-3)
*   **Feature:** Content-Hashed Ingestion & Two-Stage Retrieval.
*   **Focus:** Update `src/rag_vector.py` and `src/document_processor.py` to support SHA-256 deduplication and Cross-Encoder reranking.
*   **Status:** **COMPLETE** (SHA-256 Hashing, Dedupe, and BGE Reranker implemented).

### Phase 2: Integrated Data Sources (Weeks 4-6)
*   **Feature:** Managed Discord Harvester & Metadata Scoping.
*   **Focus:** Integrate `hopper_harvest.py` into `src/integrations/`. Implement `POST /api/ingest/discord`.
*   **Status:** **COMPLETE** (Logic migrated to Python, API triggered, RAG integrated).
### Phase 3: Generation & Output (Weeks 7-8)
*   **Feature:** Grounded Generation (HTML-First) & Citations.
*   **Focus:** Implement strict grounding in `ai_interaction.py` and render the "Sources:" section in `app.js`.
*   **Status:** **IN PROGRESS** (Strict grounding, HTML-first output, and Source mandates implemented in `ai_interaction.py`).
*   **Added Value:** Specialized CSV-to-Markdown processing, PDF metadata extraction, and comprehensive YouTube Analysis tool (transcript + comments).
*   **Acceptance:** AI refuses to answer out-of-scope questions; every answer includes clickable local citations.


---

## 7. Technical Mandates
1.  **Async-First:** All model/DB calls must be `async`.
2.  **MCP Everywhere:** No custom tools; use MCP servers for all external integrations.
3.  **Surgical Edits:** Reuse the Odysseus UI and shell logic to minimize regression risk.

---

## 8. Quality Assurance & Definition of Done

Every feature implemented in Pryneboard 2.0 must pass the following Quality Gates before it can be considered complete.

### Gate 1: Implementation Review

Purpose:
Verify the feature was implemented according to the approved specification.

Checks:

* Acceptance criteria satisfied
* No scope creep
* No architectural violations
* Existing functionality preserved

Output:

* PASS
* FAIL

---

### Gate 2: Staff Engineer Code Review

Purpose:
Identify defects before merge.

Review Areas:

* Logic correctness
* Error handling
* Async compliance
* Logging quality
* Security concerns
* Performance concerns
* Maintainability

Severity Levels:

* Critical
* High
* Medium
* Low

Critical findings block merge.

---

### Gate 3: QA Validation

Purpose:
Verify behavior from a user perspective.

Required Tests:

* Happy path
* Edge cases
* Invalid inputs
* Failure recovery
* Data persistence

Output:

* Pass rate
* Defects found
* Recommended fixes

---

### Gate 4: Regression Testing

Purpose:
Ensure no existing functionality breaks.

Required Areas:

* Document ingestion
* Retrieval
* Chat generation
* Metadata filtering
* ChromaDB operations
* SQLite operations

All regression tests must pass.

---

### Gate 5: Acceptance Validation

Validate against the feature specification.

Requirements:

* Every acceptance criterion mapped to a test
* Every test passes
* Evidence documented

Output:

Feature Status:

* Complete
* Requires Fixes
* Rejected

---

### Definition of Done

A feature is complete only when:

✓ Code implemented

✓ Unit tests written

✓ Integration tests pass

✓ QA review completed

✓ Regression tests pass

✓ Acceptance criteria verified

✓ No critical findings remain

✓ Documentation updated

Only then may work proceed to the next feature.

*Created on Friday, June 5, 2026*
