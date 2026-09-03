import os
import chromadb
from typing import List, Dict, Optional


class VectorStore:
    """Manages ChromaDB vector store for document embeddings."""

    def __init__(self, db_path: str = "vectorstore"):
        """
        Initialize ChromaDB vector store.

        Args:
            db_path: Path to persist the vector database.
        """
        os.makedirs(db_path, exist_ok=True)

        # New Chroma client API (v0.4+): PersistentClient handles
        # persistence automatically, no Settings/duckdb config needed.
        self.client = chromadb.PersistentClient(path=db_path)

        self.collection = None
        self.db_path = db_path

    def create_or_get_collection(self, collection_name: str = "documents") -> None:
        """Create or retrieve a collection."""
        # Delete existing collection if it exists (for fresh processing)
        try:
            self.client.delete_collection(name=collection_name)
        except Exception:
            pass

        self.collection = self.client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, chunks: List[dict]) -> None:
        """
        Add document chunks to the vector store.

        Args:
            chunks: List of chunks with 'text', 'embedding', and 'metadata' keys.
        """
        if self.collection is None:
            self.create_or_get_collection()

        ids = []
        embeddings = []
        documents = []
        metadatas = []

        for idx, chunk in enumerate(chunks):
            ids.append(f"doc_{idx}")
            embeddings.append(chunk.get('embedding'))
            documents.append(chunk.get('text'))

            metadata = chunk.get('metadata', {})
            metadatas.append({
                'filename': chunk.get('filename', 'unknown'),
                'page_number': str(chunk.get('page_number', 1)),
                'source': metadata.get('source', 'unknown'),
                'file_type': metadata.get('file_type', 'unknown')
            })

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[dict]:
        """
        Search for similar documents.

        Args:
            query_embedding: Embedding vector of the query.
            top_k: Number of top results to return.

        Returns:
            List of retrieved documents with scores and metadata.
        """
        if self.collection is None:
            return []

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        retrieved_docs = []
        if results and results['documents']:
            for doc_text, metadata, distance in zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            ):
                similarity = 1 - distance

                retrieved_docs.append({
                    'text': doc_text,
                    'metadata': metadata,
                    'filename': metadata.get('filename', 'unknown'),
                    'page_number': int(metadata.get('page_number', 1)),
                    'similarity_score': similarity
                })

        return retrieved_docs

    def get_collection_info(self) -> Dict:
        """Get information about the current collection."""
        if self.collection is None:
            return {'count': 0, 'documents': []}

        try:
            count = self.collection.count()
            return {
                'count': count,
                'collection_name': self.collection.name
            }
        except Exception:
            return {'count': 0}

    def clear_collection(self) -> None:
        """Clear all documents from the current collection."""
        if self.collection is not None:
            try:
                self.client.delete_collection(name=self.collection.name)
                self.collection = None
            except Exception:
                pass

    def persist(self) -> None:
        """
        No-op kept for backward compatibility with existing callers.

        The new PersistentClient writes to disk automatically after
        every write operation (add/delete/etc.) — there is no manual
        persist() step anymore.
        """
        pass