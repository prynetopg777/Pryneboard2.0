from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class PryneDocument(BaseModel):
    """The unified schema for all ingested content."""
    id: str  # SHA-256 hash
    content: str
    metadata: Dict[str, Any]
    source_type: str  # 'pdf', 'youtube', 'discord', etc.
    created_at: datetime = Field(default_factory=datetime.utcnow)
