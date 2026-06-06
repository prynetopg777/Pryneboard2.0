import sys
import os
import hashlib
import uuid
import logging
from unittest.mock import MagicMock, patch
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock heavy/optional dependencies before imports
mock_modules = {
    'chromadb': MagicMock(),
    'src.rag.chroma_client': MagicMock(),
    'src.embeddings': MagicMock(),
    'src.auth_helpers': MagicMock(),
    'src.pdf_forms': MagicMock(),
    'src.pdf_form_doc': MagicMock(),
}

with patch.dict('sys.modules', mock_modules):
    from src.rag_vector import VectorRAG, _generate_doc_id
    from src.document_processor import calculate_content_hash
    from routes.document_routes import setup_document_routes
    from core.database import Document

# --- Functional Tests ---

def test_calculate_content_hash():
    """Verify hash creation and normalization."""
    text = "  Hello World  "
    expected = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
    assert calculate_content_hash(text) == expected
    assert calculate_content_hash("") == ""

def test_min_content_threshold_rag():
    """Verify VectorRAG blocks low-content ingestion."""
    mock_rag = VectorRAG.__new__(VectorRAG)
    mock_rag._healthy = True
    
    short_text = "short"
    assert mock_rag.add_document(short_text, {"owner": "test"}) is False

def test_add_document_deduplication_logic():
    """Verify VectorRAG deduplication logic (ID and Hash checks)."""
    mock_collection = MagicMock()
    mock_rag = VectorRAG.__new__(VectorRAG)
    mock_rag._collection = mock_collection
    mock_rag._healthy = True
    mock_rag._embed = MagicMock(return_value=[[0.1]*1536])
    
    text = "This is a long enough document to pass the threshold check in VectorRAG."
    owner = "alice"
    content_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
    metadata = {"content_hash": content_hash, "owner": owner}
    
    # Case 1: New document
    mock_collection.get.return_value = {"ids": [], "metadatas": []}
    assert mock_rag.add_document(text, metadata) is True
    assert mock_collection.add.called
    
    # Case 2: Duplicate by ID
    doc_id = _generate_doc_id(text, owner)
    mock_collection.get.return_value = {"ids": [doc_id], "metadatas": [metadata]}
    mock_collection.add.reset_mock()
    assert mock_rag.add_document(text, metadata) is True
    # Should return True but skip adding
    assert not mock_collection.add.called

    # Case 3: Duplicate by Hash (different ID)
    mock_collection.get.reset_mock()
    mock_collection.get.side_effect = [
        {"ids": [], "metadatas": []}, # ID check fails
        {"ids": ["other_doc_id"], "metadatas": [{"owner": owner, "content_hash": content_hash}]} # Hash check hits
    ]
    assert mock_rag.add_document(text, metadata) is True
    assert not mock_collection.add.called

def test_legacy_id_fallback_rag():
    """Verify 2.0 can detect 1.0 legacy IDs."""
    mock_collection = MagicMock()
    mock_rag = VectorRAG.__new__(VectorRAG)
    mock_rag._collection = mock_collection
    mock_rag._healthy = True
    
    text = "Legacy document content test legacy document content test."
    owner = "alice"
    
    legacy_id = f"doc_{hashlib.sha256((f'{owner}\\x00{text}' if owner else text).encode('utf-8')).hexdigest()[:16]}"
    
    mock_collection.get.return_value = {"ids": [legacy_id], "metadatas": [{"owner": owner}]}
    
    assert mock_rag.add_document(text, {"owner": owner}) is True
    # Verify that it queried for both full and legacy ID
    args, kwargs = mock_collection.get.call_args
    requested_ids = kwargs.get('ids', [])
    assert legacy_id in requested_ids
    assert len(requested_ids[0]) == 68 # "doc_" + 64 chars

