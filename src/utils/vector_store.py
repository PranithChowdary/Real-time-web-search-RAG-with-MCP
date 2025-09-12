"""
Utility functions for managing vector stores.
"""

from langchain.vectorstores import FAISS
from langchain.schema import Document

def create_vector_store(docs: list, embeddings, path: str):
    """
    Create and save a vector store.

    Args:
        docs: List of documents to add to the vector store.
        embeddings: Embeddings instance.
        path: Path to save the vector store.

    Returns:
        FAISS vector store instance.
    """
    vector_store = FAISS.from_documents(docs, embeddings)
    vector_store.save_local(path)
    return vector_store

def load_vector_store(path: str, embeddings):
    """
    Load an existing vector store.

    Args:
        path: Path to the vector store.
        embeddings: Embeddings instance.

    Returns:
        FAISS vector store instance.
    """
    return FAISS.load_local(path, embeddings)