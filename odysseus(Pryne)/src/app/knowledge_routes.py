from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from typing import Dict, Any
from src.domain.ingestion_service import UnifiedIngestionService
from src.rag_manager import RAGManager

def setup_knowledge_routes(ingestion_service: UnifiedIngestionService, rag_manager: RAGManager):
    router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

    @router.get("/sources")
    async def list_sources():
        """List all indexed sources."""
        # Accessing underlying Chroma collection directly for listing
        try:
            results = rag_manager.vector_rag._collection.get(include=["metadatas"])
            sources = []
            for meta in results.get("metadatas", []):
                if meta not in sources:
                    sources.append(meta)
            return {"sources": sources}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/ingest")
    async def ingest_source(
        background_tasks: BackgroundTasks,
        url_or_path: str,
        source_type: str,
        metadata: Dict[str, Any] = None
    ):
        """Trigger ingestion of a new source."""
        background_tasks.add_task(ingestion_service.ingest_source, url_or_path, source_type, metadata)
        return {"status": "Ingestion triggered in background"}

    return router
