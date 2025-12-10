---
id: tools-libraries
title: Tools & Libraries
sidebar_position: 2
---

# Tools & Libraries

Essential tools and libraries for building RAG systems.

## Vector Databases

- **Qdrant**: Fast, Python-friendly, free tier
- **Pinecone**: Managed, enterprise-ready  
- **Weaviate**: GraphQL API, rich features
- **Chroma**: Embedded, great for prototyping

## Embedding Models

- **OpenAI text-embedding-3-small**: Best cost/performance
- **Cohere embed-v3**: Multilingual support
- **Sentence Transformers**: Open-source, free

## LLM Providers

- **OpenAI**: GPT-4, GPT-4o-mini
- **Anthropic**: Claude 3
- **Google**: Gemini Pro
- **Open Source**: Llama 2, Mistral

## Frameworks

### LangChain
```python
from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA

vectorstore = Qdrant(...)
qa_chain = RetrievalQA.from_chain_type(llm=..., retriever=vectorstore.as_retriever())
```

### LlamaIndex
```python
from llama_index import VectorStoreIndex, ServiceContext

index = VectorStoreIndex.from_documents(docs)
query_engine = index.as_query_engine()
response = query_engine.query("What is RAG?")
```

## Development Tools

- **Cursor/VS Code**: IDE with AI features
- **Postman**: API testing
- **Docker**: Containerization
- **Git**: Version control

Next: [Best Practices](best-practices)
