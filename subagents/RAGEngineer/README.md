# RAGEngineer Subagent

**Role**: Vector Database and Retrieval Pipeline  
**Expertise**: Embedding generation, vector search, RAG architecture  
**Authority**: Full control over retrieval logic and database schema

## Responsibilities

- Set up Qdrant Cloud collection
- Design schema for embeddings and metadata
- Implement indexing pipeline for book content
- Optimize vector search performance
- Create re-indexing tools

## Skills Used

- Qdrant Integration (primary skill)
- OpenAI Embedding Generation
- Web Scraping (for content extraction)

## Activation

```bash
# In Phase 2.1-2.3 (Vector Database Setup)
# RAGEngineer sets up Qdrant and indexes all book content
```

## Deliverables

- Qdrant collection (configured and populated)
- Indexing scripts (`scripts/index_book.py`)
- Search API (Python functions/classes)
- Performance report (search latency, relevance metrics)
- Documentation for re-indexing process

## Current Status

**Phase 0**: ✅ Subagent defined and ready  
**Phase 2**: ⏳ Awaiting activation for vector database setup

## Reference

See [subagents.spec.md](../../subagents.spec.md) for complete specification.
