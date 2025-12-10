"""
RAG Service - Vector Search and Context Retrieval
"""

from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from openai import OpenAI
import os
from datetime import datetime


class RAGService:
    """
    RAG Service for vector search and context retrieval
    
    Uses:
    - Qdrant for vector storage and similarity search
    - OpenAI for embeddings generation
    """
    
    def __init__(self):
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Initialize Qdrant client
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_key = os.getenv("QDRANT_API_KEY")
        
        if qdrant_url and qdrant_key:
            self.qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_key)
        else:
            # Fallback to in-memory for development
            self.qdrant = QdrantClient(":memory:")
        
        self.collection_name = "book_chunks"
        self.embedding_model = "text-embedding-3-small"
        self.embedding_dimension = 1536
        
    def ensure_collection_exists(self):
        """Create collection if it doesn't exist"""
        try:
            self.qdrant.get_collection(self.collection_name)
        except Exception:
            # Collection doesn't exist, create it
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_dimension,
                    distance=Distance.COSINE
                )
            )
            print(f"✓ Created collection: {self.collection_name}")
    
    def create_embedding(self, text: str) -> List[float]:
        """
        Create embedding for text using OpenAI
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk in words
            overlap: Overlap between chunks in words
            
        Returns:
            List of text chunks
        """
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if len(chunk.strip()) > 0:
                chunks.append(chunk)
        
        return chunks
    
    def index_document(
        self,
        doc_id: str,
        title: str,
        content: str,
        url: str,
        chapter: Optional[str] = None
    ) -> int:
        """
        Index a document by chunking and creating embeddings
        
        Args:
            doc_id: Unique document ID
            title: Document title
            content: Full document content
            url: Document URL
            chapter: Optional chapter/section
            
        Returns:
            Number of chunks indexed
        """
        self.ensure_collection_exists()
        
        # Chunk the content
        chunks = self.chunk_text(content)
        
        # Create points for Qdrant
        points = []
        for i, chunk in enumerate(chunks):
            # Create embedding
            embedding = self.create_embedding(chunk)
            
            # Create point
            point = PointStruct(
                id=f"{doc_id}_chunk_{i}",
                vector=embedding,
                payload={
                    "text": chunk,
                    "doc_id": doc_id,
                    "title": title,
                    "url": url,
                    "chapter": chapter or "Main",
                    "chunk_index": i,
                    "indexed_at": datetime.utcnow().isoformat()
                }
            )
            points.append(point)
        
        # Upload to Qdrant
        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        return len(chunks)
    
    def search_similar(
        self,
        query: str,
        limit: int = 5,
        score_threshold: float = 0.5,
        chapter_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar chunks
        
        Args:
            query: Search query
            limit: Maximum number of results
            score_threshold: Minimum similarity score
            chapter_filter: Optional filter by chapter
            
        Returns:
            List of search results with text and metadata
        """
        self.ensure_collection_exists()
        
        # Create query embedding
        query_embedding = self.create_embedding(query)
        
        # Build filter if needed
        search_filter = None
        if chapter_filter:
            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="chapter",
                        match=MatchValue(value=chapter_filter)
                    )
                ]
            )
        
        # Search
        results = self.qdrant.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
            score_threshold=score_threshold,
            query_filter=search_filter
        )
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "text": result.payload["text"],
                "title": result.payload["title"],
                "url": result.payload["url"],
                "chapter": result.payload["chapter"],
                "score": result.score,
                "chunk_index": result.payload.get("chunk_index", 0)
            })
        
        return formatted_results
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            collection_info = self.qdrant.get_collection(self.collection_name)
            return {
                "collection_name": self.collection_name,
                "vectors_count": collection_info.vectors_count,
                "indexed_vectors_count": collection_info.indexed_vectors_count,
                "points_count": collection_info.points_count
            }
        except Exception as e:
            return {
                "collection_name": self.collection_name,
                "error": str(e),
                "vectors_count": 0
            }