def test_two_stage_retrieval_rag():
    """Verify VectorRAG search implements over-fetch and reranking."""
    mock_collection = MagicMock()
    mock_reranker = MagicMock()
    
    mock_rag = VectorRAG.__new__(VectorRAG)
    mock_rag._collection = mock_collection
    mock_rag._healthy = True
    mock_rag._reranker = mock_reranker
    mock_rag._embed = MagicMock(return_value=[[0.1]*1536])
    
    query = "test query"
    # Stage 1 Mock: Return 3 candidates
    mock_collection.query.return_value = {
        "ids": [["id1", "id2", "id3"]],
        "distances": [[0.5, 0.4, 0.3]], # Cosine dists
        "documents": [["doc1", "doc2", "doc3"]],
        "metadatas": [[{}, {}, {}]]
    }
    mock_collection.count.return_value = 100
    
    # Stage 2 Mock: Rerank gives doc3 the highest score
    mock_reranker.rerank.return_value = [0.1, 0.2, 0.9] # Scores for doc1, doc2, doc3
    
    results = mock_rag.search(query, k=1)
    
    assert len(results) == 1
    # doc3 should be first because of rerank score 0.9
    assert results[0]["document"] == "doc3"
    assert results[0]["rerank_score"] == 0.9
    assert results[0]["similarity"] == 0.9

# --- API Level Tests ---

@pytest.mark.asyncio
async def test_import_pdf_min_threshold_api():
    """Verify API blocks low-content PDF imports."""
    from routes.document_routes import setup_document_routes
    
    # Mock dependencies for setup_document_routes
    session_manager = MagicMock()
    upload_handler = MagicMock()
    
    # Mocking _process_pdf and other internals
    with patch('routes.document_routes._process_pdf', return_value="Too short"), \
         patch('routes.document_routes.strip_pdf_content_marker', side_effect=lambda x: x), \
         patch('routes.document_routes.require_privilege', return_value="alice"), \
         patch('routes.document_routes.SessionLocal') as mock_session_local:
        
        router = setup_document_routes(session_manager, upload_handler)
        import_pdf = next(r.endpoint for r in router.routes if r.path == "/api/documents/import-pdf")
        
        request = SimpleNamespace(
            client=SimpleNamespace(host="127.0.0.1"),
            app=SimpleNamespace(state=SimpleNamespace(auth_manager=MagicMock()))
        )
        file = MagicMock()
        
        upload_handler.save_upload.return_value = {"id": "up1", "original_name": "test.pdf"}
        
        with patch('routes.document_routes._locate_current_user_upload', return_value="/path/to/test.pdf"):
            with pytest.raises(HTTPException) as exc:
                await import_pdf(request, file)
            assert exc.value.status_code == 400
            assert "insufficient readable text" in exc.value.detail

@pytest.mark.asyncio
async def test_import_pdf_duplicate_detection_api():
    """Verify API detects duplicates via content_hash."""
    from routes.document_routes import setup_document_routes
    
    session_manager = MagicMock()
    upload_handler = MagicMock()
    
    content = "This is a long enough document content for testing duplicate detection in the API."
    content_hash = calculate_content_hash(content)
    
    with patch('routes.document_routes._process_pdf', return_value=content), \
         patch('routes.document_routes.strip_pdf_content_marker', side_effect=lambda x: x), \
         patch('routes.document_routes.require_privilege', return_value="alice"), \
         patch('routes.document_routes.SessionLocal') as mock_session_local:
        
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        
        # Simulate existing document
        existing_doc = Document(id="existing_id", title="Existing Doc", content_hash=content_hash, owner="alice")
        mock_db.query.return_value.filter.return_value.first.return_value = existing_doc
        
        router = setup_document_routes(session_manager, upload_handler)
        import_pdf = next(r.endpoint for r in router.routes if r.path == "/api/documents/import-pdf")
        
        request = SimpleNamespace(
            client=SimpleNamespace(host="127.0.0.1"),
            app=SimpleNamespace(state=SimpleNamespace(auth_manager=MagicMock()))
        )
        file = MagicMock()
        upload_handler.save_upload.return_value = {"id": "up1", "original_name": "test.pdf"}
        
        with patch('routes.document_routes._locate_current_user_upload', return_value="/path/to/test.pdf"), \
             patch('routes.document_routes._doc_to_dict', return_value={"id": "existing_id"}):
            
            result = await import_pdf(request, file)
            assert result["is_duplicate"] is True
            assert result["id"] == "existing_id"
