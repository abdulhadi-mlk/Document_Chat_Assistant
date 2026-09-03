from typing import List, Tuple


class ChatManager:
    """Manages chat history and conversation context."""
    
    def __init__(self, retriever, llm_manager):
        """
        Initialize the chat manager.
        
        Args:
            retriever: Retriever instance for document retrieval.
            llm_manager: LLMManager instance for answer generation.
        """
        self.retriever = retriever
        self.llm_manager = llm_manager
        self.conversation_history = []  # List of (role, message) tuples
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.conversation_history.append((role, content))
    
    def get_conversation_context(self) -> str:
        """Get formatted conversation history (for reference)."""
        context_parts = []
        for role, content in self.conversation_history:
            role_label = "User" if role == "user" else "Assistant"
            context_parts.append(f"{role_label}: {content}")
        
        return "\n\n".join(context_parts)
    
    def process_query(self, query: str) -> Tuple[str, str, List[Tuple[str, int]]]:
        """
        Process a user query and generate a response.
        
        Args:
            query: User's question.
        
        Returns:
            Tuple of (answer, context_used, sources)
        """
        # Retrieve relevant documents
        retrieved_docs, sources = self.retriever.retrieve(query)
        
        # Format context
        if retrieved_docs:
            context = self.retriever.format_context(retrieved_docs)
        else:
            context = "No relevant documents found."
        
        # Generate answer
        try:
            answer = self.llm_manager.generate_answer(context, query)
        except Exception as e:
            answer = f"Error generating answer: {str(e)}"
        
        # Add to conversation history
        self.add_message("user", query)
        self.add_message("assistant", answer)
        
        return answer, context, sources
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []
    
    def get_history(self) -> List[Tuple[str, str]]:
        """Get the full conversation history."""
        return self.conversation_history.copy()
