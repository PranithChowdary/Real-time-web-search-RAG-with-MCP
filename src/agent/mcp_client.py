# MCP - Client
import requests

class MCPClient:
    def __init__(self, config):
        self.url = config.get("mcp_server_url", "http://localhost:8000")

    async def search(self, query, max_results=5):
        payload = {"query": query, "num_results": max_results}
        resp = requests.post(f"{self.url}/mcp/search", json=payload, timeout=20)
        return resp.json()
    
    def is_healthy(self):
        try:
            resp = requests.get(f"{self.url}/mcp/health")
            return resp.status_code == 200
        except Exception:
            return False