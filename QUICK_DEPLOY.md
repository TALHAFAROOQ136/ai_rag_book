# Quick Deployment Guide for TALHAFAROOQ136

## ✅ Pre-configured for Your GitHub Account!

All config files updated with your GitHub username: **TALHAFAROOQ136**

---

## Step 1: Push to GitHub (5 minutes)

```bash
cd "e:/hackthon/hckathon I/class_project/ai_book"

# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "Complete AI-driven book with RAG chatbot"

# Create new repository on GitHub:
# Go to: https://github.com/TALHAFAROOQ136?tab=repositories
# Click: "New" button
# Repository name: ai_book
# Public ✓
# Don't add README, .gitignore, or license (we have these)

# Add remote (replace after creating repo)
git remote add origin https://github.com/TALHAFAROOQ136/ai_book.git

# Push
git branch -M main
git push -u origin main
```

---

## Step 2: Enable GitHub Pages (2 minutes)

1. Go to: https://github.com/TALHAFAROOQ136/ai_book/settings/pages

2. Under "Build and deployment":
   - **Source**: GitHub Actions (select from dropdown)

3. Click **Save**

4. Wait 2-3 minutes for deployment

5. Your site will be live at:
   **https://TALHAFAROOQ136.github.io/ai_book/**

---

## Step 3: Deploy Backend (10 minutes)

### Option A: Vercel (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy backend
cd backend
vercel

# Follow prompts:
# - Link to existing project? N
# - Project name: ai-book-backend
# - Which directory? ./ (press Enter)

# Add environment variables
vercel env add OPENAI_API_KEY
# Paste your OpenAI key: sk-...

vercel env add QDRANT_URL
# Paste Qdrant URL: https://...

vercel env add QDRANT_API_KEY
# Paste Qdrant key

# Deploy to production
vercel --prod
```

**Your backend URL**: Copy the production URL from output

### Option B: Railway

1. Go to: https://railway.app
2. Sign in with GitHub
3. New Project → Deploy from GitHub repo
4. Select: `TALHAFAROOQ136/ai_book`
5. Root directory: `/backend`
6. Add environment variables in dashboard
7. Deploy

---

## Step 4: Connect Frontend to Backend (3 minutes)

Edit: `book/src/components/ChatBot/ChatBot.tsx`

Line 22, replace with YOUR backend URL:

```typescript
export const ChatBot: React.FC<ChatBotProps> = ({
  apiUrl = 'https://YOUR-BACKEND-URL.vercel.app',  // ← Paste your URL here
  initialQuestion = '',
  isOpen = false,
  onClose
}) => {
```

Example:
```typescript
apiUrl = 'https://ai-book-backend-abc123.vercel.app',
```

Then push:
```bash
git add book/src/components/ChatBot/ChatBot.tsx
git commit -m "Connect to production backend"
git push
```

---

## Step 5: Index Book Content (5 minutes)

After backend is deployed, index the book:

```bash
curl -X POST https://YOUR-BACKEND-URL.vercel.app/api/admin/reindex \
  -H "Content-Type: application/json" \
  -d '{"docs_path": "../book/docs", "background": false}'
```

Or locally:
```bash
cd backend
python scripts/index_book.py
```

---

## ✅ Done! Test Your Site

1. **Visit**: https://TALHAFAROOQ136.github.io/ai_book/
2. **Open ChatBot**: Click blue floating button
3. **Ask Question**: "What is RAG?"
4. **Check Sources**: Should show citations

---

## Deployment Checklist

- [ ] Push code to GitHub
- [ ] Enable GitHub Pages (Actions source)
- [ ] Deploy backend to Vercel/Railway
- [ ] Add environment variables
- [ ] Update ChatBot with backend URL
- [ ] Push frontend changes
- [ ] Index book content
- [ ] Test live site!

---

## Your URLs

- **Frontend**: https://TALHAFAROOQ136.github.io/ai_book/
- **Backend**: (You'll get this after Vercel deployment)
- **GitHub Repo**: https://github.com/TALHAFAROOQ136/ai_book

---

## Cost

- GitHub Pages: **FREE** ✅
- Vercel: **FREE tier** ✅
- Qdrant: **FREE (1GB)** ✅
- OpenAI: ~$5-10/month

---

## Need Help?

Check `DEPLOYMENT.md` for detailed troubleshooting!

**Good luck! 🚀**
