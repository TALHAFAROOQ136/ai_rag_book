---
id: prerequisites
title: Prerequisites
sidebar_position: 3
---

# Prerequisites

Before diving into RAG implementation, let's ensure you have the knowledge and tools needed for success.

## Knowledge Prerequisites

### Essential (Must Have)

####  Python Programming
You should be comfortable with:
- Basic Python syntax and data structures
- Functions and classes
- Working with libraries/packages
- Virtual environments

```python
# If this makes sense, you're good!
def process_documents(docs: list[str]) -> list[dict]:
    return [{"text": doc, "length": len(doc)} for doc in docs]
```

#### Basic AI/ML Concepts
Understanding of:
- What language models are
- Input/output of AI models
- Basic NLP concepts (tokens, embeddings)

### Helpful (Nice to Have)

- **REST APIs**: For building backends
- **TypeScript/React**: For frontend integration
- **Vector mathematics**: Understanding similarity
- **Database basics**: SQL or NoSQL experience

:::info Don't Worry!
Even if you don't have all the "nice to have" skills, we'll explain concepts as we go. The book is designed to teach you!
:::

## Technical Setup

### 1. Python Environment

**Required Version**: Python 3.10 or higher

```bash
# Check your Python version
python --version  # Should show 3.10+

# Create virtual environment
python -m venv rag-env

# Activate (Windows)
rag-env\Scripts\activate

# Activate (Mac/Linux)
source rag-env/bin/activate
```

### 2. Essential Libraries

Install these packages:

```bash
pip install openai>=1.12.0
pip install qdrant-client>=1.7.0
pip install fastapi>=0.110.0
pip install uvicorn>=0.27.0
pip install python-dotenv>=1.0.0
```

**What each library does**:
- `openai`: Access OpenAI's GPT models and embeddings
- `qdrant-client`: Connect to Qdrant vector database
- `fastapi`: Build the API backend
- `uvicorn`: Run the FastAPI server
- `python-dotenv`: Manage environment variables

### 3. API Keys & Services

You'll need accounts for:

#### OpenAI API
- Sign up at https://platform.openai.com
- Create API key in dashboard
- **Cost**: ~$5-10 for learning/testing

```bash
# Set your API key
export OPENAI_API_KEY="sk-your-key-here"
```

#### Qdrant Cloud (Free Tier)
- Sign up at https://cloud.qdrant.io
- Create free cluster (1GB storage)
- Get API URL and key

```bash
export QDRANT_URL="https://your-cluster.qdrant.io"
export QDRANT_API_KEY="your-qdrant-key"
```

:::tip Free Tier Limits
Qdrant's free tier (1GB) is perfect for learning. It can store ~500,000 embeddings, enough for medium-sized documentation!
:::

### 4. Development Tools

**Text Editor / IDE**:
- VS Code (recommended)
- PyCharm
- Cursor

**Optional but Helpful**:
- Git for version control
- Postman for API testing
- Docker for deployment

## Hardware Requirements

### Minimum
- **RAM**: 8GB
- **Storage**: 5GB free space
- **Internet**: Stable connection for API calls

### Recommended
- **RAM**: 16GB (for comfortable development)
- **Storage**: 10GB+ (for datasets and caching)

:::info Cloud Alternative
Don't have powerful hardware? Use Google Colab or Replit for cloud-based development!
:::

## Knowledge Check

Before proceeding, ensure you can:

✅ Run Python scripts  
✅ Install packages with pip  
✅ Set environment variables  
✅ Make HTTP requests  
✅ Understand JSON data format

## Quick Setup Script

Here's a complete setup script:

```bash
#!/bin/bash

# Create project directory
mkdir rag-project && cd rag-project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install openai qdrant-client fastapi uvicorn python-dotenv

# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your-key-here
QDRANT_URL=your-url-here
QDRANT_API_KEY=your-key-here
EOF

# Create basic structure
mkdir -p {data,src,tests}

echo "Setup complete! Don't forget to add your API keys to .env"
```

## Testing Your Setup

Run this quick test to verify everything works:

```python
# test_setup.py
import openai
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()

def test_setup():
    print("Testing setup...")
    
    # Test OpenAI
    try:
        client = openai.OpenAI()
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input="Test"
        )
        print("✓ OpenAI connection successful")
    except Exception as e:
        print(f"✗ OpenAI failed: {e}")
    
    # Test Qdrant
    try:
        qdrant = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        print("✓ Qdrant connection successful")
    except Exception as e:
        print(f"✗ Qdrant failed: {e}")

if __name__ == "__main__":
    test_setup()
```

## Estimated Costs

For learning this book:
- **OpenAI API**: $5-15 (embeddings + completions)
- **Qdrant Cloud**: Free (1GB tier)
- **Total**: ~$5-15 for complete hands-on learning

:::tip Cost Saving
Use `gpt-4o-mini` instead of `gpt-4` for learning. It's 10x cheaper and still very capable!
:::

## Ready to Go?

If you have:
- ✅ Python 3.10+ installed
- ✅ Required libraries installed
- ✅ API keys configured
- ✅ Test script passing

You're ready to move to Chapter 2 and learn about **Core Concepts**!

---

**Next**: Dive into [Vector Embeddings](../chapter-2/vector-embeddings), the foundation of RAG.
