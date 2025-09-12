"""
Advanced usage example for the RAG-MCP Assistant.
"""

from src.agent.rag_agent import RAGAgent
from src.agent.orchestrator import RAGMCPOrchestrator

def main():
    # Initialize the RAG agent and orchestrator
    agent_config = {"vector_db_path": "./data/vector_db"}
    orchestrator_config = {"confidence_threshold": 0.8}

    agent = RAGAgent(agent_config)
    orchestrator = RAGMCPOrchestrator(orchestrator_config)

    # Example query
    query = "Explain the theory of relativity."
    response = orchestrator.process_query(agent, query)

    print(f"Query: {query}")
    print(f"Response: {response}")

if __name__ == "__main__":
    main()