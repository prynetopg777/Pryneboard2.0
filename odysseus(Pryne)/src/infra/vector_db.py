import logging
from typing import List, Dict, Any
from chromadb import Client, Collection
from src.rag_vector import get_rag_manager

logger = logging.getLogger(__name__)

class ChromaAdapter:
    """Infrastructure adapter for ChromaDB."""
    def __init__(self):
        self.rag_manager = get_rag_manager()
        logger.info("ChromaAdapter initialized.")

    async def search(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Perform vector search and return candidates with content."""
        logger.info(f"Performing vector search for: {query}")
        
        # Access underlying chroma collection
        results = self.rag_manager.search(query, k=limit)
        
        # Normalize to expected dict format
        candidates = []
        for r in results:
            candidates.append({
                "content": r.get("document", ""),
                "metadata": r.get("metadata", {})
            })
        return candidates

    async def exists_by_hash(self, content_hash: str) -> bool:
        """Check if a document exists by SHA-256 hash."""
        # This assumes the hash is stored in metadata
        return self.rag_manager.exists_by_hash(content_hash)
