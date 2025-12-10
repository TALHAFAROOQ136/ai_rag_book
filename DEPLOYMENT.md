# Complete Deployment Guide - GitHub Pages + Backend

## Overview

Is project mein **2 parts** hain jo deploy karne hain:
1. **Frontend (Book)** → GitHub Pages (Free)
2. **Backend (API)** → Vercel/Railway (Free tier available)

---

## Part 1: Frontend - GitHub Pages Deployment 📚

### Step 1: GitHub Repository Setup

```bash
# Navigate to project
cd e:/hackthon/hckathon I/class_project/ai_book

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Complete AI-driven book with RAG chatbot"

# Create repository on GitHub
# Go to: https://github.com/new
# Repository name: ai_book (or your choice)
# Public/Private: Your choice
# Don't initialize with README (we already have files)

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/ai_book.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Configure GitHub Pages

1. **Go to Repository Settings**
   - https://github.com/YOUR_USERNAME/ai_book/settings

2. **Navigate to Pages** (left sidebar)

3. **Configure Source**
   - Source: **GitHub Actions** (select from dropdown)
   - Save

### Step 3: Update Docusaurus Config

Book ke config mein apna GitHub username add karo:

**File**: `book/docusaurus.config.ts`

```typescript
const config: Config = {
  title: 'Introduction to RAG',
  tagline: 'Learn Retrieval-Augmented Generation',

  url: 'https://YOUR_USERNAME.github.io',  // ← Change this
  baseUrl: '/ai_book/',  // ← Your repo name

  organizationName: 'YOUR_USERNAME',  // ← Change this
  projectName: 'ai_book',  // ← Your repo name
  // ...
};
```

### Step 4: Trigger Deployment

```bash
# Make the config change
git add book/docusaurus.config.ts
git commit -m "Update config for GitHub Pages"
git push
```

GitHub Actions automatically run karegi aur site deploy ho jayegi!

**Check Progress**:
- Go to: https://github.com/YOUR_USERNAME/ai_book/actions
- Wait for green checkmark ✓

**Your Book URL**:
- https://YOUR_USERNAME.github.io/ai_book/

---

## Part 2: Backend Deployment 🚀

Backend ko alag host karna hoga kyunki GitHub Pages sirf static files support karta hai.

### Option A: Vercel (Recommended - Free)

**Why Vercel?**
- Free tier hai
- Python/FastAPI support hai
- Auto-deploys from GitHub
- Easy environment variables

**Steps**:

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy Backend**
   ```bash
   cd backend
   vercel
   ```

4. **Answer Prompts**:
   - Set up and deploy? **Y**
   - Which scope? (Your account)
   - Link to existing project? **N**
   - Project name? **ai-book-backend**
   - Directory? **./backend** (or just press Enter)

5. **Add Environment Variables**:
   ```bash
   vercel env add OPENAI_API_KEY
   # Paste your OpenAI key
   
   vercel env add QDRANT_URL
   # Paste your Qdrant URL
   
   vercel env add QDRANT_API_KEY
   # Paste your Qdrant key
   ```

6. **Redeploy with Environment Variables**:
   ```bash
   vercel --prod
   ```

**Your Backend URL**: `https://ai-book-backend.vercel.app`

### Option B: Railway (Alternative - Free Tier)

1. **Go to**: https://railway.app
2. **Sign up** with GitHub
3. **New Project** → **Deploy from GitHub repo**
4. **Select**: `ai_book` repository
5. **Root directory**: `/backend`
6. **Add Environment Variables** in Railway dashboard:
   - `OPENAI_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
7. **Deploy**

**Your Backend URL**: `https://your-app.up.railway.app`

---

## Part 3: Connect Frontend to Backend 🔗

### Update Frontend to Use Deployed Backend

**File**: `book/src/components/ChatBot/ChatBot.tsx`

Line 22 ko change karo:

