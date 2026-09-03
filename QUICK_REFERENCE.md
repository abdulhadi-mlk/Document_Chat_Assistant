# DocChat AI - Quick Reference & Important Notes

## 🚀 30-Second Startup

```bash
# 1. Navigate to project
cd "D:\codanics_data_science\Streamlit apps\docchat-ai"

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Run app
streamlit run app.py

# App opens at http://localhost:8501
```

---

## 📋 Important Files

### Configuration
- **`.env`** - API keys (KEEP SECRET, never commit!)
- **`.env.example`** - Template only (safe to commit)
- **`.gitignore`** - Prevents .env from being committed

### Core Application
- **`app.py`** - Main UI and orchestration (13.2 KB)

### RAG Pipeline Modules
| Module | Responsibility | Key Function |
|--------|-----------------|--------------|
| `document_loader.py` | Load PDF/DOCX files | `load_document()` |
| `text_splitter.py` | Split into chunks | `split_documents()` |
| `embeddings.py` | Generate embeddings | `embed_chunks()` |
| `vector_store.py` | Store in ChromaDB | `add_documents()` |
| `retriever.py` | Find relevant chunks | `retrieve()` |
| `llm.py` | Generate answers | `generate_answer()` |
| `chat.py` | Manage conversation | `process_query()` |

### Documentation
- **`README.md`** - Complete feature documentation
- **`SETUP_GUIDE.md`** - Installation & troubleshooting
- **`TESTING_GUIDE.md`** - Comprehensive testing procedures

---

## ⚙️ Configuration Quick Reference

### Change LLM Model (in `src/llm.py`, line ~24)

```python
# Current (fast & cheap):
provider = OpenAILLMProvider(model="gpt-3.5-turbo")

# Better quality:
provider = OpenAILLMProvider(model="gpt-4")

# Fastest:
provider = OpenAILLMProvider(model="gpt-3.5-turbo")
```

### Change Chunk Size (in `app.py`, line ~30)

```python
CHUNK_SIZE = 1000      # Default
# Smaller = faster retrieval, less context
# Larger = more context, slower retrieval
```

### Change Number of Retrieved Documents (in `app.py`, line ~31)

```python
TOP_K_RETRIEVAL = 5    # Default (get top-5 chunks)
# 3-4 for faster responses
# 8-10 for more comprehensive answers
```

### Change Embedding Model (in `src/embeddings.py`, line ~31)

```python
model="text-embedding-3-small"  # Current (default)
# text-embedding-3-small = fast, good quality
# text-embedding-3-large = better quality, slower
```

---

## 🔑 API Key Setup

### Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)
4. Paste into `.env`:
```
LLM_API_KEY=sk-xxxxxxxxxxxxx
```

### Cost Estimates (approximate, as of 2024)
- **Embeddings:** $0.02 per 1M tokens (~1000 documents)
- **GPT-3.5-turbo:** $0.50 per 1M tokens (~1000 queries)
- **GPT-4:** $15.00 per 1M input tokens

---

## 🐛 Common Issues & Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| "API Key Missing" | Add LLM_API_KEY to .env |
| "Connection timeout" | Check internet, check OpenAI status |
| Slow responses (>30s) | Reduce TOP_K_RETRIEVAL to 3 |
| "Empty PDF warning" | Ensure PDF has text (not scanned image) |
| Chat history disappeared | Check if you clicked "Clear Chat" |
| Vectorstore not persisting | Check `vectorstore/` folder exists |

---

