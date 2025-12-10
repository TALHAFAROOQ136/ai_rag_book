---
id: vector-embeddings
title: Vector Embeddings
sidebar_position: 1
---

# Vector Embeddings

Vector embeddings are the mathematical foundation that makes RAG possible. Let's understand what they are and why they're crucial.

## What Are Embeddings?

**Embeddings** are numerical representations of text that capture semantic meaning in a multi-dimensional space.

### Simple Analogy

Think of embeddings like GPS coordinates:
- "Paris, France" → `[48.8566, 2.3522]` (latitude, longitude)
- Similar locations have similar coordinates
- Distance between coordinates = geographic proximity

**Text embeddings work similarly**:
- "Dog" → `[0.21, 0.85, -0.43, ...]` (1536 dimensions)
- Similar meanings have similar vectors
- Distance between vectors = semantic similarity

## How Embeddings Work

```python
from openai import OpenAI
client = OpenAI()

# Generate embedding
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Retrieval-Augmented Generation"
)

embedding = response.data[0].embedding
print(f"Vector dimensions: {len(embedding)}")  # 1536
print(f"First 5 values: {embedding[:5]}")
# [0.123, -0.456, 0.789, ...]
```

## Why Embeddings Matter for RAG

### Traditional Keyword Search vs. Semantic Search

**Keyword Search** (old way):
- User: "How do I fix a broken pipe?"
- Matches: Documents with exact words "fix", "broken", "pipe"
- Misses: Documents about "repairing leaks" or "plumbing repairs"

**Semantic Search** (with embeddings):
- Understands "fix" ≈ "repair" ≈ "fix"
- Knows "pipe" relates to "plumbing", "water system"
- Finds relevant docs even with different wording

### Similarity Example

```python
# These have high similarity (close vectors)
"artificial intelligence" ↔ "machine learning"  # 0.85
"dog" ↔ "puppy"  # 0.90

# These have low similarity (distant vectors)
"dog" ↔ "mathematics"  # 0.12
```

## Embedding Models

### Popular Options

| Model | Dimensions | Performance | Cost |
|-------|-----------|-------------|------|
| **text-embedding-3-small** | 1536 | Good | $ |
| **text-embedding-3-large** | 3072 | Better | $$ |
| **Cohere embed-v3** | 1024 | Good | $ |
| **Sentence-BERT** | 384-768 | OK | Free |

### Choosing a Model

**Use text-embedding-3-small when**:
- Starting a new project
- Cost-conscious
- English-only content

**Use text-embedding-3-large when**:
- Need highest accuracy
- Multilingual content
- Complex domain-specific content

## Creating Embeddings

### Single Text

```python
def create_embedding(text: str) -> list[float]:
    """Create embedding for a single text"""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# Example
query_vector = create_embedding("What is machine learning?")
```

### Batch Processing

```python
def create_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Create embeddings for multiple texts (more efficient)"""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts  # Pass list directly
    )
    return [item.embedding for item in response.data]

# Example - process 100 documents at once
docs = ["doc 1 text", "doc 2 text", ...]
vectors = create_embeddings_batch(docs)
```

:::tip Batching Saves Money
OpenAI charges per token. Batching reduces API overhead and can process up to 2048 texts in one call!
:::

## Understanding Vector Dimensions

### What Does Each Dimension Represent?

Each dimension captures different semantic aspects:
- Dimension 1: Might capture "formality" (informal ← → formal)
- Dimension 2: Might capture "sentiment" (negative ← → positive)
- Dimension 1536: Captures some other semantic feature

**Important**: We don't know exactly what each dimension means—the model learned these representations during training!

### Visualization (Simplified)

Real embeddings have 1536 dimensions, but imagine 2D:

```
     Technical
        ↑
        |  • "neural networks"
        |    • "algorithms"
        |
 -------+------- → Business
        |
        | • "marketing"
        |   • "sales"
        ↓
    Non-technical
```

## Calculating Similarity

### Cosine Similarity

Most common method for measuring similarity:

```python
import numpy as np

def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot_product = np.dot(vec1, vec2)
    magnitude = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    
    return dot_product / magnitude

# Example
query = create_embedding("machine learning")
doc1 = create_embedding("artificial intelligence and ML")
doc2 = create_embedding("cooking recipes")

print(cosine_similarity(query, doc1))  # 0.85 (very similar)
print(cosine_similarity(query, doc2))  # 0.15 (not similar)
```

### Other Distance Metrics

- **Euclidean Distance**: Straight-line distance
- **Dot Product**: Simple multiplication
- **Manhattan Distance**: Grid-based distance

:::info Qdrant Default
Qdrant uses **Cosine similarity** by default, which normalizes vectors and works well for most text applications.
:::

## Practical Tips

### 1. Chunk Size Matters

```python
# Too small - lacks context
chunk1 = "RAG"
embedding1 = create_embedding(chunk1)

# Too large - diluted meaning
chunk2 = "RAG is..." * 1000  # 5000 words
embedding2 = create_embedding(chunk2)

# Just right - meaningful context
chunk3 = "RAG combines retrieval and generation..."  # 200-500 words
embedding3 = create_embedding(chunk3)
```

**Recommendation**: 200-800 words per chunk

### 2. Consistent Model

Always use the **same model** for:
- Creating document embeddings
- Creating query embeddings

Mixing models won't work!

### 3. Embedding Metadata

Store important metadata alongside embeddings:

```python
{
    "id": "doc_123",
    "vector": [0.1, 0.2, ...],  # The embedding
    "payload": {
        "text": "Original text content",
        "title": "Document title",
        "source": "documentation.pdf",
        "created_at": "2024-01-15"
    }
}
```

## Cost Optimization

### Token Counting

```python
import tiktoken

def count_tokens(text: str, model: str = "text-embedding-3-small") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Example
text = "Your document text here"
tokens = count_tokens(text)
cost = tokens * 0.00002 / 1000  # $0.02 per 1M tokens
print(f"Cost: ${cost:.6f}")
```

### Caching Strategy

```python
import hashlib
import json

def get_cached_embedding(text: str, cache_dir: str = "./embeddings_cache"):
    """Cache embeddings to avoid recomputing"""
    text_hash = hashlib.md5(text.encode()).hexdigest()
    cache_file = f"{cache_dir}/{text_hash}.json"
    
    # Try cache first
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            return json.load(f)["embedding"]
    
    # Generate if not cached
    embedding = create_embedding(text)
    
    # Save to cache
    with open(cache_file, 'w') as f:
        json.dump({"text": text, "embedding": embedding}, f)
    
    return embedding
```

## Summary

Embeddings are:
- **Numerical vectors** that represent text semantically
- **Foundation of RAG** for finding relevant documents
- **Created by AI models** trained on vast text corpora
- **Comparable using similarity metrics** like cosine similarity

Next, we'll learn how to use these embeddings for [similarity search](similarity-search)!
