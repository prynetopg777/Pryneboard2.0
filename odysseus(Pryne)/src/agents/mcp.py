"""
mcp.py

MCP-related initialization and server management utilities for the agent loop.
"""

import json
from typing import Dict, Set

def load_mcp_disabled_map() -> Dict[str, Set[str]]:
    """Load per-server disabled tool sets from the database."""
    from core.database import McpServer, SessionLocal
    disabled_map: Dict[str, Set[str]] = {}
    db = SessionLocal()
    try:
        for srv in db.query(McpServer).all():
            if srv.disabled_tools:
                try:
                    names = json.loads(srv.disabled_tools)
                    if names:
                        disabled_map[srv.id] = set(names)
                except (json.JSONDecodeError, TypeError):
                    pass
    finally:
        db.close()
    return disabled_map
