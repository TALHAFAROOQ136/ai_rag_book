# Feature Specification: RAG Chatbot with OpenAI Agents SDK

**Project**: AI-Driven Book with RAG Chatbot  
**Created**: 2025-12-09  
**Status**: Draft - Implementation Ready  
**Project 2 of 2**: Intelligent Question-Answering System

## Executive Summary

Build a Retrieval-Augmented Generation (RAG) chatbot that provides intelligent answers to questions about the AI-generated book content. The system combines OpenAI's Agents SDK for conversational AI, FastAPI for the backend API, Qdrant Cloud for vector storage, and OpenAI's ChatKit SDK for the embedded UI. This creates a seamless, context-aware question-answering experience integrated directly into the book pages.

---

## User Scenarios & Testing

### User Story 1 - User Asks Questions About Book Content (Priority: P1)

A reader clicks the chatbot icon while reading the book, types a question about the content, and receives an accurate answer with citations to specific book sections.

**Why this priority**: This is the core value proposition - enabling readers to interactively explore the book content.

**Independent Test**: Open any book page, click chat icon, ask "What is [main topic]?", verify answer includes source citations, confirm answer is factually correct based on book content.

**Acceptance Scenarios**:

1. **Given** a user is on any book page, **When** they click the chatbot icon, **Then** a chat interface appears within 1 second
2. **Given** the chat interface is open, **When** the user types a question and presses enter, **Then** a response begins streaming within 3 seconds
3. **Given** the chatbot provides an answer, **When** the answer is displayed, **Then** it includes citations to specific book pages/sections
4. **Given** the user clicks a citation link, **When** the link is activated, **Then** the page scrolls to the exact referenced section
5. **Given** the answer is generated, **When** reviewing its content, **Then** it accurately reflects information from the book (no hallucination)

---

### User Story 2 - User Asks Questions About Selected Text (Priority: P1)

A reader highlights specific text on a book page, right-clicks or uses a button to ask "Explain this," and receives a contextual answer specifically about the selected passage.

**Why this priority**: Context-aware questioning dramatically improves user experience and demonstrates advanced RAG capabilities.

**Independent Test**: Select a paragraph, trigger "Ask about selection" action, verify question includes selected text context, confirm answer is specifically about that passage.

**Acceptance Scenarios**:

1. **Given** a user is reading a page, **When** they highlight text and click "Ask about this", **Then** the chatbot opens with the selected text pre-populated as context
2. **Given** the selected text is sent as context, **When** the user asks a question, **Then** the answer prioritizes the selected passage in its response
3. **Given** the user asks "Explain this" on selected text, **When** the answer is generated, **Then** it specifically elaborates on the selected passage
4. **Given** the selection contains code, **When** asking about it, **Then** the chatbot understands it as code and provides technical explanations
5. **Given** the user selects text from multiple paragraphs, **When** asking a question, **Then** the full selection context is preserved

---

### User Story 3 - User Has Multi-Turn Conversation (Priority: P2)

A reader asks an initial question, receives an answer, then asks follow-up questions that reference previous messages, creating a natural conversation flow.

**Why this priority**: Conversational memory significantly improves usability, allowing users to dig deeper without repeating context.

**Independent Test**: Ask initial question "What is RAG?", get response, then ask "How does it differ from traditional search?" without repeating "RAG", verify chatbot understands reference.

**Acceptance Scenarios**:

1. **Given** a user has asked a question and received an answer, **When** they ask a follow-up using pronouns ("it", "that", "this"), **Then** the chatbot correctly resolves the reference
2. **Given** a conversation has 3+ messages, **When** asking question 4, **Then** the chatbot maintains context from all previous messages
3. **Given** a user wants to start fresh, **When** they click "New conversation", **Then** the chat history clears and context resets
4. **Given** a conversation is active, **When** the user navigates to a different book page, **Then** [NEEDS CLARIFICATION: Should conversation persist or reset? Recommendation: persist]

---

### User Story 4 - User Receives Fast, Streaming Responses (Priority: P2)

When a user asks a question, the answer begins appearing immediately (streaming) rather than waiting for the complete response, improving perceived performance.

**Why this priority**: Streaming responses dramatically improve user experience, making the chatbot feel responsive and interactive.

