# Backend Setup Guide

## Quick Start (5 minutes)

### Step 1: Get API Keys

#### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. **Cost**: ~$5-10 for testing (pay-as-you-go)

#### Qdrant Cloud (Free Tier)
1. Go to https://cloud.qdrant.io
2. Sign up for free account
3. Click "Create Cluster"
4. Choose **Free tier** (1GB storage)
5. Select region (us-east recommended)
6. Copy **Cluster URL** and **API Key** from dashboard

### Step 2: Configure Environment

Copy `.env.example` to `.env`:
```bash
cd backend
copy .env.example .env
```

Edit `.env` and add your keys:
```bash
OPENAI_API_KEY=sk-your-actual-openai-key-here
QDRANT_URL=https://your-cluster-id.us-east.aws.cloud.qdrant.io:6333
QDRANT_API_KEY=your-actual-qdrant-key-here
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Index Book Content

```bash
python scripts/index_book.py
```

This will:
- Read all markdown files from `../book/docs`
- Create embeddings for each chunk
- Upload to Qdrant

Expected output:
```
Processing: intro.md
  ✓ Indexed: 12 chunks
Processing: what-is-rag.md
  ✓ Indexed: 28 chunks
...
Files indexed: 13/13
Total chunks: 156
✓ Ready for RAG queries!
```

### Step 5: Start Backend Server

```bash
uvicorn app.main:app --reload
```

Server will start at: http://localhost:8000

### Step 6: Test the API

Open another terminal:
```bash
python tests/test_api.py
```

Or test manually:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?"}'
```

## API Endpoints

### Chat (Non-Streaming)
```bash
POST /api/chat
{
  "question": "What is RAG?",
  "top_k": 5,
  "chapter_filter": null
}
```

### Chat (Streaming)
```bash
POST /api/chat/stream
{
  "question": "Explain vector embeddings",
  "top_k": 3
}
```

### Chat with Selected Text
```bash
POST /api/chat/context
?question=Explain this
&selected_text=RAG combines retrieval...
&page_url=/intro
```

### Admin Endpoints

**Reindex Content**:
```bash
POST /api/admin/reindex
{
  "docs_path": "../book/docs",
  "background": false
}
```

**Collection Stats**:
```bash
GET /api/admin/collection/stats
```

**Clear Collection**:
```bash
DELETE /api/admin/collection
```

## Troubleshooting

### "No module named 'app'"
```bash
# Make sure you're in the backend directory
cd backend
# Install dependencies
pip install -r requirements.txt
```

### "OPENAI_API_KEY not found"
```bash
# Check .env file exists
ls .env

# Verify keys are set
cat .env | grep OPENAI_API_KEY
```

### "No relevant content found"
```bash
# Run indexing script
python scripts/index_book.py

# Check collection stats
curl http://localhost:8000/api/admin/collection/stats
```

### "Connection refused to Qdrant"
```bash
# Verify Qdrant URL and API key in .env
# Check Qdrant dashboard: https://cloud.qdrant.io
# Make sure cluster is running
```

## Cost Estimates

### OpenAI API
- **Embeddings**: ~$0.02 per 1M tokens
- **GPT-4o-mini**: ~$0.15 per 1M input tokens
- **Indexing 13 pages**: ~$0.05
- **100 queries**: ~$0.50
- **Monthly testing**: ~$5-10

### Qdrant Cloud
- **Free tier**: 1GB storage (FREE)
- **Enough for**: ~500,000 embeddings
- **Perfect for**: Learning and small projects

## Next Steps

1. ✅ Backend is running
2. ✅ Content is indexed
3. → Integrate frontend (Phase 3)
4. → Deploy to production

## Deployment Options

### Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd backend
vercel
```

### Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Deploy
railway init
railway up
```

### Docker
```bash
# Build
docker build -t ai-book-backend .

# Run
docker run -p 8000:8000 --env-file .env ai-book-backend
```

---

**Need help?** Check the logs or create an issue!
