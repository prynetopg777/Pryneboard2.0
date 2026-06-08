# CODE_REVIEW_AND_TEST_GUIDE.md

This document defines the mandatory Quality Gates for all feature implementations in Pryneboard 2.0. Every pull request or feature branch must satisfy these requirements before being considered for merge.

---

## 1. Code Review Checklist
*Before initiating a review, ensure the implementation adheres to these standards:*

### Architectural Integrity
- [ ] **Subsystem Isolation:** Are changes contained within the appropriate subsystem (`src/app/`, `src/rag/`, `src/agents/`, `src/ingestion/`, `src/cookbook/`)?
- [ ] **Async Compliance:** Are all IO-bound operations (DB, AI calls, File IO) `async`?
- [ ] **Consistency:** Does the code follow the 5-subsystem structure?

### Security & Privacy
- [ ] **Workspace Isolation:** Is every data lookup scoped by `namespace`?
- [ ] **Secrets:** No hardcoded API keys or secrets.

### Maintainability
- [ ] **Logging:** Does the code provide actionable logs?
- [ ] **Documentation:** Have you updated `ARCHITECTURE.md` if interfaces have changed?

---

## 2. Testing Strategy
*All features require a multi-layered testing approach.*

### Unit Tests
- Verify low-level logic (e.g., `src/ingestion/document_processor.py`) in isolation.

### Integration Tests
- Verify the *pipeline* behavior (e.g., `src/ingestion/` -> `src/rag/`).
- Must include **Workspace Isolation** tests.

### Regression Tests
- **RAG Pipeline:** Run baseline query.
- **Odysseus Core:** Run integration tests for `src/app/` endpoints.

---

## 3. Production Readiness (QA Gate)
- [ ] **Concurrency:** Does this feature fail under heavy load?
- [ ] **Resource Contention:** Does this feature exhaust VRAM?
- [ ] **Error Recovery:** Does the system gracefully recover from service timeouts?
