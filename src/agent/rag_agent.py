"""
RAG Agent implementation using LangChain and FAISS
Handles local document retrieval and similarity search
"""
import os
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.schema import Document

from ..utils.vector_store import VectorStoreManager
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

@dataclass
class RAGResult:
    response: str
    sources: List[Dict[str, Any]]
    confidence: float
    retrieved_docs: List[Document]

class RAGAgent:
    """
    Retrieval-Augmented Generation agent using local vector database
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.vector_db_path = self.config.get("vector_db_path", "./data/vector_db")
        self.chunk_size = int(self.config.get("chunk_size", 1000))
        self.chunk_overlap = int(self.config.get("chunk_overlap", 200))
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=self.config.get("embedding_model", "text-embedding-ada-002")
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
        
        # Initialize vector store
        self._load_or_create_vector_store()
        
        logger.info("RAG Agent initialized")
    
    def _load_or_create_vector_store(self):
        """Load existing vector store or create new one"""
        try:
            if os.path.exists(self.vector_db_path):
                self.vector_store = FAISS.load_local(
                    self.vector_db_path, 
                    self.embeddings
                )
                logger.info(f"Loaded existing vector store from {self.vector_db_path}")
            else:
                # Create empty vector store
                sample_doc = Document(page_content="Sample document", metadata={"source": "init"})
                docs = self.text_splitter.split_documents([sample_doc])
                self.vector_store = FAISS.from_documents(docs, self.embeddings)
                self.vector_store.save_local(self.vector_db_path)
                logger.info(f"Created new vector store at {self.vector_db_path}")
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            raise
    
    async def search(self, query: str, max_results: int = 5) -> RAGResult:
        """
        Search the local vector database for relevant documents
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            RAGResult with response and metadata
        """
        try:
            # Perform similarity search
            docs = self.vector_store.similarity_search_with_score(
                query, 
                k=max_results
            )
            
            if not docs:
                return RAGResult(
                    response="No relevant information found in local database.",
                    sources=[],
                    confidence=0.0,
                    retrieved_docs=[]
                )
            
            # Calculate confidence based on similarity scores
            avg_score = sum(score for _, score in docs) / len(docs)
            confidence = max(0, 1 - avg_score)  # Convert distance to confidence
            
            # Extract documents and create sources
            retrieved_docs = [doc for doc, _ in docs]
            sources = [
                {
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata,
                    "score": score
                }
                for doc, score in docs
            ]
            
            # Generate response from retrieved documents
            response = self._generate_response(query, retrieved_docs)
            
            return RAGResult(
                response=response,
                sources=sources,
                confidence=confidence,
                retrieved_docs=retrieved_docs
            )
            
        except Exception as e:
            logger.error(f"Error in RAG search: {e}")
            return RAGResult(
                response=f"Error searching local database: {str(e)}",
                sources=[],
                confidence=0.0,
                retrieved_docs=[]
            )
    
    def _generate_response(self, query: str, docs: List[Document]) -> str:
        """Generate response from retrieved documents"""
        if not docs:
            return "No relevant information found."
        
        # Simple response generation - combine relevant chunks
        context = "\n\n".join([doc.page_content for doc in docs[:3]])
        
        # In a production system, you'd use an LLM to generate a proper response
        # For now, we'll return the most relevant chunk
        return f"Based on local documents: {docs[0].page_content[:500]}..."
    
    async def add_documents(self, document_paths: List[str]) -> None:
        """Add new documents to the vector store"""
        try:
            all_docs = []
            
            for path in document_paths:
                if path.endswith('.txt'):
                    loader = TextLoader(path)
                elif path.endswith('.pdf'):
                    loader = PyPDFLoader(path)
                else:
                    logger.warning(f"Unsupported file type: {path}")
                    continue
                
                docs = loader.load()
                split_docs = self.text_splitter.split_documents(docs)
                all_docs.extend(split_docs)
            
            if all_docs:
                # Add to existing vector store
                self.vector_store.add_documents(all_docs)
                self.vector_store.save_local(self.vector_db_path)
                logger.info(f"Added {len(all_docs)} document chunks to vector store")
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise
    
    async def update_vector_store(self) -> None:
        """Refresh the vector store"""
        # Reload the vector store
        self._load_or_create_vector_store()
        logger.info("Vector store refreshed")
    
    def is_healthy(self) -> bool:
        """Check if RAG agent is healthy"""
        try:
            # Simple health check - try to perform a search
            test_docs = self.vector_store.similarity_search("test", k=1)
            return True
        except Exception:
            return False