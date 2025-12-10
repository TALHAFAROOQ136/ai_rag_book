"""
Admin API Routes - Indexing and Management
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
from pathlib import Path
import os

from app.services.rag_service import RAGService
from app.models.chat import ReindexRequest, ReindexResponse

router = APIRouter()

# Initialize RAG service
rag_service = RAGService()


@router.post("/reindex", response_model=ReindexResponse)
async def reindex_content(
    request: ReindexRequest,
    background_tasks: BackgroundTasks
):
    """
    Re-index book content into vector database
    
    This endpoint:
    1. Reads all markdown files from the book directory
    2. Chunks the content
    3. Creates embeddings
    4. Stores in Qdrant
    
    Can be run in background for large content sets
    """
    try:
        # Get book docs directory
        book_docs_path = request.docs_path or Path("../book/docs")
        
        if not os.path.exists(book_docs_path):
            raise HTTPException(
                status_code=404,
                detail=f"Documentation path not found: {book_docs_path}"
            )
        
        # Function to perform indexing
        def perform_indexing():
            total_chunks = 0
            indexed_files = []
            
            # Recursively find all markdown files
            for md_file in Path(book_docs_path).rglob("*.md"):
                try:
                    # Read file
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract metadata from frontmatter if exists
                    title = md_file.stem.replace('-', ' ').title()
                    url_path = str(md_file.relative_to(book_docs_path)).replace('\\', '/').replace('.md', '')
                    
                    # Determine chapter from path
                    parts = md_file.parts
                    chapter = "Introduction"
                    for part in parts:
                        if "chapter" in part.lower():
                            chapter = part.replace('-', ' ').title()
                            break
                    
                    # Index the document
                    doc_id = md_file.stem
                    chunks_indexed = rag_service.index_document(
                        doc_id=doc_id,
                        title=title,
                        content=content,
                        url=f"/{url_path}",
                        chapter=chapter
                    )
                    
                    total_chunks += chunks_indexed
                    indexed_files.append({
                        "file": str(md_file.name),
                        "chunks": chunks_indexed
                    })
                    
                except Exception as e:
                    print(f"Error indexing {md_file}: {e}")
                    continue
            
            return total_chunks, indexed_files
        
        # Run indexing
        if request.background:
            background_tasks.add_task(perform_indexing)
            return ReindexResponse(
                status="started",
                message="Indexing started in background",
                indexed_count=0,
                failed_count=0
            )
        else:
            total_chunks, indexed_files = perform_indexing()
            return ReindexResponse(
                status="completed",
                message=f"Successfully indexed {len(indexed_files)} files with {total_chunks} chunks",
                indexed_count=len(indexed_files),
                failed_count=0,
                details=indexed_files
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during re-indexing: {str(e)}"
        )


@router.get("/collection/stats")
async def get_collection_stats():
    """
    Get vector database collection statistics
    
    Returns:
        Information about indexed documents and vectors
    """
    try:
        stats = rag_service.get_collection_stats()
        return {
            "status": "success",
            "data": stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching stats: {str(e)}"
        )


@router.delete("/collection")
async def clear_collection():
    """
    Clear all vectors from the collection
    
    WARNING: This deletes all indexed content!
    """
    try:
        # Recreate collection (effectively clearing it)
        rag_service.qdrant.delete_collection(rag_service.collection_name)
        rag_service.ensure_collection_exists()
        
        return {
            "status": "success",
            "message": "Collection cleared successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing collection: {str(e)}"
        )
