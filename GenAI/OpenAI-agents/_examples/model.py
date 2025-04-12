"""
Example script demonstrating different ways to configure and use LLM agents.

This script showcases three approaches:
1. Using an OpenAI client directly
2. Using global settings
3. Using a custom model provider with local settings
"""

from agents import (
    AsyncOpenAI,
    set_default_openai_client,
    set_default_openai_api,
    set_tracing_disabled,
    OpenAIChatCompletionsModel,
    Model,
    ModelProvider,
    ModelSettings,
    Agent,
    RunConfig,
    Runner,
)

import asyncio
import os
from dotenv import load_dotenv
from rich import print

# Load environment variables from .env file
load_dotenv()

# Get the environment variables and check if they are set properly
BASE_URL = os.getenv("BASE_URL") or ""
API_KEY = os.getenv("API_KEY") or ""
MODEL_NAME = os.getenv("MODEL_NAME") or ""

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set EXAMPLE_BASE_URL, EXAMPLE_API_KEY, EXAMPLE_MODEL_NAME via env var or code."
    )

# Initialize the external client with the provided API key, base URL, and other settings
external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    max_retries=2,
    timeout=120,
)

# Disable tracing for the agents library
set_tracing_disabled(disabled=True)


async def llm_with_openai_client():
    """
    Demonstrate using an agent with a direct OpenAI client configuration.
    
    This approach creates an agent and runs it with default settings.
    """
    agent = Agent(
        name="Assistant",
        instructions="Help the user with their travel plans.",
        model=MODEL_NAME,
    )
    
    # This will allow to use the OpenAI client directly or client set with global settings
    result = await Runner.run(
        starting_agent=agent,
        input="What's the best way to travel from New Delhi to New York?",
        max_turns=1,
    )
    
    print(result.final_output)

# Uncomment to set Global Settings: Set the default OpenAI client and API for the agents library
set_default_openai_client(external_client, use_for_tracing=False)
set_default_openai_api('chat_completions')
 
async def llm_with_global_settings(model: str):
    """
    Demonstrate using an agent with global settings.
    
    This approach leverages globally configured settings while overriding
    specific model settings like temperature and max_tokens.
    """
    agent = Agent(
        name="Assistant",
        instructions="Help the user with their travel plans.",
        model=model,
        model_settings=ModelSettings(temperature=0.1, max_tokens=5000), # This will override the default settings for the model settings.
    )

    # This will allow to use the OpenAI client directly or client set with global settings
    result = await Runner.run(
        starting_agent=agent,
        input="What's the best way to travel from New Delhi to New York?",
        max_turns=1,
    )
    
    print(result.final_output)

# Uncomment to set a Custom Model Provider with Local Settings: Define a custom model provider that uses the external client for model inference
class CustomModelProvider(ModelProvider):
    """Custom model provider that uses the external client for model inference."""
    def get_model(self, model_name: str | None) -> Model:
        """
        Return a model instance configured with the external client.

        Args:
            model_name: Name of the model to use, falls back to MODEL_NAME if None

        Returns:
            A configured OpenAIChatCompletionsModel instance
        """
        return OpenAIChatCompletionsModel(
            model = model_name,
            openai_client = external_client,
        )

CUSTOM_MODEL_PROVIDER = CustomModelProvider()

async def llm_with_local_settings(model: str):
    """
    Demonstrate using an agent with a custom model provider via local settings.
    
    This approach configures the model provider at runtime through RunConfig.
    """
    agent = Agent(
        name="Assistant",
        instructions="Help the user with their travel plans.",
    )
    
    # This will use the custom model provider
    result = await Runner.run(
        starting_agent=agent,
        input="What's the best way to travel from New Delhi to New York?",
        max_turns=1,
        run_config=RunConfig(model_provider=CUSTOM_MODEL_PROVIDER, model=model),
    )
    
    print(result.final_output)

async def main():
    """Main entry point that demonstrates different configuration approaches."""
    
    # model = "deepseek-r1:14b"
    model ="qwen2.5:14b"
    
    # Use the OpenAI client directly or client set with global settings
    await llm_with_global_settings(model)
    
    # # Uncomment to set a Custom Model Provider with Local Settings
    # await llm_with_local_settings(model)
    
    # # Uncomment to use the OpenAI client directly
    # await llm_with_openai_client()
    
if __name__ == "__main__":
    asyncio.run(main())