# DOMAIN MODEL: Pryneboard 2.0

## Core Entities

### 1. Knowledge Domain
- **Namespace:** A logical boundary for data (e.g., `work`, `personal`, `discord_activity`). Every query is scoped to a namespace.
- **Source:** The origin of data (a PDF file, a Discord channel, a Web URL).
- **Document:** A processed unit of knowledge containing `content`, `metadata`, and a `content_hash`.
- **Chunk:** A semantic fragment of a Document used for vector indexing.

### 2. Interaction Domain
- **Conversation:** A stateful thread of interaction between a User and an Assistant.
- **Message:** An individual turn in a conversation (User, Assistant, or System).
- **Turn:** A single execution cycle of the LLM, potentially including tool calls.

### 3. Intelligence Domain
- **Agent:** A specialized persona with specific system instructions and tool access.
- **Tool:** A function an Agent can execute (e.g., `read_file`, `send_email`).
- **MCP Server:** An external process providing a set of Tools via the Model Context Protocol.
- **Task:** A persistent unit of asynchronous work (e.g., "Summarize last week's Discord logs").

### 4. System Domain
- **Cookbook / Model:** A configuration for a local or remote AI model (Parameters, Quantization, Backend).
- **Provider:** An interface to an AI service (Ollama, vLLM, Groq, OpenAI).
- **Integration:** A third-party service connection (IMAP/SMTP for Email, CalDAV for Calendar).

---

## Relationships
- A `Namespace` contains many `Documents`.
- A `Document` is split into many `Chunks`.
- A `Conversation` is associated with an `Agent` and a `Namespace`.
- An `Agent` uses many `Tools` provided by one or more `MCP Servers`.
- a `Task` can generate `Documents` (e.g., a Research Report).
