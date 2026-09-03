# DocChat AI - Document Question & Answering with RAG

📚 **DocChat AI** is a comprehensive Python application that allows users to upload PDF and DOCX documents and ask questions about their content using an AI-powered chatbot. Built with Streamlit, LangChain, and ChromaDB.

## 🎯 Objective

Create a user-friendly "Chat with Documents" application that:

- Accepts one or multiple PDF/DOCX files
- Extracts text from documents while preserving metadata
- Splits text into manageable chunks
- Generates embeddings for semantic search
- Stores embeddings in a local vector database
- Retrieves the most relevant chunks for user queries
- Generates accurate answers using an LLM
- Displays source citations with document names and page numbers
- Maintains conversation history for follow-up questions

## 🛠 Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend | **Streamlit** 1.39.0 |
| RAG Framework | **LangChain** 0.2.14 |
| Vector DB | **ChromaDB** 0.5.5 |
| PDF Extraction | **PyMuPDF** 1.24.8 |
| DOCX Parsing | **python-docx** 1.1.0 |
| Embeddings | **OpenAI** (text-embedding-3-small) |
| LLM | **OpenAI** (gpt-3.5-turbo) |
| Env Config | **python-dotenv** 1.0.1 |

## 📁 Project Structure

```
docchat-ai/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env                       # API keys (not tracked by git)
├── .env.example               # Template for .env
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
│
├── data/                      # Sample documents folder
│
├── vectorstore/               # ChromaDB persistent storage
│   └── (auto-generated)
│
└── src/                       # Application modules
    ├── __init__.py
    ├── document_loader.py     # PDF/DOCX loading & text extraction
    ├── text_splitter.py       # Text chunking with metadata
    ├── embeddings.py          # Embedding generation (OpenAI)
    ├── vector_store.py        # ChromaDB vector database
    ├── retriever.py           # Document retrieval & ranking
    ├── llm.py                 # LLM interaction (OpenAI)
    └── chat.py                # Chat history & conversation management
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.11 or higher
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### Step 1: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

1. Copy the template:
```bash
copy .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```
LLM_API_KEY=sk-your-api-key-here
EMBEDDING_API_KEY=sk-your-api-key-here
```

**⚠️ Important:** Keep your `.env` file private! Never commit it to version control.

### Step 4: Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📖 How It Works

### RAG Pipeline Overview

1. **Document Upload**
   - Users upload PDF/DOCX files through Streamlit UI
   - File validation (type, size, corruption check)

2. **Text Extraction**
   - **PDF**: Uses PyMuPDF to extract text, preserving page numbers
   - **DOCX**: Uses python-docx for structured extraction
   - Metadata captured: filename, page number, file type

3. **Text Chunking**
   - Splits documents into ~1000 character chunks
   - Maintains 150 character overlap for context preservation
   - Uses `RecursiveCharacterTextSplitter` to avoid mid-sentence breaks

4. **Embedding Generation**
   - Creates embeddings using OpenAI's `text-embedding-3-small` model
   - Embeddings are vector representations (~1536 dimensions)
   - Each chunk receives its own embedding

5. **Vector Database Storage**
   - Stores embeddings in ChromaDB
   - Persists locally for future use (no need to re-embed)
   - Organizes by collection for flexibility

6. **Query Processing**
   - User question is embedded using the same model
   - Semantic similarity search retrieves top-5 most relevant chunks
   - Retrieved chunks become context for the LLM

7. **Answer Generation**
   - LLM (gpt-3.5-turbo) receives:
     - System prompt: instructions to only use document context
     - Retrieved document chunks as context
     - User's question
   - Generates grounded, accurate answer

8. **Source Citations**
   - Displays document names and page numbers
   - Users know exactly where information came from

### Chat History

- Maintains conversation context in Streamlit session state
- Users can ask follow-up questions (e.g., "How much did it increase?")
- System prioritizes retrieved document context over conversation history

### Error Handling

Gracefully handles:
- Missing documents before processing
- Missing API keys
- Empty/scanned PDFs (image-only)
- Corrupted files
- Unsupported file types
- API failures
- No relevant information found
- Vector database issues

Display helpful error messages instead of tracebacks.

## 💬 Usage Examples

### Example 1: Simple Query

**User:** "What is the company's revenue?"

**Assistant:** "Based on the Annual Report, the company reported a total revenue of $50 million in Q4 2023."

**Sources:**
- 📄 Annual_Report.pdf — Page 12

### Example 2: Multiple Document Query

**User:** "According to the documents, what is our vacation policy?"

**Assistant:** "The Employee Handbook states that employees are entitled to 20 days of paid vacation annually, plus 5 additional sick days..."

**Sources:**
- 📄 Employee_Handbook.docx — Page 3
- 📄 HR_Policy.pdf — Page 5

### Example 3: Follow-up Question

