---
id: building-pipeline
title: Building the Pipeline
sidebar_position: 1
---

# Building the RAG Pipeline

Now let's build a complete, production-ready RAG system end-to-end.

## Architecture Overview

```
┌─────────────────┐
│  Document Load  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Text Chunking  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Embed & Index │──► Vector DB
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┏━━━━━━━━━━━━━┓
│  Query Handler  │──────► LLM (GPT-4) │
└─────────────────┘      ┗━━━━━━━━━━━━━┛
```

## Step 1: Document Processing

```python
def load_documents(directory: str) -> list[str]:
    """Load all documents from directory"""
    documents = []
    for file in Path(directory).glob("*.md"):
        with open(file) as f:
            documents.append(f.read())
    return documents

def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - 100):  # 100 word overlap
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks
```

## Step 2: Create Embeddings & Index

```python
from openai import OpenAI
from qdrant_client import QdrantClient

client_llm = OpenAI()
client_db = QdrantClient(url="...", api_key="...")

def index_documents(documents: list[str]):
    """Process and index all documents"""
    points = []
    
    for doc_id, doc in enumerate(documents):
        chunks = chunk_text(doc)
        
        for chunk_id, chunk in enumerate(chunks):
            # Create embedding
            embedding = client_llm.embeddings.create(
                model="text-embedding-3-small",
                input=chunk
            ).data[0].embedding
            
            # Create point
            points.append({
                "id": f"{doc_id}_{chunk_id}",
                "vector": embedding,
                "payload": {
                    "text": chunk,
                    "doc_id": doc_id,
                    "chunk_id": chunk_id
                }
            })
    
    # Batch upload
    client_db.upsert(collection_name="knowledge_base", points=points)
    print(f"Indexed {len(points)} chunks")
```

## Step 3: Query Pipeline

```python
def rag_query(question: str) -> str:
    """Complete RAG query pipeline"""
    
    # 1. Create query embedding
    query_embedding = client_llm.embeddings.create(
        model="text-embedding-3-small",
        input=question
    ).data[0].embedding
    
    # 2. Search vector database
    results = client_db.search(
        collection_name="knowledge_base",
        query_vector=query_embedding,
        limit=5
    )
    
    # 3. Format context
    context = "\n\n---\n\n".join([
        f"**Source {i+1}**:\n{r.payload['text']}"
        for i, r in enumerate(results)
    ])
    
    # 4. Create prompt
    messages = [
        {"role": "system", "content": "Answer based only on the context."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]
    
    # 5. Generate response
    response = client_llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3
    )
    
    return response.choices[0].message.content
```

## Step 4: Testing

```python
# Index documents
docs = load_documents("./docs")
index_documents(docs)

# Query
answer = rag_query("What is RAG?")
print(answer)
```

## Complete Example

See the full working code on [GitHub](https://github.com/example/rag-example).

Next: [Tools & Libraries](tools-libraries)
