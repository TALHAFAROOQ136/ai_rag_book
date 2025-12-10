# RAG Chatbot Backend

FastAPI backend for the AI-Driven Book RAG chatbot system.

## Features

- **RAG Pipeline**: Vector search + OpenAI Agents SDK
- **Streaming Responses**: Server-Sent Events for real-time answers
- **Multiple Endpoints**:
  - `POST /api/chat` - Non-streaming Q&A
  - `POST /api/chat/stream` - Streaming Q&A
  - `GET /api/health` - Health check
  - `POST /api/reindex` - Re-index book content

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required variables:
- `OPENAI_API_KEY` - Your OpenAI API key
- `QDRANT_URL` - Qdrant Cloud cluster URL
- `QDRANT_API_KEY` - Qdrant API key
- `BOOK_URL` - Deployed book URL for indexing

### 3. Run Locally

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. Test API

```bash
# Health check
curl http://localhost:8000/api/health

# Chat request
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?"}'
```

## Deployment

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── api/routes/          # API endpoints
│   ├── services/            # Business logic (TO BE IMPLEMENTED)
│   ├── models/              # Pydantic models
│   ├── config/              # Configuration
│   └── utils/               # Utilities
├── scripts/                  # CLI scripts (TO BE IMPLEMENTED)
├── tests/                    # Tests (TO BE IMPLEMENTED)
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
└── vercel.json               # Deployment config
```

## Status

**Phase 0**: ✅ Project structure and scaffolding complete  
**Phase 2**: ⏳ RAG pipeline implementation pending

## Next Steps

1. Implement vector search service (Phase 2.1-2.3)
2. Implement OpenAI Agent integration (Phase 2.4)
3. Complete chat endpoints (Phase 2.5)
4. Add tests (Phase 2.6)
5. Deploy to Vercel (Phase 2.7)
