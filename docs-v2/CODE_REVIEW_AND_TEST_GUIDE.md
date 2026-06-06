# CODE_REVIEW_AND_TEST_GUIDE.md

This document defines the mandatory Quality Gates for all feature implementations in Pryneboard 2.0. Every pull request or feature branch must satisfy these requirements before being considered for merge.

---

## 1. Code Review Checklist
*Before initiating a review, ensure the implementation adheres to these standards:*

### Architectural Integrity
- [ ] **Surgical Edits:** Are changes strictly related to the feature? No unrelated refactoring or "drive-by" cleanup.
- [ ] **Async Compliance:** Are all IO-bound operations (DB, AI calls, File IO) `async`?
- [ ] **Consistency:** Does the code follow existing project patterns (e.g., `VectorRAG` delegation, `LLMCore` grounding)?
- [ ] **Memory Alignment:** Does the code align with `DOMAIN_MODEL.md`?

### Security & Privacy
- [ ] **Owner-Scope:** Is every data lookup filtered by `owner_id` or `namespace`?
- [ ] **Data Sanitization:** Are raw user inputs sanitized before being stored in the `Company Brain` graph?
- [ ] **Secrets:** Are no hardcoded API keys or secrets present?

### Maintainability
- [ ] **Logging:** Does the code provide actionable logs for both success and failure states?
- [ ] **Documentation:** Have you updated relevant documentation (e.g., `REPOSITORY_MAP_V2.md`, `README.md`) if interfaces have changed?

---

## 2. Testing Strategy
*All features require a multi-layered testing approach.*

### Unit Tests
- Verify low-level logic (e.g., `calculate_content_hash`) in isolation.
- Use `pytest` with `unittest.mock` for external dependencies.

### Integration Tests
- Verify the *pipeline* behavior (e.g., `Ingestion -> Hashing -> ChromaDB`).
- Must include **Owner Isolation** tests (User A cannot see/duplicate User B’s data).

### Regression Tests
- **RAG Pipeline:** Run a baseline query; verify the results are consistent with pre-change expectations.
- **Legacy Compatibility:** Verify 1.0 (Odysseus) data formats are still readable by 2.0.

---

## 3. Production Readiness (QA Gate)
*The final gate before merge.*

- [ ] **Concurrency Check:** Does this feature fail under simultaneous access? (Use parallel test scripts).
- [ ] **Resource Contention:** Does this feature exhaust VRAM or block the GIL during heavy load?
- [ ] **Error Recovery:** Does the system gracefully recover from database connection drops or embedding service timeouts?
- [ ] **Regression Matrix:**
    - Document Ingestion (PASS/FAIL)
    - Retrieval Funnel (PASS/FAIL)
    - Chat Grounding (PASS/FAIL)
    - Database Integrity (PASS/FAIL)

---

## 4. Final Sign-off Template
*This template must be attached to every major Feature PR.*

```markdown
# Implementation Sign-off

## Feature: [NAME]
- [ ] Architecture Compliance Verified
- [ ] Code Review Completed (No critical blockers)
- [ ] Automated Test Suite Passed
- [ ] Regression Tests Verified
- [ ] Documentation Updated (Manifest/Roadmap)

## Assessment
- Correctness: /10
- Reliability: /10
- Performance: /10

## Final Verdict:
[ ] Approved for Merge
[ ] Approved with Minor Fixes
[ ] Requires Rework
[ ] Reject
```
