---
id: context-augmentation
title: Context Augmentation
sidebar_position: 3
---

# Context Augmentation

Context augmentation is the "A" in RAG—combining retrieved documents with user queries to create enhanced prompts.

## The Augmentation Process

### 1. Retrieve Documents

```python
results = vector_db.search(query_vector, limit=3)
```

### 2. Format Context

```python
context = "\n\n".join([
    f"**Source {i+1}**: {r.payload['title']}\n{r.payload['text']}"
    for i, r in enumerate(results)
])
```

### 3. Create Augmented Prompt

```python
prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {user_question}

Answer based only on the context above."""
```

## Prompt Engineering for RAG

### Effective System Prompts

```python
SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on provided context.

Rules:
1. Only use information from the context
2. Cite sources in your answer
3. If unsure, say "I don't have enough information"
4. Be concise but thorough"""
```

### Temperature Settings

- **Low (0.0-0.3)**: Factual Q&A (recommended for RAG)
- **Medium (0.4-0.7)**: Creative but grounded
- **High (0.8-1.0)**: Not recommended for RAG

## Context Window Management

### Token Limits

Different models have different context windows:
- **GPT-4o-mini**: 128K tokens (~96K words)
- **GPT-4**: 8K-32K tokens
- **Claude 3**: 200K tokens

### Fit More Context

```python
def truncate_context(results, max_tokens=4000):
    """Ensure context fits within token limit"""
    context_parts = []
    total_tokens = 0
    
    for result in results:
        text = result.payload['text']
        tokens = count_tokens(text)
        
        if total_tokens + tokens < max_tokens:
            context_parts.append(text)
            total_tokens += tokens
        else:
            break
    
    return "\n\n".join(context_parts)
```

## Summary

Context augmentation:
- **Combines** retrieved documents with queries
- **Provides** LLMs with relevant facts
- **Manages** token limits effectively

Next chapter: [Building the Pipeline](../chapter-3/building-pipeline)
