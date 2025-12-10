"""
OpenAI Agent Builder Skill
===========================
Create and configure OpenAI Agents using the Swarm framework

This skill provides agent configuration, prompt engineering,
and integration patterns for RAG-optimized conversational AI.

Matrix-Style Loading: ✓
Self-Contained: ✓
Importable: ✓
"""

from typing import Dict, List, Optional, Any, Generator
from datetime import datetime
import json


class OpenAIAgentBuilder:
    """
    OpenAI Agent Builder Skill
    
    Capabilities:
    - Create RAG-optimized agents
    - Design system prompts
    - Configure streaming responses
    - Handle context windows
    - Manage conversation history
    
    Note: This is a template/configuration skill.
    In production, use openai library and Swarm framework.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.skill_name = "OpenAI Agent Builder"
        self.version = "1.0.0"
        self.agents = {}
    
    def create_rag_agent(
        self,
        agent_name: str,
        book_title: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.3,
        max_tokens: int = 2000,
        streaming: bool = True
    ) -> Dict[str, Any]:
        """
        Create a RAG-optimized Q&A agent
        
        Args:
            agent_name: Unique name for the agent
            book_title: Title of the book for context
            model: OpenAI model to use
            temperature: Creativity level (0.0-2.0)
            max_tokens: Maximum response length
            streaming: Enable streaming responses
            
        Returns:
            Agent configuration dict
        """
        system_prompt = self._create_rag_system_prompt(book_title)
        
        agent_config = {
            "name": agent_name,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "streaming": streaming,
            "system_prompt": system_prompt,
            "tools": [],  # Can add function calling tools
            "created_at": datetime.utcnow().isoformat(),
            "type": "rag_qa_agent"
        }
        
        self.agents[agent_name] = agent_config
        return agent_config
    
    def _create_rag_system_prompt(self, book_title: str) -> str:
        """
        Create optimized system prompt for RAG
        
        Args:
            book_title: Book title for context
            
        Returns:
            System prompt string
        """
        return f"""You are an expert Q&A assistant for "{book_title}".

Your responsibilities:
1. Answer questions based ONLY on the provided context from the book
2. Always cite specific sections and page references in your answers
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

Example Response Format:
[Direct answer to question]

[Supporting explanation with details from context]

