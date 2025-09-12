"""
Unit tests for the RAGAgent class.
"""

import pytest
from src.agent.rag_agent import RAGAgent

@pytest.fixture
def mock_config():
    return {"vector_db_path": "./data/vector_db"}

def test_rag_agent_initialization(mock_config):
    agent = RAGAgent(mock_config)
    assert agent.vector_db_path == mock_config["vector_db_path"]