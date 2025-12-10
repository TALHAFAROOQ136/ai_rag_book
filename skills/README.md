# Skills - Reusable Matrix-Style Capabilities

This directory contains five self-contained, reusable skills that can be loaded on-demand by any subagent.

## Architecture

```
skills/
├── docusaurus-setup/
│   ├── skill.py           # Docusaurus project initialization
│   └── README.md          # Documentation
├── qdrant-integration/
│   ├── skill.py           # Vector database management
│   └── README.md          # Documentation
├── openai-agent-builder/
│   ├── skill.py           # RAG agent configuration
│   └── README.md          # Documentation
├── github-pages-deploy/
│   ├── skill.py           # Automated deployment
│   └── README.md          # Documentation
└── text-selection-handler/
    ├── skill.py           # Browser text selection
    └── README.md          # Documentation
```

## Skills Overview

### 1. Docusaurus Setup
**Category**: Frontend / Documentation  
**Reusability**: High  
**Primary User**: FrontendDev subagent

**Capabilities**:
- Generate Docusaurus configuration files
- Create sidebar navigation
- Set up custom themes and CSS
- Initialize complete project structure

**Example**:
```python
from skills.docusaurus_setup.skill import DocusaurusSetup

skill = DocusaurusSetup(project_root=Path("."))
config = skill.create_docusaurus_config(
    project_name="my-book",
    title="My AI Book",
    url="https://myuser.github.io"
)
```

### 2. Qdrant Integration
**Category**: Backend / AI / Database  
**Reusability**: Very High  
**Primary User**: RAGEngineer subagent

**Capabilities**:
- Create and configure Qdrant collections
- Upload vectors with metadata
- Perform semantic search
- Batch operations for large datasets
- Collection management utilities

**Example**:
```python
from skills.qdrant_integration.skill import QdrantIntegration

skill = QdrantIntegration(url="...", api_key="...")
skill.create_collection("book_chunks", vector_size=1536)
skill.upsert_vectors("book_chunks", points)
results = skill.search("book_chunks", query_vector, limit=5)
```

### 3. OpenAI Agent Builder
**Category**: AI / Backend  
**Reusability**: Very High  
**Primary User**: APIBuilder subagent

**Capabilities**:
- Create RAG-optimized agents
- Design effective system prompts
- Configure streaming responses
- Manage conversation history
- Integrate function calling tools

**Example**:
```python
from skills.openai_agent_builder.skill import OpenAIAgentBuilder

skill = OpenAIAgentBuilder(api_key="...")
agent = skill.create_rag_agent(
    agent_name="qa_assistant",
    book_title="Introduction to RAG",
    model="gpt-4o-mini"
)
prompt = skill.create_prompt_with_context(question, context_chunks)
```

### 4. GitHub Pages Deploy
**Category**: DevOps / Deployment  
**Reusability**: High  
**Primary User**: FrontendDev subagent

**Capabilities**:
- Generate GitHub Actions workflows
- Configure repository settings
- Support custom domains  
- Create deployment checklists
- Troubleshoot common issues

**Example**:
```python
from skills.github_pages_deploy.skill import GitHubPagesDeploy

skill = GitHubPagesDeploy()
workflow = skill.create_deployment_workflow(
    site_generator="docusaurus",
    node_version="18",
    custom_domain="mybook.com"
)
```

### 5. Text Selection Handler
**Category**: Frontend / UX  
**Reusability**: High  
**Primary User**: FrontendDev subagent

**Capabilities**:
- Detect text selections in browser
- Create context menus
- Track selection position for UI
- Integrate with chat components
- Generate TypeScript/React code

**Example**:
```python
from skills.text_selection_handler.skill import TextSelectionHandler

skill = TextSelectionHandler()
hook_code = skill.create_selection_hook(min_length=15)
menu_code = skill.create_context_menu_component(actions)
```

## Matrix-Style Loading

Skills can be dynamically loaded by subagents:

```python
# In a subagent
def load_skill(self, skill_name: str) -> bool:
    skill_path = self.project_root / "skills" / skill_name / "README.md"
    if skill_path.exists():
        # Load skill documentation
        self.loaded_skills[skill_name] = {...}
        return True
    return False

# Usage
agent.load_skill("docusaurus-setup")  # ✓ Skill loaded
```

## Running Examples

Each skill includes a `main()` function with usage examples:

```bash
# Run individual skill demonstrations
python skills/docusaurus-setup/skill.py
python skills/qdrant-integration/skill.py
python skills/openai-agent-builder/skill.py
python skills/github-pages-deploy/skill.py
python skills/text-selection-handler/skill.py
```

## Import Usage

Skills are designed to be imported and used directly:

```python
# Method 1: Direct import
from skills.docusaurus_setup.skill import DocusaurusSetup
skill = DocusaurusSetup(project_root=Path("."))

# Method 2: Dynamic loading (via subagent)
agent = FrontendDevAgent(project_root=".")
agent.load_skill("docusaurus-setup")
```

## Skill Structure

All skills follow this pattern:

```python
class SkillName:
    def __init__(self, ...):
        self.skill_name = "..."
        self.version = "1.0.0"
    
    def primary_capability(self, ...) -> ReturnType:
        """Main skill function"""
        pass
    
    def helper_function(self, ...) -> ReturnType:
        """Supporting function"""
        pass

def main():
    """Example usage"""
    pass
```

## Skill Categories

| Category | Skills | Primary Subagent |
|----------|--------|------------------|
| **Frontend** | Docusaurus Setup, Text Selection | FrontendDev |
| **Backend** | Qdrant Integration, OpenAI Agent Builder | RAGEngineer, APIBuilder |
| **DevOps** | GitHub Pages Deploy | FrontendDev |

## Extending Skills

To add a new skill:

1. Create directory: `skills/new-skill/`
2. Create `skill.py` with class and `main()`
3. Create `README.md` with documentation
4. Update this README
5. Skills are now loadable by any subagent

## Production Notes

Current implementations are **simulations** for demonstration. To use in production:

### Qdrant Integration
Replace with actual qdrant-client:
```python
from qdrant_client import QdrantClient
client = QdrantClient(url=url, api_key=api_key)
```

### OpenAI Agent Builder
Replace with actual OpenAI SDK:
```python
from openai import OpenAI
client = OpenAI(api_key=api_key)
```

### Text Selection Handler
The generated TypeScript code is production-ready and can be used directly in React applications.

## Skill Dependencies

Some skills have dependencies for production use:

- **Docusaurus Setup**: No runtime dependencies (generates config files)
- **Qdrant Integration**: `qdrant-client>=1.7.0`
- **OpenAI Agent Builder**: `openai>=1.12.0`
- **GitHub Pages Deploy**: No runtime dependencies (generates YAML)
- **Text Selection Handler**: React 18+, TypeScript 5+

## Testing

```bash
# Test all skills
for skill in docusaurus-setup qdrant-integration openai-agent-builder github-pages-deploy text-selection-handler; do
    echo "Testing $skill..."
    python skills/$skill/skill.py
done
```

## License

MIT - See project root LICENSE file

---

**Status**: ✅ All 5 skills implemented  
**Self-Contained**: ✓  
**Importable**: ✓  
**Matrix-Style Loading**: ✓  
**Example Usage**: ✓
