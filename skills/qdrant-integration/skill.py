"""
Qdrant Integration Skill
=========================
Set up and manage Qdrant vector database for RAG applications

This skill provides complete Qdrant integration including collection
management, vector upload, and semantic search.

Matrix-Style Loading: ✓
Self-Contained: ✓
Importable: ✓
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import hashlib
import json


class QdrantIntegration:
    """
    Qdrant Integration Skill
    
    Capabilities:
    - Create and configure collections
    - Upload vectors with metadata
    - Semantic search with filters
    - Batch operations
    - Collection management
    
    Note: This is a simulation. In production, use qdrant-client library.
    """
    
    def __init__(
        self,
        url: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        self.url = url
        self.api_key = api_key
        self.skill_name = "Qdrant Integration"
        self.version = "1.0.0"
        self.collections = {}  # Simulated storage
    
    def create_collection(
        self,
        collection_name: str,
        vector_size: int = 1536,
        distance: str = "Cosine",
        on_disk: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new Qdrant collection
        
        Args:
            collection_name: Name for the collection
            vector_size: Dimension of vectors (1536 for text-embedding-3-small)
            distance: Distance metric (Cosine, Euclidean, Dot)
            on_disk: Store vectors on disk (for large collections)
            
        Returns:
            Collection configuration
        """
        config = {
            "collection_name": collection_name,
            "status": "created",
            "config": {
                "params": {
                    "vectors": {
                        "size": vector_size,
                        "distance": distance,
                        "on_disk": on_disk
                    }
                },
                "hnsw_config": {
                    "m": 16,
                    "ef_construct": 100
                },
                "optimizer_config": {
                    "indexing_threshold": 20000
                }
            },
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Store in simulated storage
        self.collections[collection_name] = {
            "config": config,
            "vectors": []
        }
        
        return config
    
    def upsert_vectors(
        self,
        collection_name: str,
        points: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Upload or update vectors in collection
        
        Args:
            collection_name: Target collection
            points: List of point dicts with id, vector, payload
            
        Returns:
            Upload result with status
            
        Example point format:
        {
            "id": "unique-id",
            "vector": [0.1, 0.2, ...],  # 1536 dimensions
            "payload": {
                "page_title": "Chapter 1",
                "page_url": "/chapter-1",
                "text": "Content text..."
            }
        }
        """
        if collection_name not in self.collections:
            return {
                "status": "error",
                "error": f"Collection '{collection_name}' not found"
            }
        
        # Validate points
        for point in points:
            if "id" not in point or "vector" not in point:
                return {
                    "status": "error",
                    "error": "Each point must have 'id' and 'vector'"
                }
        
        # Store vectors (simulated)
        collection = self.collections[collection_name]
        collection["vectors"].extend(points)
        
        return {
            "status": "completed",
            "operation_id": hashlib.md5(
                f"{collection_name}{len(points)}".encode()
            ).hexdigest(),
            "points_count": len(points),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def search(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 5,
        score_threshold: Optional[float] = None,
        payload_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors
        
        Args:
            collection_name: Collection to search
            query_vector: Query embedding vector
            limit: Number of results to return
            score_threshold: Minimum similarity score
            payload_filter: Filter by payload fields
            
        Returns:
            List of search results with scores
        """
        if collection_name not in self.collections:
            return []
        
        collection = self.collections[collection_name]
        vectors = collection["vectors"]
        
        # Simulated search (in production, Qdrant handles this)
        results = []
        for i, point in enumerate(vectors[:limit]):
            # Simulate similarity score
            score = 0.9 - (i * 0.1)
            
            if score_threshold and score < score_threshold:
                continue
            
            # Apply payload filter if provided
            if payload_filter:
                matches = all(
                    point.get("payload", {}).get(k) == v
                    for k, v in payload_filter.items()
                )
                if not matches:
                    continue
            
            results.append({
                "id": point["id"],
                "version": 0,
                "score": score,
                "payload": point.get("payload", {}),
                "vector": point.get("vector")
            })
        
        return results[:limit]
    
    def get_collection_info(
        self,
        collection_name: str
    ) -> Dict[str, Any]:
        """
        Get collection information and statistics
        
        Args:
            collection_name: Collection name
            
        Returns:
            Collection info dict
        """
        if collection_name not in self.collections:
            return {
                "status": "error",
                "error": f"Collection '{collection_name}' not found"
            }
        
        collection = self.collections[collection_name]
        vectors = collection["vectors"]
        
        return {
            "status": "ok",
            "result": {
                "vectors_count": len(vectors),
                "indexed_vectors_count": len(vectors),
                "points_count": len(vectors),
                "segments_count": 1,
                "config": collection["config"]["config"]
            }
        }
    
    def delete_collection(
        self,
        collection_name: str
    ) -> Dict[str, Any]:
        """
        Delete a collection
        
        Args:
            collection_name: Collection to delete
            
        Returns:
            Deletion result
        """
        if collection_name in self.collections:
            del self.collections[collection_name]
            return {
                "status": "ok",
                "result": True,
                "time": 0.001
            }
        else:
            return {
                "status": "error",
                "error": f"Collection '{collection_name}' not found"
            }
    
    def create_payload_index(
        self,
        collection_name: str,
        field_name: str,
        field_type: str = "keyword"
    ) -> Dict[str, Any]:
        """
        Create index on payload field for faster filtering
        
        Args:
            collection_name: Collection name
            field_name: Payload field to index
            field_type: Field type (keyword, integer, float, etc.)
            
        Returns:
            Index creation result
        """
        return {
            "status": "ok",
            "result": {
                "operation_id": 0,
                "status": "completed"
            },
            "indexed_field": field_name,
            "field_type": field_type
        }
    
    def batch_upload(
        self,
        collection_name: str,
        points: List[Dict[str, Any]],
        batch_size: int = 100
    ) -> Dict[str, Any]:
        """
        Upload vectors in batches for large datasets
        
        Args:
            collection_name: Target collection
            points: All points to upload
            batch_size: Number of points per batch
            
        Returns:
            Batch upload summary
        """
        total_points = len(points)
        batches = [
            points[i:i + batch_size]
            for i in range(0, total_points, batch_size)
        ]
        
        results = []
        for i, batch in enumerate(batches):
            result = self.upsert_vectors(collection_name, batch)
            results.append(result)
        
        return {
            "total_points": total_points,
            "batch_count": len(batches),
            "batch_size": batch_size,
            "all_successful": all(r.get("status") == "completed" for r in results),
            "timestamp": datetime.utcnow().isoformat()
        }


# Example usage
def main():
    """Example usage of Qdrant Integration Skill"""
    print("="*60)
    print("Qdrant Integration Skill - Example Usage")
    print("="*60)
    
    # Initialize skill
    skill = QdrantIntegration(
        url="https://your-cluster.qdrant.io",
        api_key="your-api-key"
    )
    
    # Example 1: Create collection
    print("\n[Example 1] Create Collection")
    result = skill.create_collection(
        collection_name="book_chunks",
        vector_size=1536,
        distance="Cosine"
    )
    print(f"✓ Collection created: {result['collection_name']}")
    print(f"  Vector size: {result['config']['params']['vectors']['size']}")
    print(f"  Distance: {result['config']['params']['vectors']['distance']}")
    
    # Example 2: Upload vectors
    print("\n[Example 2] Upload Vectors")
    points = [
        {
            "id": "chunk_1",
            "vector": [0.1] * 1536,  # Dummy vector
            "payload": {
                "page_title": "Introduction to RAG",
                "page_url": "/intro",
                "section": "What is RAG?",
                "text": "RAG combines retrieval with generation..."
            }
        },
        {
            "id": "chunk_2",
            "vector": [0.2] * 1536,
            "payload": {
                "page_title": "Core Concepts",
                "page_url": "/chapter-1",
                "section": "Embeddings",
                "text": "Embeddings are vector representations..."
            }
        }
    ]
    
    result = skill.upsert_vectors("book_chunks", points)
    print(f"✓ Uploaded {result['points_count']} vectors")
    print(f"  Operation ID: {result['operation_id']}")
    
    # Example 3: Search
    print("\n[Example 3] Search Similar Vectors")
    query_vector = [0.15] * 1536  # Dummy query vector
    results = skill.search(
        collection_name="book_chunks",
        query_vector=query_vector,
        limit=2
    )
    print(f"✓ Found {len(results)} results")
    for i, result in enumerate(results):
        print(f"  {i+1}. {result['payload']['page_title']} (score: {result['score']:.3f})")
    
    # Example 4: Collection info
    print("\n[Example 4] Get Collection Info")
    info = skill.get_collection_info("book_chunks")
    print(f"✓ Collection status: {info['status']}")
    print(f"  Vectors count: {info['result']['vectors_count']}")
    
    # Example 5: Batch upload
    print("\n[Example 5] Batch Upload (Simulated)")
    large_batch = [
        {
            "id": f"chunk_{i}",
            "vector": [0.1 * i] * 1536,
            "payload": {"text": f"Content {i}"}
        }
        for i in range(250)
    ]
    result = skill.batch_upload("book_chunks", large_batch, batch_size=100)
    print(f"✓ Batch upload complete")
    print(f"  Total points: {result['total_points']}")
    print(f"  Batches: {result['batch_count']}")
    print(f"  All successful: {result['all_successful']}")
    
    print("\n" + "="*60)
    print("Skill demonstration complete")
    print("="*60)


if __name__ == "__main__":
    main()