**Sources:**
- [Page Title 1] - [Specific Section]
- [Page Title 2] - [Specific Section]
"""
    
    def create_prompt_with_context(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Construct complete prompt with retrieved context
        
        Args:
            question: User's question
            context_chunks: Retrieved chunks from vector search
            conversation_history: Previous messages (optional)
            
        Returns:
            Complete prompt string ready for the agent
        """
        # Format context
        context_parts = []
        for i, chunk in enumerate(context_chunks):
            metadata = chunk.get("payload", {})
            context_parts.append(f"""--- Context {i+1} ---
**Source**: {metadata.get('page_title', 'Unknown')} - {metadata.get('section', 'Main')}
**URL**: {metadata.get('page_url', '')}
**Relevance Score**: {chunk.get('score', 0):.2f}

{metadata.get('text', chunk.get('text', ''))}
""")
        
        context_text = "\n\n".join(context_parts)
        
        # Add conversation history if provided
        history_text = ""
        if conversation_history:
            history_text = "\nPrevious conversation:\n"
            for msg in conversation_history[-3:]:  # Last 3 messages only
                role = msg.get("role", "user")
                content = msg.get("content", "")
                history_text += f"{role.capitalize()}: {content}\n"
            history_text += "\n"
        
        # Construct full prompt
        prompt = f"""You have access to the following context from the book:

{context_text}

{history_text}Question: {question}

Please answer the question based on the context above. Include citations to the sources."""
        
        return prompt
    
    def configure_streaming(
        self,
        agent_name: str,
        enable: bool = True
    ) -> Dict[str, Any]:
        """
        Configure streaming for an agent
        
        Args:
            agent_name: Name of agent to configure
            enable: Enable or disable streaming
            
        Returns:
            Updated configuration
        """
        if agent_name not in self.agents:
            return {"error": f"Agent '{agent_name}' not found"}
        
        self.agents[agent_name]["streaming"] = enable
        
        return {
            "agent_name": agent_name,
            "streaming": enable,
            "updated_at": datetime.utcnow().isoformat()
        }
    
    def add_function_tool(
        self,
        agent_name: str,
        function_name: str,
        description: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Add a function calling tool to the agent
        
        Args:
            agent_name: Target agent
            function_name: Name of the function
            description: What the function does
            parameters: JSON schema for parameters
            
        Returns:
            Tool configuration
        """
        tool = {
            "type": "function",
            "function": {
                "name": function_name,
                "description": description,
                "parameters": parameters
            }
        }
        
        if agent_name in self.agents:
            if "tools" not in self.agents[agent_name]:
                self.agents[agent_name]["tools"] = []
            self.agents[agent_name]["tools"].append(tool)
        
        return tool
    
    def estimate_tokens(
        self,
        text: str,
        model: str = "gpt-4o-mini"
    ) -> int:
        """
        Estimate token count for text
        
        Args:
            text: Text to estimate
            model: Model to use for estimation
            
        Returns:
            Estimated token count
        """
        # Simple estimation: ~4 chars per token
        # In production, use tiktoken library
        return len(text) // 4
    
    def create_conversation_manager(
        self,
        max_history: int = 10
    ) -> Dict[str, Any]:
        """
        Create conversation history manager
        
        Args:
            max_history: Maximum messages to keep
            
        Returns:
            Manager configuration
        """
        return {
            "max_history": max_history,
            "messages": [],
            "total_tokens": 0,
            "created_at": datetime.utcnow().isoformat()
        }
    
    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """Get agent configuration"""
        return self.agents.get(agent_name, {})
    
    def list_agents(self) -> List[str]:
        """List all configured agents"""
        return list(self.agents.keys())


# Example usage
def main():
    """Example usage of OpenAI Agent Builder Skill"""
    print("="*60)
    print("OpenAI Agent Builder Skill - Example Usage")
    print("="*60)
    
    # Initialize skill
    skill = OpenAIAgentBuilder(api_key="sk-your-key")
    
    # Example 1: Create RAG agent
    print("\n[Example 1] Create RAG Agent")
    agent = skill.create_rag_agent(
        agent_name="rag_book_assistant",
        book_title="Introduction to RAG",
        model="gpt-4o-mini",
        temperature=0.3
    )
    print(f"✓ Agent created: {agent['name']}")
    print(f"  Model: {agent['model']}")
    print(f"  Temperature: {agent['temperature']}")
    print(f"  Streaming: {agent['streaming']}")
    
    # Example 2: Create prompt with context
    print("\n[Example 2] Create Prompt with Context")
    context_chunks = [
        {
            "score": 0.92,
            "payload": {
                "page_title": "What is RAG?",
                "page_url": "/intro/what-is-rag",
                "section": "Introduction",
                "text": "RAG stands for Retrieval-Augmented Generation. It's a technique that combines information retrieval with text generation..."
            }
        },
        {
            "score": 0.85,
            "payload": {
                "page_title": "RAG Benefits",
                "page_url": "/chapter-1/benefits",
                "section": "Key Advantages",
                "text": "The main benefits of RAG include: 1) Improved accuracy through grounding in real data..."
            }
        }
    ]
    
    prompt = skill.create_prompt_with_context(
        question="What is RAG and why is it useful?",
        context_chunks=context_chunks
    )
    print(f"✓ Prompt created ({len(prompt)} chars)")
    print(f"  Estimated tokens: {skill.estimate_tokens(prompt)}")
    
    # Example 3: Add function tool
    print("\n[Example 3] Add Function Tool")
    tool = skill.add_function_tool(
        agent_name="rag_book_assistant",
        function_name="search_book",
        description="Search for specific topics in the book",
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "section": {
                    "type": "string",
                    "description": "Specific section to search (optional)"
                }
            },
            "required": ["query"]
        }
    )
    print(f"✓ Tool added: {tool['function']['name']}")
    
    # Example 4: List agents
    print("\n[Example 4] List All Agents")
    agents = skill.list_agents()
    print(f"✓ Configured agents: {', '.join(agents)}")
    
    # Example 5: Conversation manager
    print("\n[Example 5] Create Conversation Manager")
    manager = skill.create_conversation_manager(max_history=10)
    print(f"✓ Conversation manager created")
    print(f"  Max history: {manager['max_history']}")
    
    print("\n" + "="*60)
    print("Skill demonstration complete")
    print("="*60)


if __name__ == "__main__":
    main()
