"""
Unit tests for the MCP server.
"""

import pytest
from src.mcp_server.config import Config

def test_config_defaults():
    assert Config.HOST == "0.0.0.0"
    assert Config.PORT == 8000