from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict


class TextSplitter:
    """Splits documents into chunks while preserving metadata."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 150):
        """
        Initialize the text splitter.
        
        Args:
            chunk_size: Maximum size of each chunk in characters.
            chunk_overlap: Number of characters to overlap between chunks.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def split_documents(self, documents: List[dict]) -> List[dict]:
        """
        Split documents into chunks while preserving metadata.
        
        Args:
            documents: List of document dictionaries with 'text' and 'metadata' keys.
        
        Returns:
            List of chunk dictionaries with text and metadata.
        """
        chunks = []
        
        for doc_idx, doc in enumerate(documents):
            text = doc.get('text', '')
            metadata = doc.get('metadata', {})
            filename = doc.get('filename', 'Unknown')
            page_number = doc.get('page_number', 1)
            
            if not text.strip():
                continue
            
            # Split the text into chunks
            text_chunks = self.splitter.split_text(text)
            
            for chunk_idx, chunk_text in enumerate(text_chunks):
                chunk_metadata = {
                    **metadata,
                    'chunk_number': chunk_idx + 1,
                    'total_chunks': len(text_chunks),
                    'filename': filename,
                    'page_number': page_number
                }
                
                chunks.append({
                    'text': chunk_text,
                    'metadata': chunk_metadata,
                    'filename': filename,
                    'page_number': page_number
                })
        
        return chunks
    
    def update_chunk_size(self, chunk_size: int, chunk_overlap: int) -> None:
        """Update chunk size and overlap, then reinitialize splitter."""
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
