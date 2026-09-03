import os
from abc import ABC, abstractmethod
from typing import List

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


class EmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Embed a single text."""
        pass

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts."""
        pass


class GeminiEmbeddingProvider(EmbeddingProvider):
    """Google Gemini embedding provider using LangChain."""

    def __init__(self, api_key: str = None, model: str = "models/gemini-embedding-001"):
        ...
        """
        Initialize Gemini embeddings.

        Args:
            api_key: Gemini API key (uses env variables if not provided).
                     Tries GEMINI_API_KEY first, then EMBEDDING_API_KEY.
            model: Embedding model to use.
        """
        self.api_key = (
            api_key
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("EMBEDDING_API_KEY")
        )

        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Set EMBEDDING_API_KEY or GEMINI_API_KEY "
                "environment variable to a valid Gemini API key."
            )

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=model,
            google_api_key=self.api_key
        )

    def embed_text(self, text: str) -> List[float]:
        """Embed a single text using Gemini."""
        return self.embeddings.embed_query(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts using Gemini."""
        return self.embeddings.embed_documents(texts)


class EmbeddingManager:
    """Manages embedding creation and caching."""

    def __init__(self, provider: EmbeddingProvider = None):
        """
        Initialize the embedding manager.

        Args:
            provider: EmbeddingProvider instance (defaults to Gemini).
        """
        if provider is None:
            provider = GeminiEmbeddingProvider()

        self.provider = provider

    def embed_chunks(self, chunks: List[dict]) -> List[dict]:
        """
        Add embeddings to document chunks.

        Args:
            chunks: List of chunk dictionaries with 'text' key.

        Returns:
            List of chunks with added 'embedding' key.
        """
        texts = [chunk['text'] for chunk in chunks]
        embeddings = self.provider.embed_documents(texts)

        for chunk, embedding in zip(chunks, embeddings):
            chunk['embedding'] = embedding

        return chunks

    def embed_query(self, query: str) -> List[float]:
        """Embed a query string."""
        return self.provider.embed_text(query)
