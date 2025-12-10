---
id: optimization
title: Optimization
sidebar_position: 1
---

# Optimization

Techniques to make your RAG system faster, cheaper, and more accurate.

## Speed Optimization

### 1. Reduce Retrieval Latency
- Use faster vector DB with HNSW indexing
- Limit search results (top 3-5 instead of 10)
- Use smaller embedding models when possible

### 2. Parallel Processing
```python
import asyncio

async def parallel_rag(questions: list[str]):
    tasks = [rag_query_async(q) for q in questions]
    return await asyncio.gather(*tasks)
```

### 3. Caching
Cache frequent queries:
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_embedding(text: str):
    return create_embedding(text)
```

## Cost Optimization

### Use Smaller Models
- GPT-4o-mini: 10x cheaper than GPT-4
- text-embedding-3-small: 5x cheaper than large

### Reduce Token Usage
- Truncate context intelligently
- Use RAG for factual Q&A, not creative tasks
- Cache embeddings (generate once, use many times)

## Accuracy Optimization

### Re-ranking
Add a re-ranking step after initial retrieval:

```python
def rerank_results(query, results):
    """Use cross-encoder for better accuracy"""
    from sentence_transformers import CrossEncoder
    
    model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    scores = model.predict([(query, r.payload['text']) for r in results])
    
    # Sort by new scores
    return sorted(zip(results, scores), key=lambda x: x[1], reverse=True)
```

### Hybrid Search
Combine vector + keyword search for better recall.

### Query Expansion
Generate multiple versions of the query for better coverage.

## Scalability

### Horizontal Scaling
- Deploy multiple API instances
- Load balance requests
- Use managed vector DB (auto-scaling)

### Vertical Scaling
- More RAM for larger indexes
- Faster CPUs for embedding generation
- GPUs for local embedding models

## Summary

Optimize your RAG system by:
- **Speed**: Caching, parallelization, limiting results
- **Cost**: Smaller models, token reduction, embedding caching
- **Accuracy**: Re-ranking, hybrid search, query expansion
- **Scale**: Horizontal/vertical scaling, managed services

Next: [Real-World Applications](applications)
