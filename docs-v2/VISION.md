# VISION: Pryneboard 2.0

## The Core Philosophy
Pryneboard 2.0 is built on the belief that **Privacy is a Feature, not a Constraint**. It is a local-first AI workspace designed for professionals who require the power of modern LLMs but cannot compromise on data sovereignty.

### 1. Sovereignty by Default
Every byte of data—from Discord logs to personal notes—resides on the user's hardware. The system is designed to function entirely offline, using local models (via Ollama/vLLM) and local vector stores (ChromaDB).

### 2. High-Precision Intelligence
Unlike generic chat interfaces, Pryneboard 2.0 prioritizes **Contextual Integrity**. By integrating Hopper's advanced RAG (Retrieval-Augmented Generation) pipeline, it ensures that AI responses are grounded in verified local data with strict source attribution.

### 3. Action-Oriented Agency
Pryneboard is not just a chatbot; it is an **Orchestrator**. Through its Agent loop and MCP (Model Context Protocol) integration, it can perform real-world tasks: managing calendars, parsing complex Discord activity, conducting deep research, and automating workflows.

## The Mission
To provide a professional-grade AI workspace that rivals commercial cloud platforms (ChatGPT, Claude) in capability while exceeding them in privacy, customizability, and data ownership.

## Key Tenets
- **Local-First:** Prioritize local execution for all AI tasks.
- **Precision over Speed:** Use reranking and semantic deduplication to ensure the highest quality context.
- **Modularity:** Separate the "Harvesters" (data collection), "Intelligence" (RAG/Agents), and "Interface" (UI) layers for long-term maintainability.
- **Transparency:** Every AI decision should be traceable to a source or a tool execution log.
