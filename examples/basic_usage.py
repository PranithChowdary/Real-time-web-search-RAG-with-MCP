"""
Basic usage example for RAG-MCP Assistant
Demonstrates simple query processing
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from src.agent.orchestrator import RAGMCPOrchestrator

async def main():
    """Basic usage demonstration"""
    
    # Initialize the assistant
    config = {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "serpapi_key": os.getenv("SERPAPI_KEY"),
        "vector_db_path": "./data/vector_db",
        "confidence_threshold": 0.7
    }
    
    assistant = RAGMCPOrchestrator(config)
    
    # Example queries
    queries = [
        "What is machine learning?",
        "Latest developments in AI agents for 2025",
        "How does retrieval-augmented generation work?",
        "Current trends in large language models"
    ]
    
    print("🤖 RAG-MCP Assistant Demo")
    print("=" * 50)
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 40)
        
        try:
            result = await assistant.query(
                query_text=query,
                include_sources=True,
                max_results=3
            )
            
            print(f"Method: {result.search_method}")
            print(f"Confidence: {result.confidence:.2f}")
            print(f"Time: {result.execution_time:.2f}s")
            print(f"\nResponse:\n{result.response}")
            
            if result.sources:
                print(f"\nSources ({len(result.sources)}):")
                for j, source in enumerate(result.sources[:2], 1):
                    print(f"  {j}. {source.get('title', 'No title')[:60]}...")
        
        except Exception as e:
            print(f"Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Demo completed!")

if __name__ == "__main__":
    asyncio.run(main())