**Independent Test**: Ask a question that requires a long answer (200+ words), verify first words appear within 2 seconds, measure total time to complete.

**Acceptance Scenarios**:

1. **Given** a user submits a question, **When** the API begins responding, **Then** the first tokens appear in the UI within 2 seconds
2. **Given** an answer is streaming, **When** tokens arrive, **Then** the UI updates smoothly with no flickering or layout shifts
3. **Given** a long answer is being generated, **When** the user scrolls the chat, **Then** new tokens continue to appear at the bottom
4. **Given** the user changes their mind, **When** they click "Stop generation", **Then** the stream halts immediately

---

### User Story 5 - System Handles Errors Gracefully (Priority: P2)

When API limits are hit, network fails, or questions are unanswerable, the system provides clear error messages and fallback options.

**Why this priority**: Graceful error handling maintains user trust and prevents frustration.

**Independent Test**: Disconnect network, ask question, verify error message. Ask nonsensical question, verify helpful response. Hit rate limit (simulate), verify clear message.

**Acceptance Scenarios**:

1. **Given** the API is unreachable, **When** a user asks a question, **Then** an error message appears: "Unable to connect. Please check your connection."
2. **Given** the question is outside book content, **When** the chatbot cannot find relevant information, **Then** it responds: "I couldn't find information about that in this book. Try rephrasing or asking about [topic]."
3. **Given** the API rate limit is exceeded, **When** the next request is made, **Then** the error message includes estimated wait time
4. **Given** an error occurs, **When** the user clicks "Retry", **Then** the system attempts the request again
5. **Given** the Qdrant database is empty, **When** a question is asked, **Then** a setup error message appears: "Knowledge base not initialized. Contact administrator."

---

### Edge Cases

- **What happens when the user asks a question before the vector database is populated?** → Clear error message: "Knowledge base is being initialized. Please try again in a few minutes."
- **How does the system handle very long questions (>1000 characters)?** → Truncate with warning: "Question trimmed to 1000 characters"
- **What if the selected text is extremely long (entire page)?** → Use only first 500 words + last 100 words as context
- **How does chatbot handle multiple chat windows open simultaneously?** → Each window maintains independent state (or sync via session ID)
- **What if the book content changes after vector DB is populated?** → Provide re-indexing script/workflow
- **How does system handle code blocks in questions or answers?** → Preserve formatting, apply syntax highlighting
- **What if user's OpenAI API key is invalid or expired?** → Clear error: "API key invalid. Please update configuration."

---

## Requirements

### Functional Requirements

#### Vector Database & Embedding Pipeline

- **FR-001**: System MUST extract all text content from the deployed Docusaurus book (HTML scraping or build-time extraction)
- **FR-002**: System MUST chunk the extracted text into semantically meaningful segments (500-1000 tokens each with 100-token overlap)
- **FR-003**: System MUST generate embeddings for each chunk using OpenAI's text-embedding-3-small model
- **FR-004**: System MUST store embeddings in Qdrant Cloud with metadata (page title, URL, section heading)
- **FR-005**: System MUST create a Qdrant collection with appropriate vector dimensions (1536 for text-embedding-3-small)
- **FR-006**: System MUST implement incremental indexing (ability to update specific pages without re-indexing entire book)
- **FR-007**: System MUST handle indexing failures gracefully (log errors, retry failed chunks)

#### Backend API (FastAPI)

- **FR-008**: System MUST expose a POST /api/chat endpoint accepting { question: string, context?: string, conversation_id?: string }
- **FR-009**: System MUST expose a POST /api/chat/stream endpoint for streaming responses (Server-Sent Events)
- **FR-010**: System MUST implement vector search to retrieve top 5 most relevant chunks for each question
- **FR-011**: System MUST construct RAG prompt combining retrieved chunks + user question + conversation history (last 5 messages)
- **FR-012**: System MUST integrate OpenAI Agents SDK to generate responses using gpt-4o-mini (or configurable model)
- **FR-013**: System MUST include source citations in responses (page URLs and section titles)
- **FR-014**: System MUST maintain conversation history per session (in-memory or database, configurable)
- **FR-015**: System MUST expose GET /api/health endpoint for health checks
- **FR-016**: System MUST expose POST /api/reindex endpoint (admin-only) to trigger re-indexing
- **FR-017**: System MUST implement CORS to allow requests from GitHub Pages domain
- **FR-018**: System MUST validate API rate limits and return appropriate HTTP status codes (429 for rate limit)
- **FR-019**: System MUST log all requests with timestamps, question text (anonymized option), and response times

