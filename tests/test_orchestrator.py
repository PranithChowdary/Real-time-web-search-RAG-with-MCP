"""
Unit tests for the RAGMCPOrchestrator class.
"""

import pytest
from src.agent.orchestrator import RAGMCPOrchestrator

@pytest.fixture
def mock_config():
    return {"confidence_threshold": 0.7}

def test_orchestrator_initialization(mock_config):
    orchestrator = RAGMCPOrchestrator(mock_config)
    assert orchestrator.confidence_threshold == mock_config["confidence_threshold"]