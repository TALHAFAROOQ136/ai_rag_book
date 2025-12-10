# Project Constitution: AI-Driven Book with RAG Chatbot

## Project Vision
Develop an integrated system combining AI-generated documentation with intelligent question-answering capabilities, demonstrating the Matrix-like concept of on-demand knowledge loading through Claude Code Subagents and reusable Skills.

## Core Principles

### 1. AI-Driven Development Philosophy
- **Specification-First Approach**: Every feature begins with clear specifications before implementation
- **Claude Code as Primary Developer**: Leverage Claude Code for autonomous, agentic development
- **Intelligent Automation**: Maximize AI capabilities while maintaining human oversight
- **Iterative Refinement**: Continuous improvement through AI-assisted iterations

### 2. Architecture Principles
- **Separation of Concerns**: Book generation and RAG functionality are distinct but integrated modules
- **API-First Design**: FastAPI backend enables flexible frontend integration
- **Scalable Infrastructure**: Cloud-based solutions (GitHub Pages, Qdrant Cloud) for zero-cost scalability
- **Modular Components**: Reusable subagents and skills for extensibility

### 3. User Experience Principles
- **Seamless Integration**: Chatbot feels native to the book reading experience
- **Context-Aware Interactions**: Support both full-book and selected-text queries
- **Progressive Enhancement**: Book remains readable without JavaScript/chatbot
- **Responsive Design**: Works across desktop and mobile devices

### 4. Technical Excellence
- **Modern Tech Stack**: Docusaurus, FastAPI, OpenAI SDKs, Qdrant
- **Type Safety**: TypeScript/Python type hints throughout
- **Error Handling**: Graceful degradation and informative error messages
- **Performance**: Fast page loads, efficient vector searches, streaming responses

### 5. Reusability & Intelligence
- **Subagent Architecture**: Create specialized Claude Code subagents for distinct tasks
  - **BookWriter Agent**: Generates and structures book content
  - **RAG Engineer Agent**: Handles vector database and retrieval logic
  - **Frontend Developer Agent**: Manages Docusaurus integration
  - **API Builder Agent**: Constructs FastAPI backend
  
- **Reusable Skills (Programs)**: Build modular, reusable capabilities
  - **Skill: Docusaurus Setup**: Initialize and configure Docusaurus projects
  - **Skill: Qdrant Integration**: Connect and manage vector databases
  - **Skill: OpenAI Agent Builder**: Create conversational AI agents
  - **Skill: GitHub Pages Deploy**: Automated deployment pipelines
  - **Skill: Text Selection Handler**: Browser-based text highlighting logic

### 6. Quality Assurance
- **Specification Compliance**: All implementations match specifications
- **Testing Strategy**: Unit tests for API, integration tests for RAG pipeline
- **Documentation**: Self-documenting code with comprehensive README
- **Version Control**: Git-based workflow with meaningful commits

## Project Boundaries

### In Scope
- ✅ AI-generated book content using Docusaurus
- ✅ RAG chatbot with full-book question answering
- ✅ Context-based questioning (selected text queries)
- ✅ OpenAI Agents SDK integration
- ✅ OpenAI ChatKit SDK for UI
- ✅ FastAPI backend API
- ✅ Qdrant Cloud vector database (free tier)
- ✅ GitHub Pages deployment
- ✅ Claude Code subagent architecture
- ✅ Reusable skill development
- ✅ Text selection functionality

### Out of Scope
- ❌ User authentication/accounts
- ❌ Persistent chat history storage
- ❌ Multi-language support
- ❌ Paid API tiers or premium features
- ❌ Mobile native applications
- ❌ Real-time collaboration features

## Success Criteria

### Project 1: AI-Driven Book
1. **Content Quality**: Coherent, well-structured book on a technical topic
2. **Navigation**: Intuitive Docusaurus sidebar and search
3. **Deployment**: Live on GitHub Pages with custom domain support
4. **Performance**: Page load times < 3 seconds

### Project 2: RAG Chatbot
1. **Accuracy**: Relevant answers with source citations
2. **Context Handling**: Successfully processes selected text queries
3. **Integration**: Embedded seamlessly in book pages
4. **Response Time**: API responses < 5 seconds for typical queries

### Bonus: Reusable Intelligence
1. **Subagents**: Minimum 3 specialized subagents documented and functional
2. **Skills**: Minimum 4 reusable skills with clear interfaces
3. **Matrix Demonstration**: Clear example of on-demand skill loading
4. **Documentation**: Comprehensive guide to extending the system

## Technical Constraints

