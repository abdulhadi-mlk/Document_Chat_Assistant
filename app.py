import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modules
from src.document_loader import DocumentLoader
from src.text_splitter import TextSplitter
from src.embeddings import EmbeddingManager
from src.vector_store import VectorStore
from src.retriever import Retriever
from src.llm import LLMManager
from src.chat import ChatManager


# ============================================================================
# CONFIGURATION
# ============================================================================

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K_RETRIEVAL = 5
VECTORSTORE_PATH = "vectorstore"


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="DocChat AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .subheader {
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .error-box {
        background-color: #ffe8e8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #d32f2f;
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #388e3c;
    }
    </style>
""", unsafe_allow_html=True)


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def initialize_session_state():
    """Initialize all session state variables."""
    if "documents_uploaded" not in st.session_state:
        st.session_state.documents_uploaded = []
    
    if "documents_processed" not in st.session_state:
        st.session_state.documents_processed = False
    
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    
    if "chat_manager" not in st.session_state:
        st.session_state.chat_manager = None
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = []


initialize_session_state()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def validate_api_keys():
    """Check that the Gemini keys required by this app are configured."""
    llm_key = os.getenv('GEMINI_API_KEY') or os.getenv('LLM_API_KEY')
    emb_key = os.getenv('GEMINI_API_KEY') or os.getenv('EMBEDDING_API_KEY')

    def looks_like_placeholder(k: str) -> bool:
        if not k:
            return True
        lowered = k.lower()
        # common placeholder fragments that indicate the user didn't replace the example value
        placeholders = ["your", "example", "replace", "<key>", "xxx"]
        return any(p in lowered for p in placeholders)

    # Prefer showing an error for embedding key since that's used for vectorization.
    if not emb_key or looks_like_placeholder(emb_key):
        st.error("⚠️ **Embedding API Key Missing or Placeholder**\n\n"
                 "Set a valid Gemini API key in your `.env` file or environment:\n"
                 "```\nGEMINI_API_KEY=AIza...\n```\n\n"
                 "`EMBEDDING_API_KEY` is also supported for backwards compatibility.\n"
                 "Do NOT commit your keys to source control.")
        return False

    # Fallback check for LLM key (less critical if embeddings have a valid key)
    if not llm_key or looks_like_placeholder(llm_key):
        st.warning("⚠️ **LLM API Key Missing or Placeholder**\n\n"
                 "The app will still attempt to use embeddings, but LLM features may not work.\n"
                 "Add `GEMINI_API_KEY=AIza...` to your `.env` if needed.")

    return True


def process_uploaded_files(uploaded_files):
    """Process uploaded files and extract text."""
    if not uploaded_files:
        return [], []
    
    # Save files to temporary directory
    temp_dir = tempfile.mkdtemp()
    file_paths = []
    
    for uploaded_file in uploaded_files:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        file_paths.append(file_path)
    
    # Load documents
    loader = DocumentLoader()
    documents, errors = loader.load_multiple_documents(file_paths)
    
    return documents, errors


def split_and_embed_documents(documents):
    """Split documents and generate embeddings."""
    if not documents:
        return None, "No documents to process."
    
    # Split documents
    splitter = TextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(documents)
    
    if not chunks:
        return None, "No text chunks generated from documents."
    
    # Generate embeddings
    try:
        embedding_manager = EmbeddingManager()
        chunks = embedding_manager.embed_chunks(chunks)
    except Exception as e:
        if "PERMISSION_DENIED" in str(e) and "project has been denied access" in str(e):
            return None, (
                "Gemini denied access to the Google Cloud project behind this API key (403). "
                "Open that project in Google Cloud Console, review any warning banner or appeal, "
                "then use a Gemini API key from an approved project."
            )
        return None, f"Error generating embeddings: {str(e)}"
    
    return chunks, embedding_manager


def initialize_rag_pipeline(chunks, embedding_manager):
    """Initialize the RAG pipeline with processed documents."""
    try:
        # Create vector store
        vector_store = VectorStore(db_path=VECTORSTORE_PATH)
        vector_store.create_or_get_collection(collection_name="documents")
        vector_store.add_documents(chunks)
        
        # Create retriever
        retriever = Retriever(vector_store, embedding_manager, top_k=TOP_K_RETRIEVAL)
        
        # Create LLM manager
        llm_manager = LLMManager()
        
        # Create chat manager
        chat_manager = ChatManager(retriever, llm_manager)
        
        return vector_store, chat_manager
    except Exception as e:
        st.error(f"❌ Error initializing RAG pipeline: {str(e)}")
        return None, None


# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 📚 **DocChat AI**")
    st.markdown("---")
    
    # File uploader
    st.subheader("📤 Upload Documents")
    uploaded_files = st.file_uploader(
        "Select PDF or DOCX files:",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )
    
    # Display uploaded files
    if uploaded_files:
        st.markdown("**Files ready to process:**")
        for file in uploaded_files:
            st.caption(f"✓ {file.name}")
    
    # Process button
    col1, col2 = st.columns(2)
    
    with col1:
        process_button = st.button(
            "🔄 Process Documents",
            key="process_button",
            use_container_width=True
        )
    
    with col2:
        if st.session_state.documents_processed:
            clear_docs = st.button(
                "🗑️ Clear Docs",
                key="clear_docs",
                use_container_width=True
            )
        else:
            clear_docs = False
    
    # Status
    if st.session_state.documents_processed:
        st.markdown("---")
        st.markdown("**✅ Status: Documents Processed**")
        st.metric("Documents", len(st.session_state.processed_files))
        
        st.markdown("---")
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            if st.session_state.chat_manager:
                st.session_state.chat_manager.clear_history()
            st.success("Chat history cleared!")


# ============================================================================
# MAIN CONTENT
# ============================================================================

st.markdown("<h1 class='main-header'>📚 DocChat AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Upload your documents and ask questions about them.</p>", unsafe_allow_html=True)


# Process documents
if process_button:
    if not validate_api_keys():
        st.stop()
    
    if not uploaded_files:
        st.error("❌ No files selected. Please upload PDF or DOCX files.")
    else:
        with st.spinner("📖 Processing documents... This may take a moment."):
            try:
                # Load documents
                documents, errors = process_uploaded_files(uploaded_files)
                
                # Display warnings for any errors
                if errors:
                    for error in errors:
                        st.warning(f"⚠️ {error}")
                
                if not documents:
                    st.error("❌ No text could be extracted from the uploaded files.")
                else:
                    # Split and embed
                    chunks, embedding_manager = split_and_embed_documents(documents)
                    
                    if chunks is None:
                        st.error(f"❌ {embedding_manager}")
                    else:
                        # Initialize RAG pipeline
                        vector_store, chat_manager = initialize_rag_pipeline(chunks, embedding_manager)
                        
                        if vector_store and chat_manager:
                            st.session_state.vector_store = vector_store
                            st.session_state.chat_manager = chat_manager
                            st.session_state.documents_processed = True
                            st.session_state.processed_files = [f.name for f in uploaded_files]
                            st.session_state.chat_history = []
                            
                            # Display info
                            info_msg = f"""
                            ✅ **Documents processed successfully!**
                            
                            - **Files processed:** {len(uploaded_files)}
                            - **Text chunks created:** {len(chunks)}
                            - **Embedding model:** gemini-embedding-001
                            
                            You can now ask questions about your documents below.
                            """
                            st.success(info_msg)
                        else:
                            st.error("❌ Failed to initialize RAG pipeline.")
            
            except Exception as e:
                st.error(f"❌ Error processing documents: {str(e)}")


# Clear documents
if clear_docs:
    st.session_state.documents_processed = False
    st.session_state.vector_store = None
    st.session_state.chat_manager = None
    st.session_state.chat_history = []
    st.session_state.processed_files = []
    st.rerun()


# ============================================================================
# CHAT INTERFACE
# ============================================================================

if st.session_state.documents_processed and st.session_state.chat_manager:
    st.markdown("---")
    st.subheader("💬 Ask a Question")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("**Chat History:**")
        for role, message in st.session_state.chat_history:
            if role == "user":
                st.markdown(f"**You:** {message}")
            else:
                st.markdown(f"**Assistant:** {message}")
    
    # Input
    query = st.text_input("Your question:", placeholder="E.g., What are the main points in the document?")
    
    if query:
        with st.spinner("🔍 Searching and generating answer..."):
            try:
                # Process query
                answer, context, sources = st.session_state.chat_manager.process_query(query)
                
                # Update chat history for display
                st.session_state.chat_history.append(("user", query))
                st.session_state.chat_history.append(("assistant", answer))
                
                # Display answer
                st.markdown("---")
                st.markdown("**Answer:**")
                st.markdown(answer)
                
                # Display sources
                if sources:
                    st.markdown("---")
                    sources_text = st.session_state.chat_manager.retriever.format_sources(sources)
                    st.markdown(sources_text)
                
            except Exception as e:
                st.error(f"❌ Error processing query: {str(e)}")

elif not st.session_state.documents_processed:
    st.info("""
    📋 **Get Started:**
    
    1. Upload one or more PDF/DOCX files using the file uploader on the left
    2. Click the "🔄 Process Documents" button
    3. Wait for processing to complete (embeddings will be generated)
    4. Ask questions about your documents below
    
    **Note:** Make sure your `.env` file contains your Gemini API key!
    """)

else:
    st.error("❌ Error: Chat manager not initialized. Please process documents again.")


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #888; font-size: 0.9rem;'>"
    "DocChat AI © 2024 | Powered by LangChain, ChromaDB & Gemini"
    "</p>",
    unsafe_allow_html=True
)
