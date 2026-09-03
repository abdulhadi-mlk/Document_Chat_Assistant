# DocChat AI - Installation Instructions Summary

## 📋 Complete Installation Steps

### Windows Users:

```bash
# 1. Navigate to project directory
cd "D:\codanics_data_science\Streamlit apps\docchat-ai"

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate

# You should see (venv) at the start of the command line

# 4. Upgrade pip (recommended)
python -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Configure environment
# Edit .env file and add your OpenAI API key:
# LLM_API_KEY=sk-your_api_key_here

# 7. Run the application
streamlit run app.py
```

### macOS/Linux Users:

```bash
# 1. Navigate to project directory
cd /path/to/docchat-ai

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Configure environment
# Edit .env file and add your OpenAI API key:
# LLM_API_KEY=sk-your_api_key_here

# 7. Run the application
streamlit run app.py
```

---

## 🔑 Getting Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in with your account
3. Click "Create new secret key"
4. Copy the generated key (starts with `sk-`)
5. Paste it into the `.env` file:
   ```
   LLM_API_KEY=sk-your_copied_key_here
   ```
6. **Never share this key!** Keep it private.

---

## ✅ After Installation

1. **Test the application:**
   - Open http://localhost:8501 in your browser
   - Upload a PDF or DOCX file
   - Click "Process Documents"
   - Ask a question

2. **If you get errors:**
   - Check SETUP_GUIDE.md or QUICK_REFERENCE.md
   - Verify your OpenAI API key is valid
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

3. **For detailed information:**
   - README.md - Features and how it works
   - SETUP_GUIDE.md - Troubleshooting and detailed setup
   - TESTING_GUIDE.md - Comprehensive testing procedures
   - QUICK_REFERENCE.md - Configuration and optimization

---

## 🚨 Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| `python: command not found` | Install Python 3.11+ from https://python.org |
| `pip: command not found` | Python may not be in PATH. Restart terminal and try again. |
| `ModuleNotFoundError: No module named 'streamlit'` | Run `pip install -r requirements.txt` |
| "API Key Missing" error | Add `LLM_API_KEY` to `.env` file and restart app |
| "Connection timeout" | Check internet connection, check OpenAI status at status.openai.com |

---

## 💾 Project Files Overview

```
docchat-ai/
├── app.py                  ← Run this with `streamlit run app.py`
├── requirements.txt        ← Dependencies (installed with pip)
├── .env                    ← Your API keys (DON'T commit to git!)
├── .env.example            ← Template for .env
├── .gitignore              ← Tells git which files to ignore
├── README.md               ← Complete documentation
├── SETUP_GUIDE.md          ← Detailed setup & troubleshooting
├── TESTING_GUIDE.md        ← Testing checklist
├── QUICK_REFERENCE.md      ← Configuration reference
│
├── src/                    ← Python modules
│   ├── __init__.py
│   ├── document_loader.py  ← PDF/DOCX extraction
│   ├── text_splitter.py    ← Text chunking
│   ├── embeddings.py       ← Embedding generation
│   ├── vector_store.py     ← ChromaDB storage
│   ├── retriever.py        ← Document retrieval
│   ├── llm.py              ← LLM integration
│   └── chat.py             ← Chat management
│
├── data/                   ← Place sample documents here
│
└── vectorstore/            ← ChromaDB storage (auto-created)
```

---

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Configure `.env` with your API key
3. ✅ Run `streamlit run app.py`
4. ✅ Follow TESTING_GUIDE.md to verify everything works
5. ✅ Refer to QUICK_REFERENCE.md for customization

---

## 📞 Need Help?

- **Setup issues?** → Check SETUP_GUIDE.md
- **Testing?** → Check TESTING_GUIDE.md
- **Configuration?** → Check QUICK_REFERENCE.md
- **Features?** → Check README.md

---

**Happy documenting! 📚✨**