```typescript
export const ChatBot: React.FC<ChatBotProps> = ({
  apiUrl = 'https://YOUR-BACKEND-URL.vercel.app',  // ← Change this!
  initialQuestion = '',
  isOpen = false,
  onClose
}) => {
```

**Example**:
```typescript
apiUrl = 'https://ai-book-backend.vercel.app',
```

### Update CORS Settings

Backend mein GitHub Pages URL add karo:

**File**: `backend/.env` (if deploying with environment variables)

```bash
CORS_ORIGINS=https://YOUR_USERNAME.github.io,http://localhost:3000
```

Or update in `backend/app/main.py` line 24:

```python
origins = [
    "https://YOUR_USERNAME.github.io",
    "http://localhost:3000",
]
```

### Redeploy Both

```bash
# Commit frontend changes
git add book/src/components/ChatBot/ChatBot.tsx
git commit -m "Connect to deployed backend"
git push

# Redeploy backend
cd backend
vercel --prod
```

---

## Part 4: Index Book Content in Production 📖

Backend deploy hone ke baad, book content index karna hoga:

### Option 1: Manual Indexing

```bash
# Local se production backend pe index karo
cd backend

# Temporary: Use production URL
export QDRANT_URL=your-production-qdrant-url
export QDRANT_API_KEY=your-production-key
export OPENAI_API_KEY=your-openai-key

python scripts/index_book.py --docs-path ../book/docs
```

### Option 2: API Endpoint Use Karo

Backend running hone ke baad:

```bash
curl -X POST https://YOUR-BACKEND-URL.vercel.app/api/admin/reindex \
  -H "Content-Type: application/json" \
  -d '{"docs_path": "./book/docs", "background": false}'
```

---

## Summary - Deployment Checklist ✅

### Initial Setup
- [ ] GitHub repository create karo
- [ ] Code push karo GitHub pe
- [ ] GitHub Pages enable karo (Actions source)
- [ ] Docusaurus config update karo

### Backend Deployment
- [ ] Vercel/Railway account banao
- [ ] Backend deploy karo
- [ ] Environment variables add karo
- [ ] Book content index karo

### Integration
- [ ] Frontend mein backend URL update karo
- [ ] CORS settings update karo
- [ ] Final push to GitHub
- [ ] Test live site!

---

## Testing Your Deployment 🧪

1. **Visit Frontend**: https://YOUR_USERNAME.github.io/ai_book/
2. **Click ChatBot**: Blue floating button
3. **Ask Question**: "What is RAG?"
4. **Check Sources**: Citations should appear

---

## Cost Summary 💰

- **GitHub Pages**: FREE ✅
- **Vercel Free Tier**: FREE ✅
- **Railway Free Tier**: FREE (500 hours/month) ✅
- **Qdrant Cloud**: FREE (1GB) ✅
- **OpenAI API**: ~$5-10/month (pay-as-you-go)

**Total Monthly Cost**: ~$5-10 (sirf OpenAI)

---

## Troubleshooting 🔧

### Frontend Not Loading?
- Check GitHub Actions status
- Verify `docusaurus.config.ts` URLs are correct
- Wait 2-3 minutes after push

### ChatBot Not Working?
- Check browser console for errors
- Verify backend URL in ChatBot.tsx
- Check backend is deployed and running
- Verify CORS settings

### Backend 500 Error?
- Check Vercel/Railway logs
- Verify environment variables are set
- Check Qdrant connection
- Verify OpenAI API key is valid

---

## Quick Deploy Commands (Summary)

```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push

# 2. Deploy Backend (Vercel)
cd backend
vercel --prod

# 3. Update frontend with backend URL
# Edit: book/src/components/ChatBot/ChatBot.tsx
git add book/src/components/ChatBot/ChatBot.tsx
git commit -m "Connect to production backend"
git push

# 4. Index content
curl -X POST https://YOUR-BACKEND.vercel.app/api/admin/reindex
```

**Done! Your AI book is live!** 🎉

---

**Need help with any step? Let me know!** 🚀
