# AI-Driven Book with RAG Chatbot

**An integrated system combining AI-generated documentation with intelligent question-answering capabilities**

![Project Status](https://img.shields.io/badge/status-Phase%200%20Complete-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🎯 Overview

This project demonstrates the Matrix-like concept of on-demand knowledge loading through:
- **AI-Generated Book**: Technical documentation built with Docusaurus
- **RAG Chatbot**: Intelligent Q&A powered by vector search and OpenAI Agents SDK
- **Subagent Architecture**: Four specialized Claude Code agents working autonomously
- **Reusable Skills**: Five modular, loadable capabilities

## 🏗️ Project Structure

```
ai-book-with-rag/
├── book/                   # Docusaurus project (AI-generated content)
├── backend/                # FastAPI + OpenAI Agents SDK
├── subagents/              # Four specialized agents
│   ├── BookWriter/
│   ├── RAGEngineer/
│   ├── FrontendDev/
│   └── APIBuilder/
├── skills/                 # Five reusable skills
│   ├── docusaurus-setup/
│   ├── qdrant-integration/
│   ├── openai-agent-builder/
│   ├── github-pages-deploy/
│   └── text-selection-handler/
├── data/                  # Vector database cache
├── specs/                 # Project specifications
├── .github/workflows/     # CI/CD automation
└── implementation-plan.md # Phased execution plan
```

## 📚 Documentation

- **[Constitution](./\.specify/memory/constitution.md)** - Project principles and vision
- **[Book Specification](./book.spec.md)** - Docusaurus book requirements
- **[RAG Specification](./rag.spec.md)** - Chatbot and backend requirements
- **[Subagents Specification](./subagents.spec.md)** - Agent roles and responsibilities
- **[Skills Specification](./skills.spec.md)** - Reusable skill modules
- **[Implementation Plan](./implementation-plan.md)** - Phased execution roadmap

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18.x or higher
- **Python** 3.10 or higher
- **OpenAI API Key** (for embeddings and chat)
- **Qdrant Cloud Account** (free tier)
- **GitHub Account** (for Pages deployment)

### Installation

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-book-with-rag
```

#### 2. Set Up Book (Frontend)

```bash
cd book
npm install
npm start  # Runs on http://localhost:3000
```

#### 3. Set Up Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn app.main:app --reload  # Runs on http://localhost:8000
```

### Environment Variables

Create `backend/.env` with:

```bash
OPENAI_API_KEY=sk-your-key
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-key
BOOK_URL=http://localhost:3000
```

## 🏃 Current Status

### ✅ Phase 0: Project Setup (Complete)

- [x] Repository structure created
- [x] Backend scaffolding (FastAPI with placeholder endpoints)
- [x] Book scaffolding (package.json, intro page)
- [x] Subagent documentation
- [x] Skills documentation
- [x] GitHub Actions workflows
- [x] Configuration templates

### ⏳ Next Steps: Phase 1 - Book Development

1. Initialize Docusaurus with FrontendDev subagent
2. Generate content with BookWriter subagent
3. Deploy to GitHub Pages

See [implementation-plan.md](./implementation-plan.md) for the complete roadmap.

## 🤖 Subagents

This project uses four specialized Claude Code subagents:

| Subagent | Role | Current Status |
|----------|------|----------------|
| **BookWriter** | Content generation and structure | ✅ Ready |
| **RAGEngineer** | Vector database and retrieval | ✅ Ready |
| **FrontendDev** | UI/UX and Docusaurus setup | ✅ Ready |
| **APIBuilder** | Backend API and AI integration | ✅ Ready |

## 🛠️ Skills

Five reusable, loadable skills:

1. **Docusaurus Setup** - Initialize documentation projects
2. **Qdrant Integration** - Vector database management
3. **OpenAI Agent Builder** - Conversational AI configuration
4. **GitHub Pages Deploy** - Automated deployment
5. **Text Selection Handler** - Browser text capture

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend (coming in Phase 1)
cd book
npm test
```

## 📦 Deployment

### Book (GitHub Pages)

Automatically deploys on push to `main` branch via GitHub Actions.

### Backend (Vercel)

```bash
cd backend
vercel
```

## 🎯 Features

### AI-Generated Book
- 10-15 pages of technical content
- Organized into 3-4 chapters
- Code examples with syntax highlighting
- Dark mode support
- Full-text search

### RAG Chatbot
- Context-aware question answering
- Source citations with page links
- Streaming responses
- Text selection for contextual queries
- Conversation memory

## 🔧 Technology Stack

**Frontend**:
- Docusaurus 3.x
- React 18.x
- TypeScript 5.x
- OpenAI ChatKit SDK (Phase 3)

**Backend**:
- FastAPI 0.110+
- OpenAI SDK 1.12+
- Qdrant Client 1.7+
- Python 3.10+

**Infrastructure**:
- GitHub Pages (book hosting)
- Vercel/Railway (backend hosting)
- Qdrant Cloud (vector database)

## 📊 Progress Tracking

**Total Progress**: Phase 0 Complete (20% of project)

| Phase | Status | Duration | Completion |
|-------|--------|----------|------------|
| Phase 0: Setup | ✅ Complete | 0.5 days | 100% |
| Phase 1: Book | ⏳ Pending | 1.5-2 days | 0% |
| Phase 2: Backend | ⏳ Pending | 2-3 days | 0% |
| Phase 3: Integration | ⏳ Pending | 1.5-2 days | 0% |
| Phase 4: Polish | ⏳ Pending | 1 day | 0% |

## 🤝 Contributing

This project is part of a hackathon/class project. Contributions are welcome after initial implementation is complete.

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **OpenAI** for GPT models and SDKs
- **Qdrant** for vector database
- **Docusaurus** for documentation framework
- **Claude Code** for AI-driven development

---

**Created**: 2025-12-10  
**Last Updated**: 2025-12-10  
**Version**: 0.1.0 (Phase 0 Complete)
# ai_rag_book
# ai_rag_book
# ai_rag_book