#### Frontend Integration (ChatKit SDK)

- **FR-020**: System MUST embed OpenAI ChatKit UI component into Docusaurus pages via custom plugin
- **FR-021**: System MUST provide a floating chat button (bottom-right corner) on all book pages
- **FR-022**: System MUST implement click handler to open/close chat interface
- **FR-023**: System MUST connect ChatKit to the FastAPI backend URL (configurable in Docusaurus config)
- **FR-024**: System MUST implement text selection handler that captures highlighted text
- **FR-025**: System MUST provide "Ask about selection" button or context menu when text is selected
- **FR-026**: System MUST pre-populate chat with selected text when "Ask about selection" is triggered
- **FR-027**: System MUST display chat history within the session (persist in sessionStorage)
- **FR-028**: System MUST implement "New conversation" button to clear history
- **FR-029**: System MUST display loading indicators during API calls
- **FR-030**: System MUST display error messages in the chat UI (not just console)
- **FR-031**: System MUST render Markdown in chatbot responses (formatting, code blocks, links)
- **FR-032**: System MUST make citation links clickable (navigate to source page/section)

#### OpenAI Agents SDK Integration

- **FR-033**: System MUST configure an OpenAI Agent with system prompt defining its role as book Q&A assistant
- **FR-034**: System MUST pass retrieved chunks as context to the agent
- **FR-035**: System MUST implement streaming capability for agent responses
- **FR-036**: System MUST handle agent errors (model failures, timeout) with fallback messages
- **FR-037**: System MUST configure agent temperature (0.3 recommended for factual answers)
- **FR-038**: System MUST implement token counting to stay within context limits (8k tokens for gpt-4o-mini)

---

### Non-Functional Requirements

- **NFR-001**: API response time (non-streaming) MUST be under 5 seconds for p95 of requests
- **NFR-002**: First token latency (streaming) MUST be under 2 seconds for p95 of requests
- **NFR-003**: Vector search retrieval MUST complete within 500ms
- **NFR-004**: System MUST support at least 10 concurrent users (free tier limitation acknowledged)
- **NFR-005**: Qdrant collection MUST stay within 1GB free tier limit (approximately 50,000-100,000 chunks)
- **NFR-006**: System MUST handle OpenAI API rate limits gracefully (retry with exponential backoff)
- **NFR-007**: Chat UI MUST work on mobile devices with touch interactions
- **NFR-008**: System MUST be deployable on free hosting tiers (Vercel/Railway/local)
- **NFR-009**: Backend MUST be stateless (conversation state in request or external store)

---

### Key Entities

- **Chunk**: A segment of book text with embeddings
  - Attributes: chunk_id, text, embedding_vector, page_url, page_title, section_heading, token_count
  - Relationships: Belongs to Page, stored in VectorDatabase

- **VectorDatabase**: Qdrant collection
  - Attributes: collection_name, vector_dimensions, distance_metric, indexed_count
  - Relationships: Contains Chunks

- **Conversation**: A session of Q&A between user and chatbot
  - Attributes: conversation_id, messages[], created_at, last_updated
  - Relationships: Contains Messages

- **Message**: A single question or answer
  - Attributes: message_id, role (user/assistant), content, timestamp, sources[]
  - Relationships: Belongs to Conversation, references Chunks (for citations)

- **ChatAgent**: OpenAI agent instance
  - Attributes: model_name, system_prompt, temperature, max_tokens
  - Relationships: Generates Messages

- **APIClient**: FastAPI application
  - Attributes: base_url, cors_origins, api_key
  - Relationships: Connects to VectorDatabase, ChatAgent

---

## Technical Specifications

### Technology Stack

