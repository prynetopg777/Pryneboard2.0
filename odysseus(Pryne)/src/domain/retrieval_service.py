import logging
from typing import List, Dict, Any
from src.core.models import PryneDocument
from src.infra.vector_db import ChromaAdapter
from src.infra.reranker import RerankerAdapter

logger = logging.getLogger(__name__)

class RetrievalService:
    """
    Bridge service for high-precision retrieval.
    Decouples agent loop from specific vector DB or reranking implementations.
    """
    def __init__(self):
        self.db = ChromaAdapter()
        self.reranker = RerankerAdapter()
        logger.info("RetrievalService initialized.")

    async def get_grounded_context(self, query: str, top_k: int = 5, namespace: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Executes the two-stage pipeline:
        1. Vector search to find candidates.
        2. Reranking for high-precision grounding.
        """
        logger.info(f"Executing two-stage retrieval for: {query} (namespace: {namespace})")
        
        # 1. Vector + Keyword Hybrid Search (from underlying ChromaAdapter)
        # Assuming search returns candidates with 'content' and 'metadata'
        candidates = await self.db.search(query, limit=top_k * 10, namespace=namespace)
        
        if not candidates:
            return []

        # 2. Reranking for high-precision
        reranked = await self.reranker.rerank(query, candidates, top_n=top_k)
        
        # 3. Format as PryneDocument
        final_docs = []
        for cand in reranked:
            final_docs.append({
                "content": cand["content"],
                "metadata": cand["metadata"],
                "score": cand.get("rerank_score", 0.0)
            })
            
        return final_docs
