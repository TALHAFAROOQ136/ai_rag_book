---
id: similarity-search
title: Similarity Search
sidebar_position: 2
---

# Similarity Search

Once you have embeddings, you need to find the most similar ones quickly. This is where vector databases and similarity search shine.

## The Challenge

Imagine searching through 1 million document embeddings:
- Each embedding: 1536 dimensions
- Brute force: Compare query to ALL 1M documents
- **Problem**: Too slow for real-time applications!

## Solution: Vector Databases

Vector databases use smart algorithms (like HNSW) to find similar vectors in milliseconds instead of seconds.

### Popular Vector Databases

| Database | Highlights | Best For |
|----------|-----------|----------|
| **Qdrant** | Fast, free tier, easy | Learning & production |
| **Pinecone** | Managed, scalable | Enterprise |
| **Weaviate** | Feature-rich | Complex queries |
| **Chroma** | Simple, embedded | Prototyping |

## Qdrant Setup

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Connect to Qdrant Cloud
client = QdrantClient(
    url="https://your-cluster.qdrant.io",
    api_key="your-api-key"
)

# Create collection
client.create_collection(
    collection_name="knowledge_base",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)
```

## Indexing Documents

```python
# Prepare documents with embeddings
points = [
    {
        "id": 1,
        "vector": create_embedding("RAG combines retrieval and generation..."),
        "payload": {
            "text": "RAG combines retrieval and generation...",
            "title": "What is RAG?",
            "chapter": 1
        }
    },
    # ... more documents
]

# Upload to Qdrant
client.upsert(
    collection_name="knowledge_base",
    points=points
)
```

## Performing Search

```python
# User query
query = "How does RAG work?"
query_vector = create_embedding(query)

# Search for similar documents
results = client.search(
    collection_name="knowledge_base",
    query_vector=query_vector,
    limit=5,  # Top 5 results
    score_threshold=0.7  # Minimum similarity
)

# Use results
for result in results:
    print(f"Score: {result.score}")
    print(f"Text: {result.payload['text']}")
```

## Advanced Filtering

```python
# Search only in specific chapter
results = client.search(
    collection_name="knowledge_base",
    query_vector=query_vector,
    query_filter={
        "must": [
            {"key": "chapter", "match": {"value": 2}}
        ]
    },
    limit=3
)
```

## Summary

Similarity search enables:
- **Fast retrieval** from millions of documents
- **Semantic matching** beyond keywords
- **Flexible filtering** with metadata

Next: [Context Augmentation](context-augmentation)
