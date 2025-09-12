"""
Utility functions for handling embeddings.
"""

from langchain.embeddings import OpenAIEmbeddings

def get_embeddings(model_name: str = "text-embedding-ada-002"):
    """
    Initialize and return an OpenAI embeddings instance.

    Args:
        model_name: Name of the embedding model.

    Returns:
        OpenAIEmbeddings instance.
    """
    return OpenAIEmbeddings(model=model_name)