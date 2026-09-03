
import os
from abc import ABC, abstractmethod

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate_answer(self, context: str, query: str) -> str:
        """Generate an answer based on context and query."""
        pass


class GeminiLLMProvider(LLMProvider):
    """Google Gemini LLM provider using LangChain."""

    SYSTEM_PROMPT = """You are a document question-answering assistant.

Answer the user's question using ONLY the information contained in the provided document context.

Do not invent information or use outside knowledge.

If the answer cannot be found in the uploaded documents, clearly say:

"I couldn't find the answer in the uploaded documents."

When possible, mention the document name and page number where the information was found.

Keep answers clear, accurate, and easy to understand.
"""

    def __init__(
        self,
        api_key: str = None,
        model: str = "gemini-3.6-flash"
    ):
        """
        Initialize Gemini LLM.

        Args:
            api_key: Gemini API key. Uses GEMINI_API_KEY, then the legacy
                     LLM_API_KEY environment variable if not provided.
            model: Gemini model to use.
        """

        self.api_key = (
            api_key
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("LLM_API_KEY")
        )

        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. "
                "Please set GEMINI_API_KEY (or LLM_API_KEY) in your .env file."
            )

        self.llm = ChatGoogleGenerativeAI(
            google_api_key=self.api_key,
            model=model,
            temperature=0.2
        )

    def generate_answer(self, context: str, query: str) -> str:
        """Generate an answer using Gemini."""

        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(
                content=f"""Context:
{context}

Question:
{query}
"""
            )
        ]

        response = self.llm.invoke(messages)

        return response.content


class LLMManager:
    """Manages LLM interactions."""

    def __init__(self, provider: LLMProvider = None):
        """
        Initialize the LLM manager.

        Args:
            provider: LLMProvider instance.
            Defaults to Gemini.
        """

        if provider is None:
            provider = GeminiLLMProvider()

        self.provider = provider

    def generate_answer(self, context: str, query: str) -> str:
        """
        Generate an answer for a query using the provided context.

        Args:
            context: Formatted context from retrieved documents.
            query: User's question.

        Returns:
            Generated answer string.
        """

        return self.provider.generate_answer(context, query)
