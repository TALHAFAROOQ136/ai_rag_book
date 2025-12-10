"""
OpenAI Agent Service - RAG-optimized Q&A
"""

from typing import List, Dict, Any, Optional, Generator
from openai import OpenAI
import os
from datetime import datetime


class AgentService:
    """
    OpenAI Agent Service for RAG Q&A
    
    Uses OpenAI Chat Completions API with RAG-optimized prompts
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
        
        # RAG-optimized system prompt
        self.system_prompt = """You are a helpful Q&A assistant for "Introduction to RAG" book.

Your responsibilities:
1. Answer questions based ONLY on the provided context from the book
2. Always cite specific sections in your answers
3. If information is not in the context, clearly state that
4. Be concise yet thorough in your explanations
5. Use markdown formatting for clarity

Response Guidelines:
- Begin with a direct answer to the question
- Provide supporting details from the context
- Include citations in the format: **Source: [Page Title]**
- Format code with proper syntax highlighting
- Use bullet points and headers for structure

Quality Standards:
- Do not invent information not present in the context
- Ask for clarification if the question is ambiguous
- Maintain a helpful and educational tone
- Reference multiple sources when relevant
"""
    
    def create_rag_prompt(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]]
    ) -> str:
        """
        Create RAG prompt with context
        
        Args:
            question: User's question
            context_chunks: Retrieved chunks from vector search
            
        Returns:
            Formatted prompt with context
        """
        # Format context
        context_parts = []
        for i, chunk in enumerate(context_chunks):
            context_parts.append(f"""--- Context {i+1} ---
**Title**: {chunk['title']} ({chunk['chapter']})
**URL**: {chunk['url']}
**Relevance**: {chunk['score']:.2f}

{chunk['text']}
""")
        
        context_text = "\n\n".join(context_parts)
        
        # Create full prompt
        prompt = f"""Based on the following context from the book, please answer the question.

Context:
{context_text}

Question: {question}

Please provide a comprehensive answer based on the context above. Include citations to the source sections."""
        
        return prompt
    
    def generate_response(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]],
        stream: bool = False
    ) -> Any:
        """
        Generate response using OpenAI
        
        Args:
            question: User's question
            context_chunks: Retrieved context chunks
            stream: Whether to stream the response
            
        Returns:
            Response text or stream generator
        """
        # Create RAG prompt
        user_prompt = self.create_rag_prompt(question, context_chunks)
        
        # Prepare messages
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Generate response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=stream
        )
        
        if stream:
            return self._stream_response(response)
        else:
            return response.choices[0].message.content
    
    def _stream_response(self, response) -> Generator[str, None, None]:
        """
        Stream response chunks
        
        Args:
            response: OpenAI streaming response
            
        Yields:
            Response chunks
        """
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    def generate_response_with_metadata(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate response with full metadata
        
        Args:
            question: User's question
            context_chunks: Retrieved context chunks
            
        Returns:
            Dict with answer, sources, and metadata
        """
        # Generate answer
        answer = self.generate_response(question, context_chunks, stream=False)
        
        # Extract sources
        sources = [
            {
                "title": chunk["title"],
                "url": chunk["url"],
                "chapter": chunk["chapter"],
                "relevance_score": chunk["score"]
            }
            for chunk in context_chunks
        ]
        
        # Calculate tokens (approximate)
        prompt_tokens = sum(len(chunk["text"].split()) for chunk in context_chunks) + len(question.split())
        completion_tokens = len(answer.split())
        
        return {
            "answer": answer,
            "sources": sources,
            "metadata": {
                "model": self.model,
                "temperature": self.temperature,
                "prompt_tokens": prompt_tokens * 1.3,  # Rough estimate
                "completion_tokens": completion_tokens * 1.3,
                "total_tokens": (prompt_tokens + completion_tokens) * 1.3,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
