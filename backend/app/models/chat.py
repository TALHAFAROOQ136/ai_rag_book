"""
Pydantic Models for Chat API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    question: str = Field(..., description="User's question", min_length=1)
    top_k: int = Field(5, description="Number of relevant chunks to retrieve", ge=1, le=10)
    chapter_filter: Optional[str] = Field(None, description="Filter results by chapter")


class Source(BaseModel):
    """Source citation model"""
    page_title: str
    page_url: str
    section: str
    relevance_score: float


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str
    sources: List[Source]


class StreamToken(BaseModel):
    """Streaming response token"""
    type: str = "token"
    token: str


class StreamSources(BaseModel):
    """Streaming sources event"""
    type: str = "sources"
    sources: List[Dict[str, Any]]


class StreamDone(BaseModel):
    """Streaming completion event"""
    type: str = "done"


class ReindexRequest(BaseModel):
    """Request model for reindexing"""
    docs_path: Optional[str] = Field(None, description="Path to documentation directory")
    background: bool = Field(False, description="Run indexing in background")


class ReindexResponse(BaseModel):
    """Response model for reindexing"""
    status: str
    message: str
    indexed_count: int
    failed_count: int
    details: Optional[List[Dict[str, Any]]] = None
