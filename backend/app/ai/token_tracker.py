"""
Token Usage Tracker for LLM API calls.

This module provides tools to track token usage and estimate costs when using
language models like OpenAI's GPT or Google's Gemini.
"""

import os
import json
import time
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime
import tiktoken
from tqdm.auto import tqdm
import google.generativeai as genai
from app.core.config import settings


class TokenUsageTracker:
    """Tracks token usage and costs for various LLM APIs."""

    # Approximate token counts per character for different languages
    TOKENS_PER_CHAR = {
        "english": 0.25,  # ~4 chars per token for English
        "chinese": 1.0,  # ~1 char per token for Chinese
        "japanese": 0.8,  # ~1.25 chars per token for Japanese
        "korean": 0.7,  # ~1.4 chars per token for Korean
        "other": 0.3,  # Conservative estimate for other languages
    }

    # Cost per 1K tokens in USD for different models (input/output)
    COST_PER_1K_TOKENS = {
        # OpenAI models
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        # Google Gemini models
        "gemini-pro": {"input": 0.000125, "output": 0.000375},
        "gemini-1.5-pro": {"input": 0.0005, "output": 0.0015},
        "gemini-1.5-flash": {"input": 0.000125, "output": 0.000375},
        "gemini-2.0-pro": {"input": 0.0007, "output": 0.0021},
        "gemini-2.0-flash": {"input": 0.00017, "output": 0.00051},
        # Latest Gemini 2.5 models with optimized pricing
        "gemini-2.5-flash-preview-05-20": {"input": 0.00015, "output": 0.0006},
        "gemini-2.5-pro-preview-05-06": {"input": 0.001, "output": 0.003},
    }

    def __init__(
        self,
        model_name: str = None,
        log_file: str = "token_usage.jsonl",
        streaming: bool = True,
    ):
        """
        Initialize token tracker.

        Args:
            model_name: Name of LLM model to track
            log_file: Path to log file for token usage
            streaming: Whether to stream token usage to console
        """
        self.model_name = model_name or settings.LLM_MODEL_NAME
        self.log_file = log_file
        self.streaming = streaming
        self.usage_log = []
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0

        # Set up tokenizer
        if "gpt" in self.model_name.lower():
            # Get the appropriate OpenAI tokenizer
            if "gpt-4" in self.model_name:
                self.tokenizer = tiktoken.encoding_for_model("gpt-4")
            else:
                self.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
        else:
            # For Gemini, we'll estimate using characters since there's no official tokenizer
            self.tokenizer = None

    def _count_tokens_with_tiktoken(self, text: str) -> int:
        """Count tokens using tiktoken for OpenAI models."""
        if not text:
            return 0
        return len(self.tokenizer.encode(text))

    def _estimate_tokens_by_chars(self, text: str, lang: str = "english") -> int:
        """Estimate token count based on character count for non-OpenAI models."""
        if not text:
            return 0
        chars = len(text)
        tokens_per_char = self.TOKENS_PER_CHAR.get(lang, self.TOKENS_PER_CHAR["other"])
        return int(chars * tokens_per_char)

    def count_tokens(self, text: str, lang: str = "english") -> int:
        """
        Count tokens in text.

        Args:
            text: Text to count tokens for
            lang: Language of text for character-based estimation

        Returns:
            Token count
        """
        if self.tokenizer:
            return self._count_tokens_with_tiktoken(text)
        else:
            return self._estimate_tokens_by_chars(text, lang)

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost based on token usage.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Estimated cost in USD
        """
        model_costs = self.COST_PER_1K_TOKENS.get(
            self.model_name,
            {"input": 0.001, "output": 0.002},  # Default if model not found
        )

        input_cost = (input_tokens / 1000) * model_costs["input"]
        output_cost = (output_tokens / 1000) * model_costs["output"]

        return input_cost + output_cost

    async def track_usage(
        self, prompt: str, response: str, metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Track token usage for a prompt-response pair.

        Args:
            prompt: Input prompt text
            response: Output response text
            metadata: Additional tracking metadata

        Returns:
            Usage data dictionary
        """
        # Count tokens
        input_tokens = self.count_tokens(prompt)
        output_tokens = self.count_tokens(response)

        # Calculate cost
        cost = self.calculate_cost(input_tokens, output_tokens)

        # Create usage record
        timestamp = datetime.now().isoformat()
        usage_data = {
            "timestamp": timestamp,
            "model": self.model_name,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "estimated_cost_usd": cost,
        }

        # Add metadata if provided
        if metadata:
            usage_data["metadata"] = metadata

        # Update totals
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_cost += cost

        # Add to log
        self.usage_log.append(usage_data)

        # Save to log file
        with open(self.log_file, "a") as f:
            f.write(json.dumps(usage_data) + "\n")

        # Stream to console if enabled
        if self.streaming:
            self._stream_usage(usage_data)

        return usage_data

    def _stream_usage(self, usage_data: Dict[str, Any]) -> None:
        """Stream usage data to console."""
        print("\n" + "=" * 50)
        print(f"TOKEN USAGE - {usage_data['timestamp']}")
        print(f"Model: {self.model_name}")
        print(f"Input tokens: {usage_data['input_tokens']}")
        print(f"Output tokens: {usage_data['output_tokens']}")
        print(f"Total tokens: {usage_data['total_tokens']}")
        print(f"Estimated cost: ${usage_data['estimated_cost_usd']:.6f}")
        print("=" * 50)

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of total token usage and costs."""
        return {
            "model": self.model_name,
            "total_calls": len(self.usage_log),
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost_usd": self.total_cost,
            "log_file": self.log_file,
        }

    def print_summary(self) -> None:
        """Print summary of token usage and costs."""
        summary = self.get_summary()
        print("\n" + "=" * 50)
        print("TOKEN USAGE SUMMARY")
        print(f"Model: {summary['model']}")
        print(f"Total API calls: {summary['total_calls']}")
        print(f"Total input tokens: {summary['total_input_tokens']}")
        print(f"Total output tokens: {summary['total_output_tokens']}")
        print(f"Total tokens: {summary['total_tokens']}")
        print(f"Total cost: ${summary['total_cost_usd']:.6f}")
        print("=" * 50)


# Decorator for tracking LLM function calls
def track_tokens(tracker: TokenUsageTracker):
    """
    Decorator to track token usage for a function.

    Args:
        tracker: TokenUsageTracker instance

    Returns:
        Decorated function
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Extract prompt from args or kwargs
            prompt = None
            if len(args) > 0 and isinstance(args[0], str):
                prompt = args[0]
            elif "prompt" in kwargs:
                prompt = kwargs["prompt"]
            elif "text" in kwargs:
                prompt = kwargs["text"]

            # Call the original function
            start_time = time.time()
            result = await func(*args, **kwargs)
            end_time = time.time()

            # Extract response
            response = str(result)

            # Track usage
            metadata = {
                "function": func.__name__,
                "execution_time": end_time - start_time,
                "args": str(args)[:100] if args else None,
            }

            await tracker.track_usage(prompt or "", response, metadata)

            return result

        return wrapper

    return decorator
