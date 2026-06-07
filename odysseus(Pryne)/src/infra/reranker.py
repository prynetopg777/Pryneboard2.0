import logging
from typing import List, Dict, Any
from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)

class RerankerAdapter:
    """Infrastructure adapter for BGE reranking models."""
    def __init__(self, model_name: str = 'BAAI/bge-reranker-v2-m3'):
        # Local model loading - will be optimized in future iterations
        self.model = CrossEncoder(model_name)
        logger.info(f"RerankerAdapter initialized with {model_name}")

    async def rerank(self, query: str, candidates: List[Dict[str, Any]], top_n: int = 3) -> List[Dict[str, Any]]:
        """Perform BGE reranking on candidates."""
        if not candidates:
            return []

        logger.info(f"Reranking {len(candidates)} candidates.")
        
        # Prepare pairs for the cross-encoder
        pairs = [(query, c['content']) for c in candidates]
        
        # Predict scores
        scores = self.model.predict(pairs)
        
        # Attach scores to candidates
        for i, score in enumerate(scores):
            candidates[i]['rerank_score'] = float(score)
            
        # Sort by rerank score descending
        candidates.sort(key=lambda x: x['rerank_score'], reverse=True)
        
        return candidates[:top_n]
