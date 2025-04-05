from agents import (
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    Model,
    ModelProvider,
    set_tracing_disabled,
    ModelSettings,
    Agent,
    RunConfig,
    Runner,
    function_tool,
    FunctionTool,
    RunContextWrapper,
    handoff,
)

from agents.extensions.visualization import draw_graph

from openai.types.responses import ResponseTextDeltaEvent

from pydantic import BaseModel, Field
import asyncio
import os
from dotenv import load_dotenv

from rich import print
import json

load_dotenv()
BASE_URL = os.getenv("BASE_URL") or ""
API_KEY = os.getenv("API_KEY") or ""
MODEL_NAME = os.getenv("MODEL_NAME") or ""

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set EXAMPLE_BASE_URL, EXAMPLE_API_KEY, EXAMPLE_MODEL_NAME via env var or code."
    )

# setup the client to use a local model provider client - Ollama
client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    max_retries=2,
    timeout=120,
)
set_tracing_disabled(disabled=True) # Set tracing to off

# Intialize the Local Model Provider to be used by defult in run contexts
class LocalModelProvider(ModelProvider):
    def get_model(self, model_name: str | None) -> Model:
        return OpenAIChatCompletionsModel(model=model_name or MODEL_NAME, openai_client=client)
LOCAL_MODEL_PROVIDER = LocalModelProvider()

# Define a pydanctic object for output
class Info(BaseModel):
    first_name : str
    last_name : str
    location : str


# Define a dummy tool
@function_tool  
async def fetch_weather(location: str) -> str:
    
    """
    Fetch the weather for a given location.

    Args:
        location: The location to fetch the weather for.
    """
    # In real life, we'd fetch the weather from a weather API
    return "sunny"


async def main():

    # Initialize Basic assistant agent with LOCAL MODEL PROVIDER
    agent = Agent(
        name = "Assistant",
        instructions= "Help user with all it's needs.",
        model_settings = ModelSettings(temperature = 0.3, max_tokens=2000),
    )

    # Define a agent with a pydantic object output type
    info_agent = Agent(
        name = "Info Extractor",
        instructions= "Extract User Information from the text.",
        output_type=Info,
    )
    
    # Define a tool agent with a basic weather call tool
    tool_agent = Agent(
        name = "Tooler",
        instructions="Use all the tools at your disposal.",
        tools=[fetch_weather,],
    )

    # # Too see all the tools at agent's disposal
    # for tool in tool_agent.tools:
    #     if isinstance(tool, FunctionTool):
    #         print(tool.name)
    #         print(tool.description)
    #         print(json.dumps(tool.params_json_schema, indent=2))
    #         print()


    # For normal output - all at once
    print("-" * 80)
    print("> Normal output:")
    print("-" * 80)
    result = await Runner.run(
        # agent,
        # info_agent,
        tool_agent,
        # "What are all the known planets in our solar system?",
        # "My name is Trap Singh. I am located in New York.",
        "How is the weather in antartica?",
        run_config=RunConfig(model_provider=LOCAL_MODEL_PROVIDER),
        )
    # print(result.final_output)
    print(result)
    print("-" * 80)


    # # For streaming out the output
    # result = Runner.run_streamed(
    #     agent,
    #     input="What are all the known planets in our solar system?.",
    #     run_config=RunConfig(model_provider=LOCAL_MODEL_PROVIDER),
    # )
    
    # print("-" * 80)
    # print("> Streamed output:")
    # print("-" * 80)
    # async for event in result.stream_events():
    #     if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
    #         print(event.data.delta, end="", flush=True)
    # print()
    # print("-" * 80)


if __name__ == "__main__":
    asyncio.run(main())