### Infrastructure
- **Hosting**: GitHub Pages (static site hosting)
- **Backend**: Must run separately (Vercel/Railway/local for demo)
- **Database**: Qdrant Cloud free tier (1GB limit)
- **APIs**: OpenAI API (user provides key)

### Development Environment
- **Primary Tool**: Claude Code CLI
- **Language**: Python 3.10+ (backend), TypeScript (frontend enhancements)
- **Package Management**: pip/poetry (Python), npm/yarn (Node.js)
- **Version Control**: Git with conventional commits

### Cost Constraints
- **Zero Infrastructure Cost**: Free tiers only
- **API Costs**: User-provided OpenAI API keys
- **Scalability**: Design for free tier limits

## Workflow Integration

### Spec-Kit Plus Stages
1. **sp.constitution** ← Current stage: Establish principles ✓
2. **sp.specify**: Create detailed specifications for both projects
3. **sp.plan**: Break down into phases and dependencies
4. **sp.tasks**: Generate granular, actionable tasks
5. **sp.implement**: Execute with Claude Code

### Claude Code Workflow
```bash
# Initialize projects
claude-code init book-with-rag

# Create subagents
claude-code subagent create BookWriter
claude-code subagent create RAGEngineer
claude-code subagent create FrontendDev
claude-code subagent create APIBuilder

# Load skills (Matrix-style)
claude-code skill load docusaurus-setup
claude-code skill load qdrant-integration
claude-code skill load openai-agent-builder

# Execute with specifications
claude-code implement --spec specifications.md
```

## Risk Management

### Technical Risks
- **API Rate Limits**: Implement caching and retry logic
- **Vector DB Limits**: Monitor storage usage, implement chunking strategy
- **Deployment Complexity**: Separate static site from API backend
- **Integration Challenges**: Test OpenAI SDK compatibility thoroughly

### Mitigation Strategies
- Start with MVP features, add complexity incrementally
- Comprehensive error handling and user feedback
- Clear documentation for setup and deployment
- Fallback mechanisms for API failures

## Project Roles

### Human Responsibilities
- Define book topic and high-level structure
- Provide OpenAI API key for testing
- Review AI-generated specifications and code
- Make final decisions on architecture choices
- Test and validate final deliverables

### Claude Code Responsibilities
- Generate detailed specifications
- Implement all code based on specs
- Create and manage subagents
- Develop reusable skills
- Execute testing and debugging
- Generate documentation

### Subagent Responsibilities
- **BookWriter**: Content generation, structure, MDX formatting
- **RAG Engineer**: Vector database setup, embedding pipeline, retrieval logic
- **Frontend Developer**: Docusaurus customization, ChatKit integration
- **API Builder**: FastAPI endpoints, OpenAI Agents SDK integration

## Deliverables Checklist

### Core Deliverables
- [ ] Docusaurus-based book (10+ pages) deployed on GitHub Pages
- [ ] FastAPI backend with RAG endpoints
- [ ] Qdrant vector database populated with book content
- [ ] Embedded chatbot using OpenAI ChatKit SDK
- [ ] Full-book question answering functionality
- [ ] Selected-text question answering functionality
- [ ] Deployment documentation
- [ ] User guide for interacting with chatbot

### Bonus Deliverables
- [ ] Minimum 3 documented subagents
- [ ] Minimum 4 reusable skills with examples
- [ ] Matrix demonstration video/documentation
- [ ] Subagent and skill developer guide
- [ ] Architecture diagram showing intelligence flow

## Timeline Expectations

### Phase 1: Foundation (Day 1)
- Constitution finalized ✓
- Specifications created
- Project scaffolding initialized

### Phase 2: Book Development (Day 2)
- Content generation with BookWriter subagent
- Docusaurus setup and customization
- Initial GitHub Pages deployment

### Phase 3: RAG Implementation (Day 3)
- Qdrant setup and embedding pipeline
- FastAPI backend development
- OpenAI Agents SDK integration

### Phase 4: Integration (Day 4)
- ChatKit UI integration
- Text selection functionality
- End-to-end testing

### Phase 5: Polish & Bonus (Day 5+)
- Subagent documentation
- Skill library creation
- Final testing and refinement

## Next Steps

After constitution approval:
1. Run `sp.specify` to create detailed specifications
2. Define book topic and target audience
3. Set up development environment
4. Initialize Claude Code project
5. Create first subagent (BookWriter)

---

**Constitution Status**: ✅ Draft Complete - Pending Review
**Next Command**: `sp.specify` - Create baseline specification
**Estimated Project Duration**: 5-7 days
**Bonus Content Potential**: High (Subagents + Skills architecture)