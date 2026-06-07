import logging
from typing import List, Dict, Any
from src.rag_vector import VectorRAG

logger = logging.getLogger(__name__)

class ChromaAdapter:
    """Infrastructure adapter for ChromaDB."""
    def __init__(self):
        # Initialize directly or get instance
        from src.rag_singleton import get_rag_manager
        self.rag = get_rag_manager()
        logger.info("ChromaAdapter initialized.")

    async def search(self, query: str, limit: int = 50, namespace: Optional[str] = None) -> List[Dict[str, Any]]:
        """Perform vector search and return candidates with content."""
        logger.info(f"Performing vector search for: {query} (namespace: {namespace})")
        
        # Use vector_rag directly from the RAGManager (which is the instance from rag_singleton)
        if self.rag:
            # Pass namespace if supported by the underlying rag.search
            results = self.rag.vector_rag.search(query, k=limit, namespace=namespace)
            
            # Normalize to expected dict format
            candidates = []
            for r in results:
                candidates.append({
                    "content": r.get("document", ""),
                    "metadata": r.get("metadata", {})
                })
            return candidates
        return []

    async def exists_by_hash(self, content_hash: str) -> bool:
        """Check if a document exists by SHA-256 hash."""
        if self.rag:
            return self.rag.vector_rag.exists_by_hash(content_hash)
        return False
