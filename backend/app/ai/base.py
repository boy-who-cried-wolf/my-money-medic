"""
Base AI service module providing common functionality for LLM interactions.
"""

from typing import Dict, Any, Optional
from app.core.config import settings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableSequence

# Import the appropriate LLM based on configuration
if settings.LLM_PROVIDER.lower() == "anthropic":
    from langchain_anthropic import ChatAnthropic as LLM
elif settings.LLM_PROVIDER.lower() == "gemini":
    from langchain_google_genai import ChatGoogleGenerativeAI as LLM
    import google.generativeai as genai

    # Configure the Gemini API
    genai.configure(api_key=settings.GEMINI_API_KEY)
else:
    from langchain_openai import ChatOpenAI as LLM


class BaseAIService:
    """
    Base class for AI services providing common functionality.

    This class handles LLM initialization and provides common methods
    for interacting with language models.
    """

    def __init__(self, model_name: Optional[str] = None, temperature: float = 0.7):
        """
        Initialize the base AI service.

        Args:
            model_name: The LLM model to use (defaults to settings.LLM_MODEL_NAME)
            temperature: Temperature setting for LLM (default: 0.7)
        """
        self.model_name = model_name or settings.LLM_MODEL_NAME
        self.temperature = temperature

        # Initialize the language model with provider-specific settings
        if settings.LLM_PROVIDER.lower() == "gemini":
            self.llm = LLM(
                model=self.model_name,
                temperature=self.temperature,
                google_api_key=settings.GEMINI_API_KEY,
                convert_system_message_to_human=True,  # Gemini doesn't support system messages directly
            )
        else:
            self.llm = LLM(
                model=self.model_name,
                temperature=self.temperature,
            )

    def create_chain(self, prompt_template: PromptTemplate) -> RunnableSequence:
        """
        Create a chain with the configured LLM.

        Args:
            prompt_template: The PromptTemplate to use for the chain

        Returns:
            A runnable sequence for generation
        """
        return prompt_template | self.llm

    async def generate(self, chain: RunnableSequence, **kwargs) -> str:
        """
        Generate text using the provided chain and parameters.

        Args:
            chain: The chain to use for generation
            **kwargs: Parameters to pass to the chain

        Returns:
            The generated text
        """
        return await chain.ainvoke(kwargs)

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current LLM configuration.

        Returns:
            Dictionary with model details
        """
        return {
            "provider": settings.LLM_PROVIDER,
            "model": self.model_name,
            "temperature": self.temperature,
        }
