from typing import List, Dict, Tuple


class Retriever:
    """Retrieves relevant document chunks based on query embeddings."""
    
    def __init__(self, vector_store, embedding_manager, top_k: int = 5):
        """
        Initialize the retriever.
        
        Args:
            vector_store: VectorStore instance.
            embedding_manager: EmbeddingManager instance.
            top_k: Number of documents to retrieve.
        """
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager
        self.top_k = top_k
    
    def retrieve(self, query: str) -> Tuple[List[dict], List[Tuple[str, int]]]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: User's question or search query.
        
        Returns:
            Tuple of (retrieved documents list, sources list of (filename, page_number))
        """
        # Embed the query
        query_embedding = self.embedding_manager.embed_query(query)
        
        # Search the vector store
        retrieved_docs = self.vector_store.search(query_embedding, top_k=self.top_k)
        
        # Extract unique sources (filename + page number)
        sources = set()
        for doc in retrieved_docs:
            filename = doc.get('filename', 'Unknown')
            page_number = doc.get('page_number', 1)
            sources.add((filename, page_number))
        
        sources_list = sorted(list(sources))
        
        return retrieved_docs, sources_list
    
    def format_context(self, retrieved_docs: List[dict]) -> str:
        """
        Format retrieved documents into a context string for the LLM.
        
        Args:
            retrieved_docs: List of retrieved document chunks.
        
        Returns:
            Formatted context string.
        """
        context_parts = []
        
        for idx, doc in enumerate(retrieved_docs, 1):
            filename = doc.get('filename', 'Unknown')
            page_number = doc.get('page_number', 1)
            text = doc.get('text', '')
            
            header = f"[Document {idx}: {filename} - Page {page_number}]"
            context_parts.append(f"{header}\n{text}")
        
        return "\n\n".join(context_parts)
    
    def format_sources(self, sources: List[Tuple[str, int]]) -> str:
        """
        Format sources for display.
        
        Args:
            sources: List of (filename, page_number) tuples.
        
        Returns:
            Formatted sources string.
        """
        if not sources:
            return "No sources found."
        
        formatted = "**Sources:**\n"
        for filename, page_number in sources:
            formatted += f"📄 {filename} — Page {page_number}\n"
        
        return formatted
