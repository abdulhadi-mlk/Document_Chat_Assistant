import os
from pathlib import Path
import pymupdf
from docx import Document
from typing import List, Tuple


class DocumentLoader:
    """Loads and extracts text from PDF and DOCX files."""
    
    SUPPORTED_FORMATS = {'.pdf', '.docx'}
    MAX_FILE_SIZE_MB = 50
    
    def __init__(self):
        self.documents = []
    
    def validate_file(self, file_path: str) -> Tuple[bool, str]:
        """Validate file type, size, and existence."""
        if not os.path.exists(file_path):
            return False, "File does not exist."
        
        file_ext = Path(file_path).suffix.lower()
        if file_ext not in self.SUPPORTED_FORMATS:
            return False, f"Unsupported file type: {file_ext}. Supported: {self.SUPPORTED_FORMATS}"
        
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > self.MAX_FILE_SIZE_MB:
            return False, f"File size ({file_size_mb:.2f}MB) exceeds {self.MAX_FILE_SIZE_MB}MB limit."
        
        return True, "File is valid."
    
    def load_pdf(self, file_path: str) -> List[dict]:
        """Extract text from PDF while preserving page numbers."""
        chunks = []
        try:
            pdf_document = pymupdf.open(file_path)
            filename = Path(file_path).name
            
            if len(pdf_document) == 0:
                return []
            
            for page_num, page in enumerate(pdf_document, start=1):
                text = page.get_text()
                
                if text.strip():
                    chunks.append({
                        'text': text,
                        'filename': filename,
                        'file_type': 'PDF',
                        'page_number': page_num,
                        'metadata': {
                            'source': filename,
                            'page': page_num,
                            'file_type': 'PDF'
                        }
                    })
            
            pdf_document.close()
        except Exception as e:
            raise Exception(f"Error loading PDF {file_path}: {str(e)}")
        
        return chunks
    
    def load_docx(self, file_path: str) -> List[dict]:
        """Extract text from DOCX while preserving structure."""
        chunks = []
        try:
            doc = Document(file_path)
            filename = Path(file_path).name
            
            if not doc.paragraphs:
                return []
            
            paragraph_num = 0
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    paragraph_num += 1
                    chunks.append({
                        'text': paragraph.text,
                        'filename': filename,
                        'file_type': 'DOCX',
                        'page_number': 1,  # DOCX doesn't have pages, use section/paragraph
                        'metadata': {
                            'source': filename,
                            'paragraph': paragraph_num,
                            'file_type': 'DOCX'
                        }
                    })
        except Exception as e:
            raise Exception(f"Error loading DOCX {file_path}: {str(e)}")
        
        return chunks
    
    def load_document(self, file_path: str) -> List[dict]:
        """Load document based on file type."""
        is_valid, message = self.validate_file(file_path)
        if not is_valid:
            raise ValueError(message)
        
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return self.load_pdf(file_path)
        elif file_ext == '.docx':
            return self.load_docx(file_path)
        
        return []
    
    def load_multiple_documents(self, file_paths: List[str]) -> Tuple[List[dict], List[str]]:
        """Load multiple documents and return documents + error list."""
        all_documents = []
        errors = []
        
        for file_path in file_paths:
            try:
                documents = self.load_document(file_path)
                if not documents:
                    errors.append(f"{Path(file_path).name}: Empty or scanned PDF (no extractable text).")
                else:
                    all_documents.extend(documents)
            except Exception as e:
                errors.append(f"{Path(file_path).name}: {str(e)}")
        
        return all_documents, errors
