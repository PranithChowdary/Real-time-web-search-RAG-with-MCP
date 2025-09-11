"""
Main orchestrator for RAG-MCP Assistant
Manages the decision flow between local RAG and web search
"""
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage

from .rag_agent import RAGAgent
from .mcp_client import MCPClient
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

@dataclass
class QueryResult:
    response: str
    sources: List[Dict[str, Any]]
    confidence: float
    search_method: str
    execution_time: float

class RAGMCPOrchestrator:
    """
    Main orchestrator that combines RAG with MCP web search capabilities
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.confidence_threshold = float(self.config.get("confidence_threshold", 0.7))
        
        # Initialize components
        self.rag_agent = RAGAgent(config)
        self.mcp_client = MCPClient(config)
        self.llm = ChatOpenAI(
            model=self.config.get("openai_model", "gpt-4-turbo-preview"),
            temperature=float(self.config.get("temperature", 0.7))
        )
        
        logger.info("RAG-MCP Orchestrator initialized")
    
    async def query(self, 
                   query_text: str, 
                   force_web_search: bool = False,
                   include_sources: bool = True,
                   max_results: int = 5) -> QueryResult:
        """
        Process a query using RAG first, then MCP fallback if needed
        
        Args:
            query_text: The user's question
            force_web_search: Skip RAG and go directly to web search
            include_sources: Include source information in response
            max_results: Maximum number of results to return
            
        Returns:
            QueryResult with response, sources, and metadata
        """
        import time
        start_time = time.time()
        
        try:
            # Try RAG first unless forced to use web search
            if not force_web_search:
                rag_result = await self.rag_agent.search(query_text, max_results)
                
                if rag_result.confidence >= self.confidence_threshold:
                    logger.info(f"Query answered using RAG (confidence: {rag_result.confidence})")
                    return QueryResult(
                        response=rag_result.response,
                        sources=rag_result.sources if include_sources else [],
                        confidence=rag_result.confidence,
                        search_method="rag",
                        execution_time=time.time() - start_time
                    )
                
                logger.info(f"RAG confidence too low ({rag_result.confidence}), falling back to web search")
            
            # Fallback to web search via MCP
            web_result = await self.mcp_client.search(query_text, max_results)
            
            # Combine RAG context (if available) with web results
            combined_response = await self._combine_results(
                query_text, 
                rag_result if not force_web_search else None,
                web_result
            )
            
            return QueryResult(
                response=combined_response,
                sources=web_result.get("sources", []) if include_sources else [],
                confidence=0.9,  # High confidence for web results
                search_method="mcp_web",
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return QueryResult(
                response=f"I apologize, but I encountered an error processing your query: {str(e)}",
                sources=[],
                confidence=0.0,
                search_method="error",
                execution_time=time.time() - start_time
            )
    
    async def _combine_results(self, query: str, rag_result: Optional[Any], web_result: Dict) -> str:
        """Combine RAG and web search results into a coherent response"""
        
        context_parts = []
        
        if rag_result and rag_result.confidence > 0.3:
            context_parts.append(f"Local Knowledge: {rag_result.response}")
        
        if web_result.get("content"):
            context_parts.append(f"Web Search Results: {web_result['content']}")
        
        system_prompt = """You are an AI assistant that provides comprehensive answers by combining local knowledge with real-time web search results. 

Your task:
1. Synthesize information from both local and web sources
2. Provide accurate, up-to-date information
3. Clearly indicate when information comes from web sources
4. If there are conflicts, prioritize more recent web information
5. Be concise but comprehensive

Context available: {context}

User query: {query}

Provide a well-structured response that addresses the query completely."""

        messages = [
            SystemMessage(content=system_prompt.format(
                context="\n\n".join(context_parts),
                query=query
            )),
            HumanMessage(content=query)
        ]
        
        response = await self.llm.agenerate([messages])
        return response.generations[0][0].text.strip()
    
    async def add_documents(self, documents: List[str]) -> None:
        """Add new documents to the RAG system"""
        await self.rag_agent.add_documents(documents)
        logger.info(f"Added {len(documents)} documents to RAG system")
    
    async def update_vector_store(self) -> None:
        """Refresh the vector database"""
        await self.rag_agent.update_vector_store()
        logger.info("Vector store updated")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get system health status"""
        return {
            "rag_agent": self.rag_agent.is_healthy(),
            "mcp_client": self.mcp_client.is_healthy(),
            "llm": True,  # Simple check - could be enhanced
            "timestamp": time.time()
        }