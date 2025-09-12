"""
Command-line interface demo for the RAG-MCP Assistant.
"""

import argparse
from src.agent.rag_agent import RAGAgent

def main():
    parser = argparse.ArgumentParser(description="RAG-MCP Assistant CLI")
    parser.add_argument("query", type=str, help="The query to process")
    args = parser.parse_args()

    # Initialize the RAG agent
    config = {"vector_db_path": "./data/vector_db"}
    agent = RAGAgent(config)

    # Process the query
    response = agent.answer_query(args.query)

    print(f"Query: {args.query}")
    print(f"Response: {response}")

if __name__ == "__main__":
    main()