
import os
import logging
from typing import List, Dict, Any
from src.document_processor import calculate_content_hash
from src.rag_vector import VectorRAG

logger = logging.getLogger(__name__)

def ingest_discord_file(file_path: str, owner: str, namespace: str) -> Dict[str, Any]:
    """
    Ingests a pre-chunked Discord log file into the VectorRAG system.
    """
    if not os.path.exists(file_path):
        return {"success": False, "message": "File not found"}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # The Hopper format uses '\n\n---\n\n' as a delimiter
            raw_content = f.read()
            chunks = [c.strip() for c in raw_content.split('\n\n---\n\n') if c.strip()]

        rag = VectorRAG()
        if not rag.healthy:
            return {"success": False, "message": "RAG system not healthy"}

        docs_to_add = []
        for chunk in chunks:
            content_hash = calculate_content_hash(chunk)
            metadata = {
                "owner": owner,
                "namespace": namespace,
                "content_hash": content_hash,
                "source": file_path,
                "type": "discord"
            }
            docs_to_add.append((chunk, metadata))

        result = rag.add_documents_batch(docs_to_add)
        
        logger.info(f"Successfully ingested {result.get('added_count')} Discord chunks from {file_path}")
        return result

    except Exception as e:
        logger.error(f"Error ingesting Discord file {file_path}: {e}")
        return {"success": False, "message": str(e)}
