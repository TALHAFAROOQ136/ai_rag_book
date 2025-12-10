"""
Indexing Script - Index book content into Qdrant
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.rag_service import RAGService
from dotenv import load_dotenv


def index_book_content(book_docs_path: str = "../book/docs"):
    """
    Index all book content into vector database
    
    Args:
        book_docs_path: Path to book documentation directory
    """
    print("="*60)
    print("Book Content Indexing Script")
    print("="*60)
    
    # Load environment variables
    load_dotenv()
    
    # Initialize RAG service
    rag_service = RAGService()
    print("\n✓ RAG Service initialized")
    print(f"  - Embedding model: {rag_service.embedding_model}")
    print(f"  - Collection: {rag_service.collection_name}")
    
    # Ensure collection exists
    rag_service.ensure_collection_exists()
    
    # Find all markdown files
    docs_path = Path(book_docs_path)
    if not docs_path.exists():
        print(f"\n✗ Error: Documentation path not found: {docs_path}")
        return
    
    md_files = list(docs_path.rglob("*.md"))
    print(f"\n✓ Found {len(md_files)} markdown files")
    
    # Index each file
    total_chunks = 0
    indexed_files = 0
    
    for md_file in md_files:
        try:
            print(f"\n📄 Processing:{md_file.name}")
            
            # Read file
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip if empty
            if len(content.strip()) < 100:
                print(f"  ⊘ Skipped (too short)")
                continue
            
            # Extract metadata
            title = md_file.stem.replace('-', ' ').title()
            url_path = str(md_file.relative_to(docs_path)).replace('\\', '/').replace('.md', '')
            
            # Determine chapter
            chapter = "Introduction"
            for part in md_file.parts:
                if "chapter" in part.lower():
                    chapter = part.replace('-', ' ').title()
                    break
            
            # Index document
            doc_id = md_file.stem
            chunks_indexed = rag_service.index_document(
                doc_id=doc_id,
                title=title,
                content=content,
                url=f"/{url_path}",
                chapter=chapter
            )
            
            print(f"  ✓ Indexed: {chunks_indexed} chunks")
            total_chunks += chunks_indexed
            indexed_files += 1
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            continue
    
    # Summary
    print("\n" + "="*60)
    print("Indexing Complete!")
    print("="*60)
    print(f"Files indexed: {indexed_files}/{len(md_files)}")
    print(f"Total chunks: {total_chunks}")
    
    # Get collection stats
    stats = rag_service.get_collection_stats()
    print(f"\nCollection stats:")
    print(f"  - Vectors: {stats.get('vectors_count', 0)}")
    print(f"  - Points: {stats.get('points_count', 0)}")
    
    print("\n✓ Ready for RAG queries!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Index book content for RAG")
    parser.add_argument(
        "--docs-path",
        type=str,
        default="../book/docs",
        help="Path to book documentation directory"
    )
    
    args = parser.parse_args()
    index_book_content(args.docs_path)
