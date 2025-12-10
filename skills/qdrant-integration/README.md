# Qdrant Integration Skill

**Version**: 1.0.0  
**Category**: Backend / AI / Database  
**Reusability**: High (works with any vector search project)

## Purpose

Set up and manage Qdrant vector database for RAG applications, including collection creation, vector upload, and search functions.

## Inputs

- `qdrant_url`: Qdrant cluster URL
- `api_key`: Qdrant API key
- `collection_name`: Name for vector collection
- `vector_size`: Embedding dimensions (default: 1536)
- `distance_metric`: Distance metric (Cosine/Euclidean/Dot)

## Outputs

- Qdrant collection (created and configured)
- Python client code for interaction
- Search functions (similarity search, metadata filtering)
- Indexing utilities (add vectors, batch upload)
- Performance metrics

## Usage

See [skills.spec.md](../../skills.spec.md#skill-2-qdrant-integration) for complete implementation with code examples.

## Status

**Phase 0**: ✅ Skill defined and documented  
**Phase 2**: ⏳ Ready for use by RAGEngineer subagent
