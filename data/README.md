# Data Directory

This directory stores vector database cache and chunked content.

## Structure

```
data/
├── embeddings/    # Cached embedding vectors
└── chunks/        # Processed text chunks
```

## Usage

- **embeddings/**: Stores generated embeddings to avoid re-computation
- **chunks/**: Contains chunked text from book pages with metadata

## Status

**Phase 0**: ✅ Directory structure created  
**Phase 2**: ⏳ Will be populated during indexing process

## Note

These files are cached locally but **not** stored in the version control system (see `.gitignore`). The source of truth is always the Qdrant Cloud database.
