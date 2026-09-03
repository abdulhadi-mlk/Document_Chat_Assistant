# DocChat AI - Testing Checklist & Instructions

## Pre-Launch Testing (Before Running)

### ✅ 1. Environment Setup
```bash
# Check Python version (must be 3.11+)
python --version

# Check if venv exists
ls -la venv/  # (or dir venv on Windows)

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### ✅ 2. Dependencies Verification
```bash
# Verify all packages installed
pip list

# Expected packages:
# - streamlit==1.39.0
# - langchain==0.2.14
# - chromadb==0.5.5
# - pymupdf==1.24.8
# - python-docx==1.1.0
# - openai==1.51.0
# - python-dotenv==1.0.1
```

### ✅ 3. Configuration Check
```bash
# Verify .env file exists
cat .env  # (type .env on Windows)

# Should contain:
# LLM_API_KEY=sk-xxxxx...
# EMBEDDING_API_KEY=sk-xxxxx...

# ⚠️ Do NOT commit .env file!
```

### ✅ 4. Code Quality
```bash
# Check for syntax errors
python -m py_compile app.py
python -m py_compile src/*.py

# Should complete without output (no errors)
```

---

## Launch Testing (Running the App)

### ✅ 5. Application Startup
```bash
streamlit run app.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.
  
  Local URL: http://localhost:8501
  Network URL: http://xxx.xxx.x.x:8501
```

**Verify in Browser:**
- [ ] Page loads without errors
- [ ] Title "📚 DocChat AI" visible
- [ ] Sidebar appears on left
- [ ] Main content area visible
- [ ] No console errors (check F12 Developer Tools)

---

## Feature Testing (After App Loads)

### ✅ 6. File Upload Functionality

**Test 1: Upload Supported Files**
```
1. In sidebar, click "Select PDF or DOCX files"
2. Choose any .pdf or .docx file from your computer
3. File appears in "Files ready to process" list
4. Repeat for multiple files
```

**Expected Behavior:**
- [ ] File picker opens
- [ ] File name displays after selection
- [ ] Multiple files can be selected
- [ ] Files show with ✓ checkmark

**Test 2: Reject Unsupported Files**
```
1. Try uploading .txt, .xlsx, or .png file
2. Observe error handling
```

**Expected Behavior:**
- [ ] Unsupported file type rejected
- [ ] Clear error message
- [ ] No crash or traceback

---

### ✅ 7. Document Processing

**Test 1: Process Documents**
```
1. Upload 1-2 PDF/DOCX files
2. Click "🔄 Process Documents" button
3. Wait for completion
```

**Expected Behavior:**
- [ ] Spinner/loading indicator appears
- [ ] "Processing documents..." message
- [ ] Status message: "✅ Documents processed successfully!"
- [ ] File count and chunk count displayed
- [ ] Chat interface becomes visible

**Test 2: Handle Empty Files**
```
1. Create empty .pdf or .docx file
2. Upload it
3. Process documents
```

**Expected Behavior:**
- [ ] Warning message: "Empty or scanned PDF"
- [ ] Processing continues with other files
- [ ] No crash

**Test 3: Handle Corrupted Files**
```
1. Create invalid .pdf (e.g., text file renamed to .pdf)
2. Upload it
3. Process documents
```

**Expected Behavior:**
- [ ] Error message with filename
- [ ] Other valid files still processed
- [ ] Application doesn't crash

---

### ✅ 8. Chat Interface

**Test 1: Basic Question**
```
1. After documents processed, type question:
   "What is the main topic of the document?"
2. Press Enter or click submit
3. Wait for response
```

**Expected Behavior:**
- [ ] Response received within 10 seconds
- [ ] Answer is relevant to document
- [ ] No Python errors
- [ ] Response shows as "Assistant: ..."

**Test 2: Follow-up Question**
```
1. Ask initial question (e.g., "What is the revenue?")
2. Ask follow-up: "How much did it increase?"
3. System should understand context
```

**Expected Behavior:**
- [ ] Both questions appear in chat history
- [ ] Follow-up answer makes sense
- [ ] No context loss between questions

**Test 3: Question Before Processing**
```
1. Without processing documents, type a question
2. Submit
```

**Expected Behavior:**
- [ ] Info message: "Upload and process documents first"
- [ ] No crash
- [ ] Clear user guidance

---

### ✅ 9. Source Citations

**Test: Verify Citations**
```
1. Ask any question
2. Look for "Sources" section below answer
3. Check formatting
```

**Expected Format:**
```
**Sources**
📄 document.pdf — Page 3
📄 document.pdf — Page 7
```

**Verify:**
- [ ] Sources section appears
- [ ] Document names are correct
- [ ] Page numbers are valid
- [ ] Format is clean (📄 symbol, proper spacing)
- [ ] Sources match retrieved documents

---

### ✅ 10. Error Handling

**Test 1: Missing API Key**
```
1. Remove/comment out LLM_API_KEY from .env
2. Restart app
3. Try to process documents
```

**Expected Behavior:**
- [ ] Error message: "API Key Missing"
- [ ] No traceback
- [ ] Clear instructions to add key

**Test 2: Invalid API Key**
```
1. Change LLM_API_KEY to invalid value
2. Process documents
3. Try asking question
```

**Expected Behavior:**
- [ ] Error message during processing or query
- [ ] Graceful handling
- [ ] No ugly Python traceback

**Test 3: Network Failure Simulation**
```
1. Disconnect internet
2. Try processing or asking question
```

**Expected Behavior:**
- [ ] Timeout or connection error message
- [ ] User-friendly error, not traceback

---

### ✅ 11. Clear Functions

**Test 1: Clear Chat History**
```
1. Ask several questions (build history)
2. Click "🗑️ Clear Chat History" button
3. Observe result
```

**Expected Behavior:**
- [ ] All messages disappear
- [ ] Chat interface still available
- [ ] Can ask new questions
- [ ] "Chat history cleared!" message

**Test 2: Clear Documents**
```
1. After processing, click "🗑️ Clear Docs" button
2. Observe result
```

**Expected Behavior:**
- [ ] Chat interface disappears
- [ ] Returns to initial state
- [ ] Upload interface visible again
- [ ] Sidebar shows "Process Documents" button

---

### ✅ 12. Performance & Limits

**Test 1: Large Files**
```
1. Try uploading file >50 MB
2. Observe
```

**Expected Behavior:**
- [ ] Clear error message
- [ ] Message about file size limit
- [ ] No crash

**Test 2: Multiple Documents**
```
1. Upload 3-5 different PDFs
2. Process together
3. Ask questions spanning multiple docs
```

**Expected Behavior:**
- [ ] All documents processed
- [ ] Sources show correct documents
- [ ] Responses reference multiple files correctly

**Test 3: Response Time**
```
1. Time the response for typical question
2. Measure end-to-end time
```

**Expected Baseline:**
- [ ] First response: 5-15 seconds (embedding + retrieval + LLM)
- [ ] Follow-up responses: 3-10 seconds

**Performance Tips if Slow:**
- Check internet speed
- Reduce `TOP_K_RETRIEVAL` from 5 to 3
- Use `gpt-3.5-turbo` instead of `gpt-4`

---

## Browser Console Testing (F12)

### ✅ 13. Console Errors

Open browser Developer Tools (F12) and check Console tab:

**Expected:**
- [ ] No red error messages
- [ ] No JavaScript exceptions
- [ ] No CORS errors

**If Errors Appear:**
- Note error message
- Check Streamlit terminal for backend errors
- Review SETUP_GUIDE.md troubleshooting section

---

## Regression Testing (After Changes)

If you modify code, run this sequence:

1. Check syntax: `python -m py_compile src/*.py`
2. Start app: `streamlit run app.py`
3. Upload document
4. Process documents
5. Ask 2-3 questions
6. Check sources
7. Clear chat
8. Verify no errors
9. Stop app (Ctrl+C)
10. Check vectorstore folder created

---

## Load Testing (Optional)

### Test: Multiple Sequential Questions
```
1. Process documents
2. Ask 10 rapid questions
3. Monitor response times
4. Check for memory leaks (Task Manager)
5. Verify all answers are coherent
```

### Test: Session Persistence
```
1. Process documents
2. Ask question + get answer
3. Refresh browser (F5)
4. Verify documents still processed
5. Chat history may clear (expected)
6. Try new questions
```

---

## Final Checklist Before Deployment

- [ ] All 13 test sections passed
- [ ] No console errors
- [ ] No Python tracebacks
- [ ] Performance acceptable
- [ ] Error messages are user-friendly
- [ ] Source citations accurate
- [ ] Multiple file upload works
- [ ] Chat history works
- [ ] Clear buttons work
- [ ] .env file secure (not in git)
- [ ] README and SETUP_GUIDE complete
- [ ] Code has inline comments
- [ ] All imports resolve correctly

---

## Production Deployment Checklist

Before deploying to production:

- [ ] Update `gpt-3.5-turbo` to `gpt-4` (optional, for quality)
- [ ] Set `temperature=0.3` in `src/llm.py` (more consistent)
- [ ] Add logging for debugging
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Configure rate limiting
- [ ] Add user authentication
- [ ] Monitor API costs
- [ ] Set up backup strategy for vectorstore
- [ ] Test with 100+ documents
- [ ] Load test with concurrent users
- [ ] Document deployment procedure

---

## Quick Troubleshooting Reference

| Issue | Solution |
|-------|----------|
| "Module not found" | Run `pip install -r requirements.txt` |
| "API key missing" | Check `.env` file, add key |
| "Connection timeout" | Check internet, OpenAI status |
| "Empty PDF warning" | Ensure PDF has selectable text, not image |
| "Slow responses" | Reduce TOP_K_RETRIEVAL, use gpt-3.5-turbo |
| "No sources shown" | Verify documents were processed |
| "Chat history empty" | Click "Clear Chat" may have cleared it |

---

## Support Resources

- **Streamlit Docs:** https://docs.streamlit.io/
- **LangChain Docs:** https://python.langchain.com/
- **OpenAI Status:** https://status.openai.com/
- **ChromaDB Issues:** https://github.com/chroma-core/chroma

---

**Testing Complete! 🎉 Your DocChat AI is ready for use!**