- **Backend Framework**: FastAPI 0.110+
- **AI Agent**: OpenAI Agents SDK (Swarm framework)
- **Vector Database**: Qdrant Cloud (free tier)
- **Embeddings**: OpenAI text-embedding-3-small (1536 dimensions)
- **LLM**: OpenAI gpt-4o-mini (configurable to gpt-4o)
- **Frontend SDK**: OpenAI ChatKit SDK (React component)
- **Languages**: Python 3.10+ (backend), TypeScript (frontend integration)
- **Deployment**: Vercel/Railway (backend), GitHub Pages (frontend)

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                          │
│  ┌────────────────────────────────────────────────────┐    │
│  │       Docusaurus Book (GitHub Pages)                │    │
│  │  ┌──────────────────────────────────────────────┐  │    │
│  │  │  ChatKit UI Component                        │  │    │
│  │  │  - Floating chat button                      │  │    │
│  │  │  - Text selection handler                    │  │    │
│  │  │  - Message display / input                   │  │    │
│  │  └──────────────┬───────────────────────────────┘  │    │
│  └─────────────────┼──────────────────────────────────┘    │
└────────────────────┼─────────────────────────────────────────┘
                     │ HTTPS
                     │ POST /api/chat/stream
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Vercel/Railway)                │
│  ┌────────────────────────────────────────────────────┐    │
│  │  API Endpoints                                      │    │
│  │  - /api/chat (non-streaming)                       │    │
│  │  - /api/chat/stream (SSE)                          │    │
│  │  - /api/health                                     │    │
│  │  - /api/reindex                                    │    │
│  └────────┬──────────────────────────────┬────────────┘    │
│           │                               │                  │
│           ▼                               ▼                  │
│  ┌────────────────┐           ┌──────────────────────┐     │
│  │ Vector Search  │           │  OpenAI Agents SDK   │     │
│  │   Module       │           │   (Swarm)            │     │
│  │                │           │  - gpt-4o-mini       │     │
│  │ Retrieve top-5 │           │  - Streaming         │     │
│  │   chunks       │           │  - Context builder   │     │
│  └────────┬───────┘           └──────────┬───────────┘     │
└───────────┼──────────────────────────────┼──────────────────┘
            │                               │
            ▼                               ▼
┌─────────────────────┐         ┌──────────────────────┐
│  Qdrant Cloud       │         │  OpenAI API          │
│  - Vector storage   │         │  - Embeddings        │
│  - Similarity search│         │  - Chat completions  │
│  - Metadata filter  │         │  - Streaming         │
└─────────────────────┘         └──────────────────────┘
```

### Data Flow

#### 1. Indexing Pipeline (One-time/Update)

```
Book Content (HTML)
  ├─> Scrape/Extract text
  ├─> Chunk text (500-1000 tokens, 100 overlap)
  ├─> Generate metadata (page URL, title, section)
  ├─> Create embeddings (OpenAI API)
  └─> Store in Qdrant (vector + metadata)
```

#### 2. Query Pipeline (Real-time)

```
User Question
  ├─> Embed question (OpenAI API)
  ├─> Vector search in Qdrant (top-5 chunks)
  ├─> Construct RAG prompt:
  │    - System: "You are a Q&A assistant for [book]..."
  │    - Context: Retrieved chunks
  │    - History: Last 5 messages
  │    - User: Question
  ├─> Send to OpenAI Agent (Swarm)
  ├─> Stream response tokens
  └─> Return with citations
```

### Project Structure

```
rag-backend/
├── app/
│   ├── main.py                 # FastAPI app entry
│   ├── api/
│   │   ├── routes/
│   │   │   ├── chat.py         # Chat endpoints
│   │   │   ├── health.py       # Health check
│   │   │   └── admin.py        # Reindex endpoint
│   │   └── middleware/
│   │       └── cors.py         # CORS configuration
│   ├── services/
│   │   ├── embedding.py        # OpenAI embedding generation
│   │   ├── vector_search.py    # Qdrant search logic
│   │   ├── agent.py            # OpenAI Agents SDK integration
│   │   └── indexing.py         # Content chunking & indexing
│   ├── models/
│   │   ├── chat.py             # Pydantic models (ChatRequest, ChatResponse)
│   │   └── chunk.py            # Chunk data model
│   ├── config/
│   │   ├── settings.py         # Environment variables
│   │   └── prompts.py          # System prompts
│   └── utils/
│       ├── text_chunker.py     # Text chunking utilities
│       └── logger.py           # Logging setup
├── scripts/
│   ├── index_book.py           # CLI script to index book content
│   └── test_rag.py             # RAG pipeline testing
├── tests/
│   ├── test_api.py
│   ├── test_vector_search.py
│   └── test_agent.py
├── requirements.txt
├── .env.example
├── Dockerfile (optional)
├── vercel.json (if deploying to Vercel)
└── README.md

