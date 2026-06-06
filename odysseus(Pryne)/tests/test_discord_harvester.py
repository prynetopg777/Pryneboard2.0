
import pytest
import os
import tempfile
from unittest.mock import MagicMock, patch
from src.integrations.discord_parser import parse_and_chunk_discord_messages
from src.integrations.discord_harvester import ingest_discord_file

# --- Discord Parser Tests ---

def test_parser_standard_message():
    """Verify standard discord message parsing."""
    content = "This is a message.\n- Bullet point 1\n- Bullet point 2"
    results = parse_and_chunk_discord_messages(
        content, "Tester", "2026-06-05", "TestServer", "general"
    )
    assert len(results) >= 1
    assert "Server: TestServer" in results[0]
    assert "Tester" in results[0]
    assert "Bullet point 1" in results[0]

# --- Discord Harvester Tests ---

@patch('src.integrations.discord_harvester.VectorRAG')
def test_ingest_discord_file(mock_rag_class):
    """Verify ingestion pipeline integration."""
    # Setup
    mock_rag = MagicMock()
    mock_rag.healthy = True
    mock_rag_class.return_value = mock_rag
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        tmp.write("Chunk 1\n\n---\n\nChunk 2")
        tmp_path = tmp.name

    try:
        result = ingest_discord_file(tmp_path, "user1", "test-namespace")
        
        # Verify
        assert result['success'] is True
        assert mock_rag.add_documents_batch.called
        
        # Check if hash was passed
        args, _ = mock_rag.add_documents_batch.call_args
        docs = args[0]
        assert len(docs) == 2
        assert "content_hash" in docs[0][1]
    finally:
        os.remove(tmp_path)

@patch('src.integrations.discord_harvester.VectorRAG')
def test_ingest_discord_deduplication(mock_rag_class):
    """Verify that batch ingestion respects deduplication."""
    mock_rag = MagicMock()
    mock_rag.healthy = True
    # Simulate partial failure or duplication
    mock_rag.add_documents_batch.return_value = {"success": True, "added_count": 0}
    mock_rag_class.return_value = mock_rag
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        tmp.write("Duplicate Chunk")
        tmp_path = tmp.name

    try:
        result = ingest_discord_file(tmp_path, "user1", "test-namespace")
        assert result['added_count'] == 0
    finally:
        os.remove(tmp_path)
