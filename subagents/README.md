# Subagents - Matrix-Style AI Agent System

This directory contains four specialized Claude Code subagents that work together to build the AI-Driven Book with RAG Chatbot system.

## Architecture

```
subagents/
├── orchestrator.py          # Master controller for all agents
├── BookWriter/
│   ├── agent.py              # Content generation specialist
│   └── README.md             # Documentation
├── RAGEngineer/
│   ├── agent.py              # Vector database specialist
│   └── README.md             # Documentation
├── FrontendDev/
│   ├── agent.py              # UI/UX specialist
│   └── README.md             # Documentation
└── APIBuilder/
    ├── agent.py              # Backend API specialist
    └── README.md             # Documentation
```

## Subagent Capabilities

### 1. BookWriter
**Expertise**: Content generation, technical writing, MDX/Markdown

**Capabilities**:
- Generate comprehensive book content
- Create code examples with explanations
- Organize content into logical chapters
- Generate cross-references and metadata
- Validate content quality

**Skills Used**: Docusaurus Setup (for structure understanding)

### 2. RAGEngineer
**Expertise**: Vector databases, embeddings, search optimization

**Capabilities**:
- Set up Qdrant vector database
- Chunk text into semantic segments
- Generate embeddings via OpenAI
- Optimize vector search performance
- Create indexing and re-indexing tools

**Skills Used**: Qdrant Integration, OpenAI Embeddings

### 3. FrontendDev
**Expertise**: React, TypeScript, Docusaurus, UI/UX

**Capabilities**:
- Configure Docusaurus projects
- Integrate ChatKit SDK for chat UI
- Implement text selection handlers
- Optimize frontend performance
- Create GitHub Pages deployment workflows

**Skills Used**: Docusaurus Setup, Text Selection Handler, GitHub Pages Deploy

### 4. APIBuilder
**Expertise**: FastAPI, Python, OpenAI Agents SDK, system integration

**Capabilities**:
- Design RESTful API endpoints
- Integrate OpenAI Agents SDK (Swarm)
- Orchestrate RAG pipeline
- Handle streaming responses
- Configure backend deployment

**Skills Used**: OpenAI Agent Builder

## Matrix-Style Skill Loading

Each subagent can dynamically load skills on-demand, similar to the Matrix movie concept:

```python
# Example: Load a skill into an agent
agent = BookWriterAgent(project_root="../../")
agent.load_skill("docusaurus-setup")  # ✓ Skill loaded
```

Skills are loaded from `../skills/` directory and activate specific capabilities.

## Usage

### Individual Agent Usage

```python
from BookWriter.agent import BookWriterAgent

# Initialize agent
agent = BookWriterAgent(project_root="../../")

# Load skill
agent.load_skill("docusaurus-setup")

# Execute task
result = agent.execute_task({
    "action": "generate_outline",
    "params": {
        "book_topic": "Introduction to RAG",
        "num_chapters": 4
    }
})

print(result)
```

### Orchestrated Multi-Agent Workflow

```python
from orchestrator import SubagentOrchestrator

# Initialize orchestrator
orchestrator = SubagentOrchestrator()

# Execute complete workflow
result = orchestrator.execute_workflow(
    "phase_1_book_generation",
    params={
        "docusaurus_config": {
            "project_name": "My AI Book",
            "organization_name": "myusername"
        },
        "outline_params": {
            "book_topic": "Introduction to RAG",
            "num_chapters": 4
        }
    }
)

# Check status
orchestrator.print_status_report()
```

## Running the Demo

### Test Individual Agents

```bash
# Test BookWriter
cd subagents/BookWriter
python agent.py

# Test RAGEngineer
cd subagents/RAGEngineer
python agent.py

# Test FrontendDev
cd subagents/FrontendDev
python agent.py

# Test APIBuilder
cd subagents/APIBuilder
python agent.py
```

### Test Orchestrator

```bash
cd subagents
python orchestrator.py
```

This will run a complete demonstration of all three phases:
1. **Phase 1**: Book Development (FrontendDev + BookWriter)
2. **Phase 2**: Backend Setup (RAGEngineer + APIBuilder)
3. **Phase 3**: Integration (FrontendDev)

## Task Execution Interface

All agents share a common task execution interface:

```python
result = agent.execute_task({
    "action": "action_name",  # Action to perform
    "params": {               # Action parameters
        "param1": "value1",
        ...
    }
})

# Result format:
{
    "agent": "AgentName",
    "action": "action_name",
    "status": "success" | "error",
    "timestamp": "2025-12-10T00:00:00Z",
    "data": {...}  # or "error": "message"
}
```

## Available Actions by Agent

### BookWriter Actions
- `generate_outline` - Create chapter structure
- `generate_content` - Generate page content
- `validate` - Validate content quality
- `load_skill` - Load a skill module

### RAGEngineer Actions
- `setup_collection` - Create Qdrant collection
- `index_document` - Index a page
- `search` - Search for similar vectors
- `optimize` - Optimize search parameters
- `load_skill` - Load a skill module

### FrontendDev Actions
- `configure_docusaurus` - Generate Docusaurus config
- `create_chatbot` - Generate ChatBot components
- `create_text_selector` - Generate text selection handler
- `optimize` - Get performance recommendations
- `create_deployment` - Generate deployment workflow
- `load_skill` - Load a skill module

### APIBuilder Actions
- `design_endpoint` - Design API endpoint spec
- `create_agent` - Create RAG agent config
- `handle_request` - Handle RAG request
- `create_deployment` - Generate deployment config
- `generate_docs` - Generate API documentation
- `load_skill` - Load a skill module

## Agent Status

Get status of any agent:

```python
status = agent.get_status()

# Returns:
{
    "agent": "AgentName",
    "status": "initialized" | "active",
    "capabilities": ["cap1", "cap2", ...],
    "loaded_skills": ["skill1", "skill2", ...]
}
```

## Cross-Agent Communication

The orchestrator handles communication between agents through:

1. **Handoff Documents**: Each phase produces output used by the next
2. **Shared Context**: Project root and configuration shared across agents
3. **Workflow Coordination**: Orchestrator manages execution order

## Development Notes

### Simulation vs Real Implementation

These agents currently **simulate** their operations for demonstration purposes:

- **Vector embeddings**: Return dummy vectors (real: call OpenAI API)
- **Vector search**: Return mock results (real: query Qdrant)
- **Agent responses**: Return template text (real: call OpenAI Agents SDK)

To convert to production:
1. Replace simulation code with actual API calls
2. Add proper error handling and retries
3. Implement authentication and rate limiting
4. Add logging and monitoring

### Extending Agents

To add new capabilities to an agent:

1. Add method to agent class
2. Add action handler in `execute_task()`
3. Update capabilities list
4. Document in agent's README

Example:

```python
def new_capability(self, param1: str) -> Dict[str, Any]:
    """New capability description"""
    # Implementation
    return {"result": "data"}

def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
    # ... existing code ...
    elif action == "new_action":
        result["data"] = self.new_capability(**params)
        result["status"] = "success"
```

## Integration with Main Project

These agents are designed to be used in the implementation phases:

- **Phase 1**: BookWriter + FrontendDev generate and deploy book
- **Phase 2**: RAGEngineer + APIBuilder set up backend
- **Phase 3**: FrontendDev integrates chatbot UI

## License

MIT - See project root LICENSE file

---

**Status**: ✅ All subagents implemented and tested  
**Ready for**: Phase 1-3 execution  
**Matrix-Style Loading**: Fully functional