book-frontend/ (Docusaurus integration)
├── src/
│   ├── components/
│   │   └── ChatBot/
│   │       ├── ChatBot.tsx         # ChatKit integration
│   │       ├── FloatingButton.tsx  # Chat button
│   │       └── TextSelector.tsx    # Selection handler
│   └── theme/
│       └── Root.tsx                # App-level wrapper
├── static/
│   └── chatbot-config.js           # Backend URL config
└── docusaurus.config.ts            # Plugin configuration
```

### API Specifications

#### POST /api/chat

**Request Body:**
```json
{
  "question": "What is retrieval-augmented generation?",
  "context": "Optional selected text...",
  "conversation_id": "uuid-v4",
  "model": "gpt-4o-mini"  // optional
}
```

**Response:**
```json
{
  "answer": "Retrieval-augmented generation (RAG) is...",
  "sources": [
    {
      "page_title": "Chapter 2: Core Concepts",
      "page_url": "https://yourusername.github.io/book/chapter-2/rag-intro",
      "section": "What is RAG?",
      "relevance_score": 0.92
    }
  ],
  "conversation_id": "uuid-v4",
  "tokens_used": 856
}
```

#### POST /api/chat/stream

**Request Body:** (same as /api/chat)

**Response:** Server-Sent Events (SSE)
```
event: token
data: {"content": "Retrieval"}

event: token
data: {"content": "-augmented"}

event: sources
data: {"sources": [...]}

event: done
data: {"tokens_used": 856}
```

#### POST /api/reindex

**Request Body:**
```json
{
  "pages": ["https://book.com/page1", "https://book.com/page2"],  // optional
  "full_reindex": false
}
```

**Response:**
```json
{
  "status": "success",
  "chunks_indexed": 1247,
  "pages_processed": 12,
  "duration_seconds": 45.3
}
```

### Configuration

#### Backend .env

```env
# OpenAI
OPENAI_API_KEY=sk-...

# Qdrant
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-api-key
QDRANT_COLLECTION_NAME=book_chunks

# API
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://yourusername.github.io,http://localhost:3000

# Agent
MODEL_NAME=gpt-4o-mini
TEMPERATURE=0.3
MAX_TOKENS=2000

