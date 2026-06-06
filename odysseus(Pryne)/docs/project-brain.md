# Project Brain (docs/project-brain.md)

## Executive Summary
Odysseus is a comprehensive, self-hosted AI workspace that provides local, privacy-conscious alternatives to commercial AI tools.

## Core Features
- Multi-model Chat (Local/API)
- Task-capable AI Agents (built on `opencode`, MCP)
- Cookbook (Hardware-aware model installation/serving)
- Deep Research (Synthesized reporting)
- Documents (AI-assisted editor)
- Persistent Memory (ChromaDB)
- Native integrations: Email, Calendar, Notes, Tasks.

## System Architecture
Odysseus acts as a high-level manager that orchestrates local services and AI providers. The web server (FastAPI) provides an authenticated entry point, while background workers manage tasks, MCP connections, and model downloads.

## Data Flow
User Requests → FastAPI Routes → Logic Managers (src/services) → AI Provider/Local Model OR Database/VectorDB → Response.

## Key Modules
- `core/`: Infrastructure components (Auth, DB, Middleware).
- `src/`: AI Interaction, Agent loop, Tool orchestration.
- `routes/`: API & UI endpoint handling.
- `services/`: Specialized domain logic (Memory, Research, TTS/STT, etc.).

## Technical Debt / Known Limitations
- Heavy dependence on external model serving infrastructure (when not using simple APIs).
- Complexity of local-first cross-platform deployment (Windows/Linux/macOS disparities).
- Potential for bloat in `app.py` due to manual route registration.

## Roadmap
- Improving mobile-first UI experiences.
- Enhancing agent autonomy and tool reliability.
- Expanding local-first integration capabilities.
