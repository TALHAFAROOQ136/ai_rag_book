"""
Chat API Routes - RAG Q&A Endpoints
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any
import json

from app.models.chat import ChatRequest, ChatResponse, Source, StreamToken, StreamSources, StreamDone
from app.services.rag_service import RAGService
from app.services.agent_service import AgentService

router = APIRouter()

# Initialize services
rag_service = RAGService()
agent_service = AgentService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    RAG-powered Q&A endpoint (non-streaming)
    
    Process:
    1. Search for relevant chunks in vector database
    2. Create RAG prompt with context
    3. Generate response using OpenAI
    4. Return answer with sources
    """
    try:
        # Step 1: Search for relevant context
        context_chunks = rag_service.search_similar(
            query=request.question,
            limit=request.top_k,
            chapter_filter=request.chapter_filter
        )
        
        if not context_chunks:
            raise HTTPException(
                status_code=404,
                detail="No relevant content found. The book may not be indexed yet."
            )
        
        # Step 2 & 3: Generate response with OpenAI
        result = agent_service.generate_response_with_metadata(
            question=request.question,
            context_chunks=context_chunks
        )
        
        # Step 4: Format response
        sources = [
            Source(
                page_title=src["title"],
                page_url=src["url"],
                section=src["chapter"],
                relevance_score=src["relevance_score"]
            )
            for src in result["sources"]
        ]
        
        return ChatResponse(
            answer=result["answer"],
            sources=sources
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    RAG-powered Q&A endpoint (streaming)
    
    Streams the response as Server-Sent Events (SSE)
    
    Events:
    - token: Individual response tokens
    - sources: Source citations
    - done: Completion signal
    """
    
    async def generate():
        try:
            # Step 1: Search for relevant context
            context_chunks = rag_service.search_similar(
                query=request.question,
                limit=request.top_k,
                chapter_filter=request.chapter_filter
            )
            
            if not context_chunks:
                error_data = {"error": "No relevant content found"}
                yield f"data: {json.dumps(error_data)}\n\n"
                return
            
            # Step 2: Stream response
            stream = agent_service.generate_response(
                question=request.question,
                context_chunks=context_chunks,
                stream=True
            )
            
            # Stream tokens
            for token in stream:
                token_event = StreamToken(token=token)
                yield f"data: {json.dumps(token_event.dict())}\n\n"
            
            # Send sources
            sources = [
                {
                    "page_title": chunk["title"],
                    "page_url": chunk["url"],
                    "section": chunk["chapter"],
                    "relevance_score": chunk["score"]
                }
                for chunk in context_chunks
            ]
            sources_event = StreamSources(type="sources", sources=sources)
            yield f"data: {json.dumps(sources_event.dict())}\n\n"
            
            # Send done signal
            done_event = StreamDone(type="done")
            yield f"data: {json.dumps(done_event.dict())}\n\n"
            
        except Exception as e:
            error_data = {"error": str(e)}
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.post("/chat/context")
async def chat_with_selected_text(
    question: str,
    selected_text: str,
    page_url: str
):
    """
    RAG Q&A with user-selected text as primary context
    
    This endpoint allows users to select text and ask questions about it specifically.
    """
    try:
        # Use selected text as primary context
        # Optionally search for additional context
        context_chunks = rag_service.search_similar(
            query=question,
            limit=2
        )
        
        # Add selected text as highest priority context
        selected_context = {
            "text": selected_text,
            "title": "Selected Text",
            "url": page_url,
            "chapter": "User Selection",
            "score": 1.0
        }
        
        # Prepend selected text to context
        all_context = [selected_context] + context_chunks
        
        # Generate response
        result = agent_service.generate_response_with_metadata(
            question=question,
            context_chunks=all_context
        )
        
        sources = [
            Source(
                page_title=src["title"],
                page_url=src["url"],
                section=src["chapter"],
                relevance_score=src["relevance_score"]
            )
            for src in result["sources"]
        ]
        
        return ChatResponse(
            answer=result["answer"],
            sources=sources
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )
