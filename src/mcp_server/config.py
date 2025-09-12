"""
Configuration settings for the MCP server.
"""

import os

class Config:
    HOST = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
    PORT = int(os.getenv("MCP_SERVER_PORT", 8000))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    TIMEOUT = int(os.getenv("WEB_SEARCH_TIMEOUT", 30))