# ROADMAP: Pryneboard 2.0

## Phase 1: Foundation (The Merger)
**Goal:** Establish the unified backend and ingestion pipeline.
- [x] Merge Odysseus FastAPI core with Hopper's specialized processing logic. (Implemented in 1.1/1.2)
- [x] Implement Unified Ingestion Pipeline (supporting PDF, JSON, Web, and Discord). (1.1 Core done)
- [ ] Migrate `hopper_harvest.py` into a core Pryneboard background service.
- [x] Establish ChromaDB as the primary vector store with SHA-256 deduplication.

## Phase 2: Intelligence (High-Precision RAG)
**Goal:** Implement advanced retrieval and agent capabilities.
- [x] Port Hopper's two-stage retrieval (Vector + Reranking) to Python.
- [x] Add support for local reranking models (Cross-Encoders) via the Cookbook.
- [x] Integrate MCP (Model Context Protocol) as the primary tool extension mechanism.
- [ ] Enhance Agent Loop with "Namespace Awareness" (agents can intelligently switch contexts).

## Phase 3: Experience (The Modern Workspace)
**Goal:** Launch the new React/Tailwind frontend.
- [ ] Implement new "Workspace" UI with multi-window support (Chat, Editor, Gallery).
- [x] Stream AI responses as HTML with Tailwind styling (Hopper style).
- [x] Implement specialized document processing (CSV tables, PDF metadata).
- [x] Add YouTube Analysis tool (Transcripts + Comments via yt-dlp).
- [x] Build backend API for Knowledge Dashboard (Source listing + Ingestion).
- [x] Implement Knowledge Dashboard UI shell (Modal + Sidebar access).
- [ ] Build the "Knowledge Dashboard" ingestion controls (Add Source form).
- [ ] Implement "Visual Citations" (thumbnails/links for sources).

## Phase 4: Ecosystem (Advanced Automation)
**Goal:** Deep integration and local-first autonomy.
- [ ] Full local Vision support (LLaVA/Moondream) for image analysis.
- [ ] Local Speech-to-Text (Whisper) and Text-to-Speech integration.
- [ ] Advanced "Tasks" system: autonomous background agents for research and housekeeping.
- [ ] Mobile-optimized PWA with local-sync capabilities.
