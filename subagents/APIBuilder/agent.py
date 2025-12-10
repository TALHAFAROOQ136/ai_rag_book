"""
APIBuilder Subagent
===================
Backend API and AI Agent Integration specialist

Capabilities:
- Design and implement RESTful APIs
- Integrate OpenAI Agents SDK
- Configure RAG pipeline
- Handle streaming responses
- Deploy backend services

Matrix-Style Skill Loading:
- Can load "OpenAI Agent Builder" skill for Swarm integration
"""

import os
import json
from typing import Dict, List, Optional, Any, Generator
from datetime import datetime
from pathlib import Path


class APIBuilderAgent:
    """
    APIBuilder Subagent - Backend API Specialist
    
    Responsibilities:
    - FastAPI application design and implementation
    - OpenAI Agents SDK integration
    - RAG pipeline orchestration
    - Streaming response handling
    - Backend deployment
    """
    
    def __init__(self, project_root: str):
        self.agent_name = "APIBuilder"
        self.project_root = Path(project_root)
        self.loaded_skills = {}
        self.capabilities = [
            "api_design",
            "openai_agent_integration",
            "rag_pipeline_orchestration",
            "streaming_responses",
            "error_handling",
            "deployment_configuration"
        ]
        self.status = "initialized"
        self.agent_instance = None
        
    def load_skill(self, skill_name: str) -> bool:
        """
        Matrix-style skill loading
        
        Args:
            skill_name: Name of skill (e.g., "openai-agent-builder")
            
        Returns:
            bool: Success status
        """
        skill_path = self.project_root / "skills" / skill_name / "README.md"
        
        if skill_path.exists():
            with open(skill_path, 'r', encoding='utf-8') as f:
                skill_content = f.read()
            
            self.loaded_skills[skill_name] = {
                "loaded_at": datetime.utcnow().isoformat(),
                "documentation": skill_content,
                "status": "active"
            }
            print(f"✓ Skill '{skill_name}' loaded into {self.agent_name}")
            
            # Activate skill-specific capabilities
            if skill_name == "openai-agent-builder":
                self._activate_agent_capabilities()
            
            return True
        else:
            print(f"✗ Skill '{skill_name}' not found")
            return False
    
    def _activate_agent_capabilities(self):
        """Activate OpenAI Agent capabilities"""
        print("  → OpenAI Agent SDK integration ready")
        print("  → Streaming response handling enabled")
        print("  → RAG prompt construction loaded")
    
    def design_api_endpoint(
        self,
        endpoint_path: str,
        method: str,
        description: str,
        request_model: Dict[str, Any],
        response_model: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Design API endpoint specification
        
        Input:
            endpoint_path: URL path (e.g., "/api/chat")
            method: HTTP method (GET, POST, etc.)
            description: Endpoint description
            request_model: Pydantic model specification
            response_model: Response model specification
            
        Output:
            Endpoint specification dict
        """
        return {
            "path": endpoint_path,
            "method": method,
            "description": description,
            "request_schema": request_model,
            "response_schema": response_model,
            "authentication": "none",  # For MVP
            "rate_limit": None,
            "created_at": datetime.utcnow().isoformat()
        }
    
    def create_rag_agent(
        self,
        book_title: str = "the book",
        model: str = "gpt-4o-mini",
        temperature: float = 0.3
    ) -> Dict[str, Any]:
        """
        Create RAG-optimized OpenAI Agent configuration
        
        Input:
            book_title: Title of the book for context
            model: OpenAI model to use
            temperature: Temperature setting (0.0-2.0)
            
        Output:
            Agent configuration
        """
        system_prompt = f"""You are a helpful Q&A assistant for {book_title}.

Your role:
- Answer questions based ONLY on the provided context
- Cite specific sections when answering
- If information is not in the context, say so clearly
- Be concise but thorough
- Use markdown formatting for clarity

Guidelines:
- Always reference the source passages
- Don't make up information
- If the question is unclear, ask for clarification
- Format code blocks with syntax highlighting
"""
        
        config = {
            "agent_name": f"{book_title.replace(' ', '_')}_RAG_Agent",
            "model": model,
            "temperature": temperature,
            "max_tokens": 2000,
            "system_prompt": system_prompt,
            "streaming_enabled": True,
            "tools": [],  # Can add function calling tools later
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.agent_instance = config
        return config
    
    def construct_rag_prompt(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Construct RAG prompt with retrieved context
        
        Input:
            question: User's question
            context_chunks: Retrieved chunks from vector search
            conversation_history: Previous messages (optional)
            
        Output:
            Complete prompt string
        """
        # Format context
        context_text = "\n\n---\n\n".join([
            f"**Source**: {chunk['metadata']['page_title']} - {chunk['metadata'].get('section', 'Main')}\n"
            f"**URL**: {chunk['metadata']['page_url']}\n\n"
            f"{chunk['metadata'].get('text_preview', chunk.get('text', ''))}"
            for chunk in context_chunks
        ])
        
        # Build full prompt
        prompt = f"""Context from the book:

{context_text}

---

Question: {question}

Please answer the question based on the context above. Include citations to the source sections."""
        
        return prompt
    
    def simulate_streaming_response(
        self,
        answer: str
    ) -> Generator[str, None, None]:
        """
        Simulate streaming response (token by token)
        
        Input:
            answer: Complete answer text
            
        Output:
            Generator yielding tokens
        """
        words = answer.split()
        for word in words:
            yield word + " "
    
    def handle_rag_request(
        self,
        question: str,
        retrieved_chunks: List[Dict[str, Any]],
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Handle complete RAG request
        
        Input:
            question: User question
            retrieved_chunks: Results from vector search
            stream: Whether to stream response
            
        Output:
            Response with answer and sources
        """
        # Construct prompt
        prompt = self.construct_rag_prompt(question, retrieved_chunks)
        
        # Simulate agent response (in real implementation, call OpenAI)
        answer = f"Based on the provided context, {question.lower()} is explained in the book. "
        answer += "The key points are: relevance, accuracy, and proper citations. "
        answer += "\n\n**Sources**:\n"
        for chunk in retrieved_chunks[:3]:
            answer += f"- [{chunk['metadata']['page_title']}]({chunk['metadata']['page_url']})\n"
        
        response = {
            "answer": answer,
            "sources": [
                {
                    "page_title": chunk["metadata"]["page_title"],
                    "page_url": chunk["metadata"]["page_url"],
                    "section": chunk["metadata"].get("section", "Main"),
                    "relevance_score": chunk.get("score", 0.85)
                }
                for chunk in retrieved_chunks
            ],
            "tokens_used": len(prompt.split()) + len(answer.split()),
            "model": self.agent_instance.get("model", "gpt-4o-mini") if self.agent_instance else "gpt-4o-mini",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if stream:
            response["stream_generator"] = self.simulate_streaming_response(answer)
        
        return response
    
    def create_error_response(
        self,
        error_type: str,
        message: str,
        status_code: int = 500
    ) -> Dict[str, Any]:
        """
        Create standardized error response
        
        Input:
            error_type: Type of error (validation, server, etc.)
            message: Error message
            status_code: HTTP status code
            
        Output:
            Error response dict
        """
        return {
            "error": {
               "type": error_type,
                "message": message,
                "timestamp": datetime.utcnow().isoformat()
            },
            "status_code": status_code
        }
    
    def generate_api_documentation(
        self,
        endpoints: List[Dict[str, Any]]
    ) -> str:
        """
        Generate API documentation in Markdown
        
        Input:
            endpoints: List of endpoint specifications
            
        Output:
            Markdown documentation
        """
        doc = "# API Documentation\n\n"
        doc += f"**Generated**: {datetime.utcnow().isoformat()}\n\n"
        doc += "## Endpoints\n\n"
        
        for endpoint in endpoints:
            doc += f"### {endpoint['method']} {endpoint['path']}\n\n"
            doc += f"{endpoint['description']}\n\n"
            doc += "**Request**:\n```json\n"
            doc += json.dumps(endpoint['request_schema'], indent=2)
            doc += "\n```\n\n"
            doc += "**Response**:\n```json\n"
            doc += json.dumps(endpoint['response_schema'], indent=2)
            doc += "\n```\n\n"
            doc += "---\n\n"
        
        return doc
    
    def create_deployment_config(
        self,
        platform: str = "vercel",
        python_version: str = "3.10"
    ) -> Dict[str, Any]:
        """
        Create deployment configuration
        
        Input:
            platform: Deployment platform (vercel, railway, docker)
            python_version: Python version to use
            
        Output:
            Platform-specific config
        """
        if platform == "vercel":
            config = {
                "version": 2,
                "builds": [
                    {
                        "src": "app/main.py",
                        "use": "@vercel/python"
                    }
                ],
                "routes": [
                    {
                        "src": "/(.*)",
                        "dest": "app/main.py"
                    }
                ],
                "env": {
                    "PYTHONPATH": "/var/task",
                    "PYTHON_VERSION": python_version
                }
            }
        elif platform == "docker":
            config = {
                "dockerfile": f"""FROM python:{python_version}-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
            }
        else:
            config = {"error": f"Unknown platform: {platform}"}
        
        return config
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main task execution interface
        
        Input:
            task: {
                "action": "design_endpoint" | "create_agent" | "handle_request",
                "params": {...}
            }
            
        Output:
            Task result with status and data
        """
        action = task.get("action")
        params = task.get("params", {})
        
        result = {
            "agent": self.agent_name,
            "action": action,
            "status": "pending",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            if action == "design_endpoint":
                result["data"] = self.design_api_endpoint(**params)
                result["status"] = "success"
                
            elif action == "create_agent":
                result["data"] = self.create_rag_agent(**params)
                result["status"] = "success"
                
            elif action == "handle_request":
                result["data"] = self.handle_rag_request(**params)
                result["status"] = "success"
                
            elif action == "create_deployment":
                result["data"] = self.create_deployment_config(**params)
                result["status"] = "success"
                
            elif action == "generate_docs":
                result["data"] = {
                    "documentation": self.generate_api_documentation(params.get("endpoints", [])),
                    "format": "markdown"
                }
                result["status"] = "success"
                
            elif action == "load_skill":
                success = self.load_skill(params.get("skill_name"))
                result["status"] = "success" if success else "failed"
                result["data"] = {"loaded": success}
                
            else:
                result["status"] = "error"
                result["error"] = f"Unknown action: {action}"
                
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent": self.agent_name,
            "status": self.status,
            "capabilities": self.capabilities,
            "loaded_skills": list(self.loaded_skills.keys()),
            "agent_configured": self.agent_instance is not None
        }


def main():
    """Example usage of APIBuilder agent"""
    print("="*60)
    print("APIBuilder Subagent - Example Usage")
    print("="*60)
    
    # Initialize agent
    agent = APIBuilderAgent(project_root="../../")
    print(f"\n✓ {agent.agent_name} initialized")
    
    # Load skill (Matrix-style)
    print("\n--- Loading Skill ---")
    agent.load_skill("openai-agent-builder")
    
    # Create RAG agent
    print("\n--- Creating RAG Agent ---")
    task = {
        "action": "create_agent",
        "params": {
            "book_title": "Introduction to RAG",
            "model": "gpt-4o-mini",
            "temperature": 0.3
        }
    }
    result = agent.execute_task(task)
    print(f"Status: {result['status']}")
    print(f"Agent: {result['data']['agent_name']}")
    print(f"Model: {result['data']['model']}")
    
    # Design endpoint
    print("\n--- Designing API Endpoint ---")
    task = {
        "action": "design_endpoint",
        "params": {
            "endpoint_path": "/api/chat",
            "method": "POST",
            "description": "Chat endpoint for RAG Q&A",
            "request_model": {"question": "string", "context": "string?"},
            "response_model": {"answer": "string", "sources": "array"}
        }
    }
    result = agent.execute_task(task)
    print(f"Status: {result['status']}")
    print(f"Endpoint: {result['data']['method']} {result['data']['path']}")
    
    # Handle RAG request
    print("\n--- Handling RAG Request ---")
    mock_chunks = [
        {
            "metadata": {
                "page_title": "What is RAG?",
                "page_url": "/chapter-1/what-is-rag",
                "section": "Introduction",
                "text_preview": "RAG combines retrieval with generation..."
            },
            "score": 0.92
        }
    ]
    
    task = {
        "action": "handle_request",
        "params": {
            "question": "What is RAG?",
            "retrieved_chunks": mock_chunks,
            "stream": False
        }
    }
    result = agent.execute_task(task)
    print(f"Status: {result['status']}")
    print(f"Answer Length: {len(result['data']['answer'])} chars")
    print(f"Sources: {len(result['data']['sources'])}")
    print(f"Tokens Used: {result['data']['tokens_used']}")
    
    # Create deployment config
    print("\n--- Creating Deployment Config ---")
    task = {
        "action": "create_deployment",
        "params": {
            "platform": "vercel",
            "python_version": "3.10"
        }
    }
    result = agent.execute_task(task)
    print(f"Status: {result['status']}")
    print(f"Platform: vercel")
    print(f"Config Keys: {list(result['data'].keys())}")
    
    # Get status
    print("\n--- Agent Status ---")
    status = agent.get_status()
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