# Indexing
CHUNK_SIZE=800
CHUNK_OVERLAP=100
BOOK_URL=https://yourusername.github.io/book
```

#### Frontend (docusaurus.config.ts)

```typescript
module.exports = {
  // ... other config
  customFields: {
    chatbotApiUrl: process.env.CHATBOT_API_URL || 'https://your-backend.vercel.app'
  }
}
```

### Text Selection Implementation

#### JavaScript/TypeScript Handler

```typescript
// src/components/ChatBot/TextSelector.tsx
export function useTextSelection() {
  const [selectedText, setSelectedText] = useState('');
  
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection?.toString().trim();
      if (text && text.length > 10) {
        setSelectedText(text);
        // Show "Ask about this" button
      }
    };
    
    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);
  
  return { selectedText, clearSelection: () => setSelectedText('') };
}
```

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: System correctly answers 90%+ of questions that can be answered from book content (validated with test question set)
- **SC-002**: System provides relevant source citations for 100% of answers
- **SC-003**: First token appears within 2 seconds for 95% of requests
- **SC-004**: Complete answers are generated within 5 seconds for 90% of requests
- **SC-005**: Vector search retrieval completes within 500ms for 99% of queries
- **SC-006**: Text selection handler captures highlighted text with 100% accuracy
- **SC-007**: Citation links navigate to correct page/section 100% of the time
- **SC-008**: System gracefully handles errors with user-friendly messages (no raw errors shown)
- **SC-009**: Chatbot maintains conversation context correctly for multi-turn conversations (4+ messages)
- **SC-010**: System stays within Qdrant free tier limits (1GB storage)
- **SC-011**: API responds with appropriate HTTP status codes (200, 400, 429, 500)
- **SC-012**: Chat UI works on mobile devices (tested on 3+ screen sizes)

---

## Acceptance Criteria

### Definition of Done

#### Backend
- [ ] FastAPI application running with all endpoints functional
- [ ] Qdrant Cloud collection created and populated with book embeddings
- [ ] OpenAI Agents SDK integrated with working streaming
- [ ] Vector search returns relevant chunks (manual testing with sample questions)
- [ ] Conversation history maintained across multi-turn conversations
- [ ] CORS configured to allow frontend requests
- [ ] Error handling implemented for all failure scenarios
- [ ] Logging configured with request/response tracking
- [ ] Health check endpoint returns 200 with system status
- [ ] Deployed to Vercel/Railway (or runnable locally)
- [ ] Environment variables configured properly
- [ ] API documentation (README or Swagger/OpenAPI)

#### Frontend Integration
- [ ] ChatKit SDK installed and configured
- [ ] Floating chat button appears on all book pages
- [ ] Chat interface opens/closes correctly
- [ ] Text selection handler captures highlighted text
- [ ] "Ask about selection" button appears when text is selected
- [ ] Selected text is sent as context to API
- [ ] Messages display with proper formatting (Markdown rendering)
- [ ] Source citations are clickable and navigate correctly
- [ ] Loading indicators show during API calls
- [ ] Error messages display in chat UI
- [ ] "New conversation" button clears chat history
- [ ] Chat state persists within browser session
- [ ] Mobile-responsive design tested

#### Indexing Pipeline
- [ ] Content extraction script successfully scrapes all book pages
- [ ] Text chunking produces appropriate chunk sizes (500-1000 tokens)
- [ ] Embeddings generated for all chunks
- [ ] Metadata (URL, title, section) correctly stored
- [ ] Re-indexing script works for individual pages
- [ ] Indexing errors logged and handled gracefully

### Test Plan

#### 1. Unit Tests

```python
# tests/test_vector_search.py
def test_vector_search_returns_relevant_chunks():
    question = "What is RAG?"
    chunks = vector_search(question, top_k=5)
    assert len(chunks) == 5
    assert all(chunk.relevance_score > 0.5 for chunk in chunks)

# tests/test_text_chunker.py
def test_chunking_respects_token_limits():
    long_text = "..." * 10000
    chunks = chunk_text(long_text, max_tokens=800, overlap=100)
    assert all(token_count(chunk) <= 800 for chunk in chunks)
