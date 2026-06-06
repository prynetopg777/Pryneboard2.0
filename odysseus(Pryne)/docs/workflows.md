# Workflows (docs/workflows.md)

## Authentication Flow
`app.py` → `core.middleware.AuthMiddleware` intercepts requests, validates session cookies (from `routes.auth_routes`) or API Bearer tokens, and sets `request.state.current_user`.

## Request Lifecycle
1. Request received by `app.py`.
2. `AuthMiddleware` verifies authentication.
3. FastAPI routes to a handler in `routes/`.
4. Handler uses `src/` logic or `services/` to process request.
5. Response returned to client.

## Background Jobs
`src/task_scheduler.py` (via `app.py` lifespan) handles scheduled tasks (calendar sync, cleanup, housekeeping).

## Agent/Tool Execution
Agent tasks are driven by `src/agent_loop.py` using tools registered in `src/agent_tools.py`, often leveraging MCP servers managed by `src/mcp_manager.py`.
