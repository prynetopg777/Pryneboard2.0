"""
rag_manager.py

A thin wrapper around VectorRAG for backward compatibility and additional features.
"""

import logging
from typing import List, Dict, Any

# Try to import from different possible locations
try:
    from rag_vector import VectorRAG
except ImportError:
    try:
        from .rag_vector import VectorRAG
    except ImportError:
        from src.rag_vector import VectorRAG

logger = logging.getLogger(__name__)

class RAGManager:
    """
    A manager class that wraps VectorRAG for storage/indexing 
    and RetrievalService for precision retrieval.
    """
    
    def __init__(self, persist_directory: str = "data/chroma"):
        """Initialize the RAGManager with VectorRAG and RetrievalService."""
        from src.rag_vector import VectorRAG
        from src.domain.retrieval_service import RetrievalService
        
        self.vector_rag = VectorRAG(persist_directory=persist_directory)
        self.retrieval_service = RetrievalService()
        logger.info("RAGManager initialized with VectorRAG and RetrievalService")
    
    def search(self, query: str, k: int = 5, owner: Optional[str] = None, namespace: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for documents - delegates to RetrievalService for high-precision retrieval."""
        import asyncio
        # RAGManager is synchronous; bridge to async RetrievalService
        try:
            loop = asyncio.get_event_loop()
            # Convert Dict to list of dicts with 'document' key for backward compatibility
            results = loop.run_until_complete(self.retrieval_service.get_grounded_context(query, top_k=k, namespace=namespace))
            return [{"document": r["content"], "metadata": r["metadata"], "score": r.get("score", 0.0)} for r in results]
        except Exception as e:
            logger.error(f"RetrievalService search failed: {e}. Falling back to VectorRAG.")
            return self.vector_rag.search(query, k=k, owner=owner, namespace=namespace)

    
    def retrieve(self, query: str, k: int = 5) -> List[str]:
        """Retrieve relevant chunks - delegates to RetrievalService."""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            results = loop.run_until_complete(self.retrieval_service.get_grounded_context(query, top_k=k))
            return [r["content"] for r in results]
        except Exception as e:
            logger.error(f"RetrievalService retrieve failed: {e}. Falling back to VectorRAG.")
            return self.vector_rag.retrieve(query, k)

    def index_personal_documents(self, directory: str, owner: str = None) -> Dict[str, Any]:
        """Index documents - delegates to VectorRAG."""
        return self.vector_rag.index_personal_documents(directory, owner=owner)
    
    def rebuild_index(self) -> bool:
        """Rebuild index - delegates to VectorRAG."""
        return self.vector_rag.rebuild_index()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get stats - delegates to VectorRAG."""
        return self.vector_rag.get_stats()
    
    def add_document(self, text: str, metadata: Dict[str, Any]) -> bool:
        """Add single document - delegates to VectorRAG."""
        return self.vector_rag.add_document(text, metadata)
    
    def add_documents_batch(self, docs: List[tuple]) -> Dict[str, Any]:
        """Add documents in batch - delegates to VectorRAG."""
        return self.vector_rag.add_documents_batch(docs)