```

#### 2. Integration Tests

- Test full RAG pipeline: question → search → agent → response
- Test streaming responses
- Test conversation history persistence
- Test error scenarios (API failures, network issues)

#### 3. Manual Testing

**Test Question Set** (validate against book content):
1. "What is the main topic of this book?"
2. "Explain [specific concept from Chapter 2]"
3. "How does [concept A] differ from [concept B]?"
4. "Give me an example of [topic]"
5. "What are the prerequisites for [topic]?"

**Text Selection Tests**:
1. Select single paragraph → ask "Summarize this"
2. Select code block → ask "Explain this code"
3. Select multiple paragraphs → verify context is preserved

**Conversation Tests**:
1. Ask initial question
2. Ask follow-up using pronouns ("it", "that")
3. Ask 4+ related questions
4. Start new conversation
5. Verify context reset

#### 4. Performance Testing

- Measure API latency under load (10 concurrent requests)
- Test with long questions (500+ words)
- Test with complex selected text (multiple code blocks)
- Measure time-to-first-token

#### 5. Error Scenario Testing

- Disconnect network → verify error message
- Use invalid API key → verify error handling
- Empty Qdrant database → verify initialization error
- Rate limit exceeded → verify retry logic

---

## Dependencies

### External Dependencies

- **OpenAI API Key**: Required for embeddings and chat completions (user-provided)
- **Qdrant Cloud Account**: Free tier sign-up required
- **Hosting Platform**: Vercel/Railway account (free tier) or local machine
- **Book Deployment**: Requires completed Project 1 (AI-Driven Book)

### Internal Dependencies (from other specs)

- **RAGEngineer Subagent**: For vector database setup and retrieval logic (see subagents.spec.md)
- **APIBuilder Subagent**: For FastAPI backend implementation (see subagents.spec.md)
- **FrontendDev Subagent**: For ChatKit integration (see subagents.spec.md)
- **Qdrant Integration Skill**: For vector database operations (see skills.spec.md)
- **OpenAI Agent Builder Skill**: For Swarm agent configuration (see skills.spec.md)
- **Text Selection Handler Skill**: For text highlighting logic (see skills.spec.md)

### Python Dependencies (requirements.txt)

```
fastapi==0.110.0
uvicorn[standard]==0.27.0
openai==1.12.0
swarm-openai==0.1.0  # OpenAI Agents SDK
qdrant-client==1.7.0
pydantic==2.6.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
httpx==0.26.0
tiktoken==0.5.2  # Token counting
beautifulsoup4==4.12.0  # HTML parsing for indexing
aiohttp==3.9.0  # Async HTTP
tenacity==8.2.3  # Retry logic
```

### Frontend Dependencies (package.json)

```json
{
  "dependencies": {
    "@openai/chatkit": "^1.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
```

---

## Risks and Mitigation

### Risk 1: Vector Search Returns Irrelevant Chunks
- **Impact**: Poor answer quality, user frustration
- **Mitigation**: 
  - Fine-tune chunk size and overlap
  - Implement hybrid search (vector + keyword)
  - Add relevance score threshold filtering
  - Test with diverse question set

### Risk 2: OpenAI API Costs Exceed Budget
- **Impact**: Unsustainable operation
- **Mitigation**:
  - Use gpt-4o-mini (cheaper than gpt-4o)
  - Implement request caching for common questions
  - Set daily usage limits
  - Monitor token usage via dashboard

### Risk 3: Qdrant Free Tier Limit Exceeded
- **Impact**: System stops working when 1GB limit hit
- **Mitigation**:
  - Monitor collection size
  - Optimize chunk size to reduce storage
  - Implement selective indexing (only key pages)
  - Document upgrade path to paid tier

### Risk 4: CORS Issues Between GitHub Pages and Backend
- **Impact**: Frontend cannot call backend API
- **Mitigation**:
  - Configure CORS properly in FastAPI
  - Test with actual deployed URLs (not just localhost)
  - Consider proxy setup if needed

### Risk 5: Chatbot Hallucinates Information
- **Impact**: Incorrect answers damage credibility
- **Mitigation**:
  - Set low temperature (0.3)
  - Strong system prompt emphasizing accuracy
  - Always include source citations
  - Implement answer validation (check if answer references retrieved chunks)

### Risk 6: Streaming Responses Fail on Some Browsers
- **Impact**: Degraded user experience
- **Mitigation**:
  - Implement graceful fallback to non-streaming
  - Test on multiple browsers (Chrome, Firefox, Safari, Edge)
  - Use polyfills for SSE if needed

---

## Open Questions

1. **Backend Hosting**: Should we deploy to Vercel, Railway, or provide Docker setup for local hosting? (Recommendation: Vercel for simplicity)
2. **Conversation Persistence**: Should conversation history persist across page navigations? (Recommendation: Yes, using sessionStorage)
3. **Model Selection**: Should users be able to choose between gpt-4o-mini and gpt-4o? (Recommendation: No, fixed to gpt-4o-mini for cost control)
4. **Authentication**: Should the chatbot be publicly accessible or require authentication? (Recommendation: Public for demo purposes)
5. **Analytics**: Should we track usage metrics (questions asked, topics queried)? (Recommendation: Yes, anonymized logging)
6. **Hybrid Search**: Should we implement keyword search alongside vector search? (Recommendation: Start with vector-only, add if needed)
7. **Admin Interface**: Should there be a web UI for re-indexing, or just a CLI script? (Recommendation: CLI script only for MVP)

---

## Next Steps

1. **Set Up Qdrant Cloud**: Create account, create collection, get API key
2. **Set Up OpenAI API**: Obtain API key, test embeddings and chat endpoints
3. **Implement Indexing Pipeline**: Extract book content, chunk, embed, store
4. **Build FastAPI Backend**: Implement all endpoints, integrate Agents SDK
5. **Deploy Backend**: Deploy to Vercel/Railway
6. **Integrate ChatKit**: Add to Docusaurus, connect to backend
7. **Test End-to-End**: Validate all user scenarios
8. **Optimize and Refine**: Improve chunk relevance, tune prompts, enhance UI

---

**Specification Status**: ✅ Implementation Ready (pending clarifications on open questions)  
**Estimated Implementation Time**: 2-3 days  
**Priority**: P1 (Core project deliverable, depends on Project 1)
