# DOMAIN MODEL: Pryneboard 2.0

## Core Subsystems & Entities

### 1. Odysseus Core (src/app)
- **Session:** A chat or interaction context.
- **Message:** An individual turn in a conversation.
- **User:** Tenant definition.

### 2. Ingestion Pipeline (src/ingestion)
- **Source:** The origin of data.
- **Document:** A processed, chunked, and hashed unit of truth.

### 3. Knowledgebase (src/rag)
- **Namespace:** A logical boundary for data isolation.
- **Embedding:** Vector representation of a document chunk.

### 4. Agentic Runtime (src/agents)
- **Agent:** A specialized persona (Thought/Action/Observation).
- **Tool:** A function an Agent executes (MCP, Bash, Python).
- **Task:** An asynchronous unit of work.

### 5. Cookbook (src/cookbook)
- **Model:** Local/Remote AI model configuration.
- **Endpoint:** Connection definition to a model provider.