## 📊 RAG Pipeline Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                  User Uploads Documents                 │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              Document Loader (PyMuPDF/python-docx)      │
│         Extracts text + metadata (page #, filename)     │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│            Text Splitter (LangChain)                    │
│    Chunks: 1000 chars, 150 char overlap per chunk      │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│      Embedding Generator (OpenAI text-embedding-3)      │
│           Converts text → 1536-dim vectors             │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│         Vector Store (ChromaDB with Cosine)            │
│     Persists embeddings locally in vectorstore/        │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              User Asks Question                         │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│      Query Embedding (same model as document)           │
│            Question → 1536-dim vector                   │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│         Cosine Similarity Search (ChromaDB)             │
│        Retrieves top-5 most similar chunks              │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│      Format Context + System Prompt                     │
│        Combine retrieved chunks for LLM                 │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│      LLM (GPT-3.5-turbo or GPT-4)                       │
│  Generates answer using ONLY provided context          │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│       Extract & Display Answer + Sources               │
│   User sees answer + which documents were used         │
└─────────────────────────────────────────────────────────┘
```

---

## 📈 Performance Optimization

### For Speed (prioritize latency):
```python
CHUNK_SIZE = 500
TOP_K_RETRIEVAL = 3
model = "gpt-3.5-turbo"
temperature = 0.3
```
**Expected time:** 2-5 seconds

### For Quality (prioritize accuracy):
```python
CHUNK_SIZE = 1500
TOP_K_RETRIEVAL = 8
model = "gpt-4"
temperature = 0.3
```
**Expected time:** 10-20 seconds

### For Cost (prioritize budget):
```python
CHUNK_SIZE = 1000
TOP_K_RETRIEVAL = 3
model = "gpt-3.5-turbo"
# Use text-embedding-3-small
```
**Estimated cost:** ~$0.001 per query

---

## 🔐 Security Checklist

### Must Do
- [ ] Keep `.env` file local only
- [ ] Add `.env` to `.gitignore` (already done)
- [ ] Never log API keys
- [ ] Use environment variables, not hardcoded keys
- [ ] Keep dependencies updated

### For Production
- [ ] Use separate API keys per environment (dev/prod)
- [ ] Rotate keys regularly
- [ ] Monitor for unusual API usage
- [ ] Implement rate limiting
- [ ] Add authentication layer
- [ ] Use HTTPS only
- [ ] Log all user queries (for audit trail)

---

## 🧪 Testing Workflow

### Before First Run
```bash
# 1. Syntax check
python -m py_compile app.py src/*.py

# 2. Dependency check
pip list | grep -E "streamlit|langchain|chromadb"
```

### First Launch
```bash
streamlit run app.py

# 1. Check sidebar loads
# 2. Upload a small PDF
# 3. Process documents
# 4. Ask one simple question
# 5. Verify sources appear
```

### Comprehensive Test
See `TESTING_GUIDE.md` for full 13-section test suite.

---

## 🎓 Learning Resources

### For Understanding RAG
- [LangChain Docs - RAG](https://python.langchain.com/docs/use_cases/question_answering/)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [ChromaDB Getting Started](https://docs.trychroma.com/)

### For Streamlit
- [Streamlit Docs](https://docs.streamlit.io/)
- [Streamlit Components](https://streamlit.io/components)
- [Session State](https://docs.streamlit.io/library/api-reference/session-state)

### For LangChain
- [Python LangChain Docs](https://python.langchain.com/)
- [Integrations](https://python.langchain.com/docs/integrations/)
- [RAG from Scratch](https://github.com/langchain-ai/rag-from-scratch)

---

## 📞 Deployment Options

### Option 1: Streamlit Cloud (Free)
```bash
# Push to GitHub, then:
# 1. Go to share.streamlit.io
# 2. Select repo
# 3. Set secrets (.env values)
# 4. Deploy!
```

### Option 2: Docker
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

### Option 3: Traditional VPS (AWS/Azure/GCP)
```bash
# 1. SSH into server
# 2. Clone repo
# 3. Setup virtual environment
# 4. Install dependencies
# 5. Run with PM2 or systemd
# 6. Use Nginx as reverse proxy
```

---

## 📝 Modification Examples

### Example 1: Change System Prompt
**File:** `src/llm.py`, lines ~13-22

```python
SYSTEM_PROMPT = """You are a helpful document assistant.
Answer questions based ONLY on provided documents.
Be concise and accurate."""
```

### Example 2: Add File Size Limit Check
**File:** `src/document_loader.py`, line ~16

```python
MAX_FILE_SIZE_MB = 100  # Change from 50 to 100
```

### Example 3: Store Chat History to Database
**File:** `src/chat.py`

Add to `ChatManager`:
```python
def save_to_db(self, user_id):
    # Store self.conversation_history to database
    pass
```

---

## ✅ Pre-Deployment Checklist

- [ ] All tests pass (see TESTING_GUIDE.md)
- [ ] API keys are valid
- [ ] .env is NOT committed to git
- [ ] README and SETUP_GUIDE are complete
- [ ] Code is well-commented
- [ ] Error handling is comprehensive
- [ ] Performance is acceptable
- [ ] UI is clean and intuitive
- [ ] Sources are accurately displayed
- [ ] Chat history works correctly
- [ ] Clear buttons function properly
- [ ] Large files are handled gracefully
- [ ] Multiple documents work together

---

## 🎯 Next Steps

1. **Setup:** Follow SETUP_GUIDE.md (5 minutes)
2. **Test:** Use TESTING_GUIDE.md (15 minutes)
3. **Customize:** Modify prompts, chunk sizes, etc.
4. **Deploy:** Use Streamlit Cloud or Docker
5. **Monitor:** Track API usage and costs
6. **Iterate:** Gather feedback and improve

---

## 📞 Support Contacts

- **LangChain Issues:** https://github.com/langchain-ai/langchain
- **ChromaDB Issues:** https://github.com/chroma-core/chroma
- **Streamlit Issues:** https://github.com/streamlit/streamlit
- **OpenAI API Status:** https://status.openai.com/

---

**DocChat AI is ready to use! Happy building! 🚀**

*Last Updated: August 2024*
*Version: 1.0.0*
