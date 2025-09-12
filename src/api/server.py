"""
FastAPI server for the RAG-MCP Assistant.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    max_results: int = 5

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/query")
async def query(request: QueryRequest):
    # Placeholder for query handling logic
    return {
        "query": request.query,
        "max_results": request.max_results,
        "response": "This is a placeholder response."
    }