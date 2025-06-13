"""
Token Usage Tracking Demo

This script demonstrates how to use the TokenUsageTracker to monitor
token usage and estimate costs when using LLMs.
"""

import sys
import os
import asyncio
from pathlib import Path
from tqdm import tqdm

# Add the parent directory to sys.path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from app.core.config import settings
from app.ai.token_tracker import TokenUsageTracker, track_tokens
from app.ai.direct_question_generator import DirectQuestionGenerator
import google.generativeai as genai


# Sample psychological book excerpts of different lengths
SAMPLE_TEXTS = {
    "short": """
    Self-awareness is the ability to recognize and understand one's own thoughts, feelings, and behaviors.
    It is a key component of emotional intelligence and a foundation for personal growth.
    """,
    "medium": """
    Cognitive Behavioral Therapy (CBT) is based on the idea that our thoughts, feelings, and behaviors are interconnected.
    By identifying and challenging negative thought patterns, individuals can change their emotional responses and behaviors.
    CBT has been shown to be effective in treating a variety of mental health conditions, including depression, anxiety,
    and post-traumatic stress disorder. The therapy typically involves working with a therapist to identify negative 
    thought patterns and develop strategies to replace them with more positive and realistic ones.
    """,
    "long": """
    The concept of flow, developed by psychologist Mihaly Csikszentmihalyi, refers to a mental state in which a person 
    is fully immersed and engaged in an activity, with a feeling of energized focus and enjoyment in the process. 
    Flow is characterized by complete absorption in what one is doing, to the point where time seems to disappear and 
    self-consciousness fades away. This state is often described as being "in the zone."

    Research has shown that flow experiences are associated with increased happiness, creativity, and productivity. 
    People who frequently experience flow tend to report higher levels of subjective well-being and life satisfaction. 
    Flow can occur in various activities, from artistic pursuits to sports, work tasks, or even engaging conversations.

    To achieve a flow state, several conditions typically need to be met: First, there must be a clear set of goals and 
    progress. Second, the task at hand should provide immediate feedback. Third, there should be a balance between the 
    perceived challenges of the task and one's perceived skills. If the challenge is too great for one's skill level, 
    anxiety may result. If the challenge is too easy, boredom may set in.

    Understanding and cultivating flow experiences can be valuable for enhancing quality of life, improving performance,
    and finding more enjoyment in daily activities. Many psychological interventions and practices aim to help individuals
    create conditions conducive to experiencing flow more frequently.
    """,
}


class TokenTrackingDemo:
    """Demo for token usage tracking."""

    def __init__(self, model_name=None, log_file="token_demo_usage.jsonl"):
        """Initialize the demo."""
        self.model_name = model_name or settings.LLM_MODEL_NAME
        self.log_file = log_file

        # Initialize token tracker
        self.tracker = TokenUsageTracker(
            model_name=self.model_name, log_file=self.log_file, streaming=True
        )

        # Initialize question generator
        self.question_generator = DirectQuestionGenerator(model_name=self.model_name)

        # Configure Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)

    @track_tokens(TokenUsageTracker(model_name=settings.LLM_MODEL_NAME))
    async def generate_text_with_tracking(self, prompt):
        """Generate text with token tracking."""
        model = genai.GenerativeModel(model_name=self.model_name)
        response = model.generate_content(prompt)
        return response.text

    async def run_demo(self):
        """Run the token tracking demo."""
        print("\n" + "=" * 80)
        print(f"TOKEN USAGE TRACKING DEMO - MODEL: {self.model_name}")
        print("=" * 80)

        # Test different text lengths to show token scaling
        for name, text in tqdm(
            SAMPLE_TEXTS.items(), desc="Testing different text lengths"
        ):
            print(f"\n\nTesting {name.upper()} text sample ({len(text)} characters)")

            # Create prompt
            prompt = f"""
            Based on this psychology excerpt, generate 2 insightful questions:
            
            {text}
            
            Return questions with reasoning and tags.
            """

            # Generate response with tracking
            response = await self.generate_text_with_tracking(prompt)

            # Show brief response preview
            preview = response[:100] + "..." if len(response) > 100 else response
            print(f"\nResponse preview: {preview}")

            # Manual tracking example
            usage_data = await self.tracker.track_usage(
                prompt=prompt,
                response=response,
                metadata={"sample_name": name, "chars": len(text)},
            )

            # Wait a moment to see the results
            await asyncio.sleep(1)

        # Show final summary
        self.tracker.print_summary()
        print(f"\nToken usage log saved to: {self.log_file}")


async def main():
    """Run the token tracking demo."""
    demo = TokenTrackingDemo()
    await demo.run_demo()

    # Calculate example costs
    print("\nExample Token Cost Calculation:")
    print("-" * 40)

    # Define token counts
    counts = [(1000, 500), (10000, 5000), (100000, 50000)]  # Small  # Medium  # Large

    for model in ["gpt-3.5-turbo", "gpt-4", "gemini-1.5-pro", "gemini-2.0-flash"]:
        tracker = TokenUsageTracker(model_name=model, streaming=False)

        print(f"\n{model.upper()} Pricing:")
        for input_tokens, output_tokens in counts:
            cost = tracker.calculate_cost(input_tokens, output_tokens)
            total = input_tokens + output_tokens
            print(
                f"  {total:,} tokens ({input_tokens:,} in, {output_tokens:,} out): ${cost:.4f}"
            )


if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