**User:** "What is the company's revenue?"
**Assistant:** "$50 million"

**User:** "How much did it increase?"
**Assistant:** "Compared to the previous year's $42 million, this represents a 19% increase."

## ⚙️ Configuration

### Adjustable Parameters (in `app.py`)

```python
CHUNK_SIZE = 1000           # Characters per chunk
CHUNK_OVERLAP = 150         # Overlap between chunks
TOP_K_RETRIEVAL = 5         # Top documents to retrieve
VECTORSTORE_PATH = "vectorstore"  # Database location
```

Modify these to:
- Increase `CHUNK_SIZE` for longer, more complete context
- Decrease `CHUNK_SIZE` for faster retrieval of specific details
- Adjust `TOP_K_RETRIEVAL` to balance comprehensiveness vs. conciseness

### LLM Model Selection (in `src/llm.py`)

```python
provider = OpenAILLMProvider(model="gpt-4")  # Use GPT-4 for better quality
```

Available models:
- `gpt-3.5-turbo` (faster, cheaper)
- `gpt-4` (smarter, more expensive)
- `gpt-4-turbo` (balanced)

## 🎨 UI Features

### Sidebar
- File uploader supporting PDF/DOCX
- "Process Documents" button with progress indicator
- Document count display
- Clear chat/documents buttons
- Status indicator

### Main Interface
- Clean, modern Streamlit design
- Chat history display
- Real-time answer generation
- Source citations with document links
- Error/warning messages
- Helpful getting-started guide

## ⚠️ Known Limitations

1. **Scanned PDFs**: Image-only PDFs cannot be processed (OCR support planned)
2. **Large Documents**: Very large files (>50MB) are rejected
3. **API Costs**: Embeddings and LLM calls incur OpenAI API charges
4. **Single Session**: Chat history is per-session (not persistent across browser closes)
5. **No Authentication**: No user authentication (suitable for single-user deployments)

## 🔄 Future Improvements

- [ ] OCR support for scanned PDFs
- [ ] Document update/re-embedding capability
- [ ] Advanced filters (date ranges, document types)
- [ ] User authentication & multi-user support
- [ ] Custom LLM/embedding provider support
- [ ] Chat history persistence to database
- [ ] RAG quality metrics (relevance scores, answer confidence)
- [ ] Support for docx tables and complex formatting
- [ ] Streaming responses for faster feedback
- [ ] Batch document processing
- [ ] Admin dashboard for usage analytics

## 🐛 Troubleshooting

### "API Key Missing" Error
**Solution:** Ensure `.env` file exists with `LLM_API_KEY` set correctly
```bash
# Verify the file exists
cat .env
```

### "No module named 'langchain'" Error
**Solution:** Reinstall dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### "Empty PDF or Scanned PDF" Warning
**Solution:** Ensure your PDF has selectable text (not an image scan). Use OCR tools or re-export from the source.

### "Vector database not found" Error
**Solution:** Process documents again. The vectorstore folder will be created automatically.

### Slow Response Times
**Solutions:**
- Reduce `CHUNK_SIZE` to retrieve fewer documents
- Use `gpt-3.5-turbo` instead of `gpt-4`
- Ensure internet connection is stable
- Check OpenAI API status

## 📝 Code Quality

- **Modular Design**: Each RAG component is in a separate module
- **Error Handling**: Comprehensive try-catch blocks with user-friendly messages
- **Comments**: Key logic explained inline
- **Type Hints**: Python type annotations for clarity
- **Best Practices**: Follows PEP 8 conventions

## 📄 Example Documents

Add sample documents to the `data/` folder to test:

```
data/
├── sample_report.pdf
├── employee_handbook.docx
└── financial_statement.pdf
```

Then upload them via the UI.

## 🤝 Contributing

To extend this project:

1. **Add Custom LLM Provider**: Implement `LLMProvider` in `src/llm.py`
   ```python
   class AnthropicLLMProvider(LLMProvider):
       def generate_answer(self, context: str, query: str) -> str:
           # Your implementation
   ```

2. **Add Custom Embedding Provider**: Implement `EmbeddingProvider` in `src/embeddings.py`
   ```python
   class HuggingFaceLLMProvider(EmbeddingProvider):
       def embed_documents(self, texts: List[str]) -> List[List[float]]:
           # Your implementation
   ```

3. **Add OCR Support**: Extend `DocumentLoader.load_pdf()` to detect and process scanned PDFs

## 📄 License

This project is open source and available under the MIT License.

## 📧 Support

For issues, questions, or suggestions, please refer to the troubleshooting section above or check the Streamlit/LangChain documentation:

- [Streamlit Docs](https://docs.streamlit.io/)
- [LangChain Docs](https://python.langchain.com/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [OpenAI API Docs](https://platform.openai.com/docs/)

---

**Happy documenting! 📚✨**
