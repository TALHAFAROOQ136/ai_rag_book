---
id: best-practices
title: Best Practices
sidebar_position: 3
---

# Best Practices

Proven strategies for building effective RAG systems.

## Chunking Strategies

### Optimal Chunk Size
- **Too small** (< 100 words): Lacks context
- **Too large** (> 1000 words): Diluted meaning
- **Sweet spot**: 200-500 words

### Overlap
Use 10-20% overlap between chunks to avoid losing context at boundaries.

```python
def chunk_with_overlap(text, size=500, overlap=100):
    words = text.split()
    for i in range(0, len(words), size - overlap):
        yield " ".join(words[i:i + size])
```

## Query Optimization

### Reformulation
Expand user queries for better retrieval:

```python
def expand_query(query: str) -> str:
    """Use LLM to generate alternative phrasings"""
    prompt = f"Rephrase this question 3 different ways: {query}"
    # ... LLM call
    return expanded_queries
```

### Hybrid Search
Combine semantic + keyword search for better accuracy:
- Vector search: 70% weight
- BM25 keyword: 30% weight

## Response Quality

### Add Citations
Always cite sources in responses:

```python
response = f"""{answer}

**Sources:**
- {source1_title} (relevance: {score1:.2f})
- {source2_title} (relevance: {score2:.2f})
"""
```

### Confidence Scores
Return confidence with answers:

```python
if max_similarity_score < 0.7:
    return "I don't have enough information to answer confidently."
```

## Performance Optimization

### Caching
- Cache embeddings (expensive to generate)
- Cache common queries
- Use Redis for production

### Batch Processing
Process multiple queries/documents together:

```python
# Good - batched
embeddings = create_embeddings_batch(texts)  # 1 API call

# Bad - sequential  
embeddings = [create_embedding(t) for t in texts]  # N API calls
```

## Monitoring

Track these metrics:
- **Retrieval accuracy**: Are top results relevant?
- **Response latency**: < 2 seconds ideal
- **Cost per query**: Monitor API usage
- **User feedback**: Thumbs up/down

## Security

### API Key Management
```python
# Good
api_key = os.getenv("OPENAI_API_KEY")

# Bad - hardcoded!
api_key = "sk-..."
```

### Input Validation
Sanitize user inputs to prevent injection attacks.

## Summary

Follow these practices for production RAG:
- Optimal chunking (200-500 words, 10-20% overlap)
- Always cite sources
- Cache expensive operations
- Monitor performance metrics
- Secure API keys

Next chapter: [Optimization](../chapter-4/optimization)
