import logging
import os
from typing import Dict, Any, Optional

from src.document_processor import calculate_content_hash, _process_text_file
from src.markitdown_runtime import convert_to_markdown
from services.youtube.youtube_handler import is_youtube_url, extract_youtube_id, extract_transcript_async
from src.rag_manager import get_rag_manager

logger = logging.getLogger(__name__)

class UnifiedIngestionService:
    """Service to handle unified ingestion of diverse sources into the RAG knowledgebase."""
    
    def __init__(self):
        self.rag_manager = get_rag_manager()
        logger.info("UnifiedIngestionService initialized.")

    async def ingest_source(self, path_or_url: str, source_type: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Ingest a source (file or URL) into the unified knowledgebase."""
        logger.info(f"Ingesting source: {path_or_url} (type: {source_type})")
        
        content = ""
        
        # 1. Extract Content
        if source_type == "youtube":
            if not is_youtube_url(path_or_url):
                return {"success": False, "error": "Invalid YouTube URL"}
            video_id = extract_youtube_id(path_or_url)
            transcript_data = await extract_transcript_async(path_or_url, video_id)
            if transcript_data.get("success"):
                content = transcript_data["transcript"]
            else:
                return {"success": False, "error": f"YouTube extraction failed: {transcript_data.get('error')}"}
        
        elif os.path.exists(path_or_url):
            # Check for markitdown formats
            if path_or_url.endswith((".docx", ".pptx", ".xlsx", ".epub")):
                content = convert_to_markdown(path_or_url) or ""
            else:
                content = _process_text_file(path_or_url)
        else:
            return {"success": False, "error": "Source not found or unsupported"}

        if not content:
            return {"success": False, "error": "No content extracted"}

        # 2. Deduplication using SHA-256
        content_hash = calculate_content_hash(content)
        if self.rag_manager.vector_rag.exists_by_hash(content_hash):
            logger.info(f"Duplicate content skipped for hash: {content_hash}")
            return {"success": True, "message": "Duplicate skipped"}

        # 3. Add to RAG
        meta = metadata or {}
        meta["content_hash"] = content_hash
        meta["source_path"] = path_or_url
        meta["source_type"] = source_type
        
        self.rag_manager.add_document(content, meta)
        
        logger.info(f"Successfully ingested source: {path_or_url}")
        return {"success": True, "content_hash": content_hash}
