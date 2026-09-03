# DocChat AI - Complete Setup Guide

## Quick Start (5 minutes)

### 1. Prerequisites
- Python 3.11+ installed
- OpenAI API key (free account at https://platform.openai.com)

### 2. Navigate to Project
```bash
cd "D:\codanics_data_science\Streamlit apps\docchat-ai"
```

### 3. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt after activation.

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- streamlit (UI framework)
- langchain (RAG orchestration)
- chromadb (vector database)
- python-docx (DOCX parsing)
- pymupdf (PDF extraction)
- python-dotenv (environment config)
- openai (LLM API)

### 5. Configure API Key

Open `.env` file and replace the placeholder:

```env
LLM_API_KEY=sk-your_actual_openai_api_key_here
EMBEDDING_API_KEY=sk-your_actual_openai_api_key_here
```

**How to get OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Log in or create an account
3. Click "Create new secret key"
4. Copy the key and paste it in `.env`

### 6. Run the Application

```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`

---

## Step-by-Step Testing Checklist

After running the app, verify each feature:

### ✅ 1. Check File Upload
- [ ] Upload button visible in sidebar
- [ ] Accepts PDF files
- [ ] Accepts DOCX files
- [ ] Rejects unsupported formats with error

### ✅ 2. Check Document Processing
- [ ] Click "Process Documents" button
- [ ] See progress indicator (spinner)
- [ ] Success message appears with file count and chunk count
- [ ] Error message if no API key configured

### ✅ 3. Check Chat Interface
- [ ] Chat interface appears after processing
- [ ] Text input field visible
- [ ] Can type questions

### ✅ 4. Check Answer Generation
- [ ] Ask: "What are the main topics in the document?"
- [ ] Receives answer within 5-10 seconds
- [ ] Answer is relevant to document content
- [ ] No API error messages

### ✅ 5. Check Source Citations
- [ ] Sources section appears below answer
- [ ] Shows document name (e.g., "document.pdf")
- [ ] Shows page number (e.g., "Page 3")
- [ ] Format: "📄 filename.pdf — Page X"

### ✅ 6. Check Chat History
- [ ] Previous questions still visible
- [ ] Multiple exchanges don't interfere
- [ ] Can ask follow-up questions
- [ ] Follow-ups reference previous context

### ✅ 7. Check Clear Functions
- [ ] "Clear Chat" button empties conversation
- [ ] "Clear Docs" button resets everything
- [ ] After clear, upload interface returns to initial state

### ✅ 8. Check Error Handling
- [ ] Ask question before uploading → Error message
- [ ] Upload corrupted file → Handled gracefully
- [ ] Disconnect internet → Error caught
- [ ] Invalid API key → Clear error message

---

## Troubleshooting

### Problem: "No module named 'streamlit'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: "API Key not found"
**Solution:**
1. Check `.env` file exists: `ls .env` (or `dir .env` on Windows)
2. Verify format:
   ```
   LLM_API_KEY=sk-xxxxx...
   ```
3. No spaces around `=`
4. Restart Streamlit: `streamlit run app.py`

### Problem: "Python 3.11+ required"
**Solution:**
```bash
python --version
# If < 3.11, download from https://www.python.org/downloads/
```

### Problem: Virtual Environment Activation Issues
**Windows - Execution Policy Error:**
```bash
# Run PowerShell as Administrator, then:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate
```

### Problem: "No such file or directory: 'venv'"
**Solution:** Recreate it:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Problem: Slow Response (>30 seconds)
**Causes & Solutions:**
1. Large documents → Reduce `CHUNK_SIZE` in `app.py`
2. Using gpt-4 → Switch to gpt-3.5-turbo in `src/llm.py`
3. Network latency → Check internet connection
4. API overloaded → Wait and retry

---

## Project File Overview

| File | Purpose |
|------|---------|
| **app.py** | Main Streamlit application & UI |
| **requirements.txt** | Python dependencies |
| **.env** | API keys (keep secret!) |
| **.env.example** | Template for .env |
| **README.md** | Full documentation |
| **src/document_loader.py** | PDF/DOCX text extraction |
| **src/text_splitter.py** | Text chunking logic |
| **src/embeddings.py** | Embedding generation |
| **src/vector_store.py** | ChromaDB integration |
| **src/retriever.py** | Document search/retrieval |
| **src/llm.py** | LLM answer generation |
| **src/chat.py** | Chat history management |

---

## Advanced Configuration

### Change Chunk Size
Edit `app.py`, line ~30:
```python
CHUNK_SIZE = 1000  # Increase for longer context, decrease for specificity
```

### Use GPT-4 Instead of GPT-3.5
Edit `src/llm.py`, line ~24:
```python
provider = OpenAILLMProvider(model="gpt-4")
```

### Retrieve More/Fewer Documents
Edit `app.py`, line ~31:
```python
TOP_K_RETRIEVAL = 5  # Change to 3 for faster, or 10 for more comprehensive
```

---

## Understanding the RAG Pipeline

```
User Question
    ↓
[Embedding Layer] - Convert question to vector
    ↓
[Vector Database] - Search for similar chunks
    ↓
[Retrieval] - Get top-5 most relevant chunks
    ↓
[Context Formatting] - Prepare chunks for LLM
    ↓
[LLM Prompt] - Send question + context to OpenAI
    ↓
[Answer Generation] - LLM generates grounded answer
    ↓
[Source Citation] - Extract & display sources
    ↓
User Response + Sources
```

---

## Performance Tips

1. **For Faster Responses:**
   - Use fewer `TOP_K_RETRIEVAL` (default: 5, try 3)
   - Use `gpt-3.5-turbo` instead of `gpt-4`
   - Reduce `CHUNK_SIZE` to 500-800 characters

2. **For Better Quality:**
   - Increase `CHUNK_SIZE` to 1500-2000 characters
   - Use `gpt-4` or `gpt-4-turbo`
   - Increase `TOP_K_RETRIEVAL` to 8-10

3. **For Cheaper Operations:**
   - Use `gpt-3.5-turbo` (costs 1/10th of GPT-4)
   - Use `text-embedding-3-small` (already configured)
   - Reduce embedding calls by caching (future improvement)

---

## Important Security Notes

⚠️ **NEVER:**
- Commit `.env` to git (it's in `.gitignore`)
- Share your API key
- Push code with API keys visible
- Leave `.env` file on shared computers

✅ **DO:**
- Keep `.env` secure and local-only
- Rotate keys if accidentally exposed
- Use `.env.example` as template only
- Review `.gitignore` before commits

---

## Next Steps

After successful setup:

1. **Test with Documents:**
   - Add PDF/DOCX files to `data/` folder
   - Upload and process them
   - Test various questions

2. **Customize:**
   - Modify system prompt in `src/llm.py`
   - Adjust chunk sizes and retrieval count
   - Change UI styling in `app.py`

3. **Production Deployment:**
   - Deploy using Streamlit Cloud (free tier available)
   - Or: Use Docker + cloud platforms (AWS, Azure, GCP)
   - Add user authentication for multi-user setup

4. **Extend Functionality:**
   - Add OCR for scanned PDFs
   - Implement document versioning
   - Add analytics dashboard
   - Support more file formats (.txt, .xlsx, etc.)

---

## Support & Resources

- **Streamlit Docs:** https://docs.streamlit.io/
- **LangChain Docs:** https://python.langchain.com/
- **ChromaDB Docs:** https://docs.trychroma.com/
- **OpenAI API:** https://platform.openai.com/docs/

---

**Ready to start? Run `streamlit run app.py` and happy documenting! 📚✨**
