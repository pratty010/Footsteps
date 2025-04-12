from agents import (
    AsyncOpenAI,
    set_default_openai_client,
    set_default_openai_api,
    set_tracing_disabled,
    ModelSettings,
    Agent,
    RunConfig,
    Runner,
    function_tool,
    FunctionTool,
    RunContextWrapper,
    handoff
)

from openai.types.responses import ResponseTextDeltaEvent
from agents.extensions.visualization import draw_graph

from typing import List, Optional
from pydantic import BaseModel, Field

import asyncio
import os
import json
from rich import print
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API credentials from environment variables
BASE_URL = os.getenv("BASE_URL") or ""
API_KEY = os.getenv("API_KEY") or ""

if not BASE_URL or not API_KEY:
    raise ValueError(
        "Please set BASE_URL, API_KEY via env var or code."
    )

# Initialize OpenAI client
client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    max_retries=2,
    timeout=120,
)
set_tracing_disabled(disabled=True)

# Set the default client and API
set_default_openai_client(client)
set_default_openai_api('chat_completions')


async def basic_agent(model: str, query: str):
    """
    Demonstrates a basic agent with simple prompt and response.
    
    Args:
        model: The model identifier to use
        query: The user query to process
    """
    
    # Initialize the agent
    assistant_agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        model=model,
        model_settings=ModelSettings(
            temperature=0.1, # Change this to tweak the temperature for the model. Range: [0.0, 1.0]
            top_p=None, # Change this to tweak the top_p for the model
            max_tokens=5000, # The maximum number of output tokens to generate.
            frequency_penalty=None, # Change this to tweak the frequency_penalty for the model
            presence_penalty=None, # Change this to tweak the presence_penalty for the model
            tool_choice=None, # Can be one of the following: "auto", "required", "none". Can be set to a tool specifically too.
            parallel_tool_calls=None, #
            truncation=None, # Can be one of the following: "auto", "disabled", "none"
            reasoning=None, # Has to set for the reasoning model. Can be one of the following: {"effort": "low"}, {"effort": "high"}, {"effort": "medium"}
            metadata=None,
            store=None,
            ),
        )
    
    # Run the agent with the query in a single turn
    # response = await Runner.run(
    #     starting_agent=assistant_agent,
    #     input=query,
    #     max_turns=1,
    # )

    # print(response.final_output)

    # Run the agent with the query in a streamed manner
    response = Runner.run_streamed(
        starting_agent=assistant_agent,
        input=query,
        max_turns=1,
    )
    
    # Stream the response tokens as they're generated
    async for event in response.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
    print("\n")


async def agent_with_history(model: str, queries: List[str] = None):
    """
    Demonstrates an agent that maintains conversation history across multiple turns.

    Args:
        model: The model identifier to use
        queries: List of sequential user queries to process
    """

    agent = Agent(
        name="Assistant",
        instructions="Reply very concisely.",
        model=model,
    )

    initial_query = queries[0]
    # First turn
    print(f"> Query: {initial_query}")
    result = await Runner.run(agent, queries[0])
    print(f"> Response: {result.final_output}")
    # print(result.to_input_list())

    # Consequent turns
    for query in queries[1:]:
        new_input = result.to_input_list() + [{"role": "user", "content": query}] # This will update the history to the new input
        print(f"> Query: {query}")
        result = await Runner.run(agent, new_input)
        print(f"> Response: {result.final_output}")


class Joke(BaseModel):
    """Joke to tell user."""

    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: Optional[int] = Field(
        default=None,
        description="How funny the joke is, from 1 to 10"
        )

async def agent_with_struct_output(model: str, query: str):
    """
    Demonstrates an agent that produces structured output in the form of a Joke object.

    Args:
        model: The model identifier to use
        query: The user query for a joke
    """
    agent = Agent(
        name="Joker",
        instructions="Write a joke as per user's requirement.",
        model=model,
        output_type=Joke,
    )

    # Run the agent
    response = await Runner.run(
        starting_agent=agent,
        input=query,
        max_turns=1,
    )
    print(response.final_output)
    
    
@function_tool
def add(a: int, b: int) -> int:
    """Add two integers.

    Args:
        a: First integer
        b: Second integer
    """

    print(f"> Add function called with args {a} and {b}")
    return a + b

@function_tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers.

    Args:
        a: First integer
        b: Second integer
    """

    print(f"> Multiply function called with args {a} and {b}")
    return a * b

# List of available tools for the agent
tools = [add, multiply]

async def agent_with_tools(model: str, query: str):
    """
    Demonstrates an agent that can use function tools to solve problems.

    Args:
        model: The model identifier to use
        query: The user query requiring tools to solve
    """

    tool_agent = Agent(
        name="Tooler",
        instructions="Use the tools at your disposal for answering.",
        model=model,
        tools=tools,
        model_settings=ModelSettings(tool_choice="auto")
    )

    # Print the description of tools at disposal
    for tool in tool_agent.tools:
        if isinstance(tool, FunctionTool):
            print(tool.name)
            print(tool.description)
            print(json.dumps(tool.params_json_schema, indent=2))
            print()

    # Run the agent
    response = await Runner.run(
        starting_agent=tool_agent,
        input=query,
    )

    print(response.final_output)


class HandOffData(BaseModel):
    """Data structure for agent handoff information."""
    agent_name: str = Field(description="Name of the handoff agent.")
    reason: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: HandOffData):
    """
    Handler function called when a handoff occurs between agents.

    Args:
        ctx: The run context wrapper
        input_data: HandOff information containing agent name and reason
    """
    print(f"> {input_data.agent_name} agent called with reason: {input_data.reason}")

async def agent_with_handoffs(model: str, query: str = None):
    """
    Demonstrates a triage agent that can hand off to specialist agents.

    Args:
        model: The model identifier to use
        query: The user query to be triaged and answered
    """

    # Initialize the first agent
    maths_tutor_agent = Agent(
        name = "Math Tutor",
        handoff_description="Specialist agent for mathematical questions",
        instructions="You provide help with math problems. Explain your reasoning at each step and include examples.",
        model_settings=ModelSettings(temperature=0.1, max_tokens=5000),
        model=model,
    )

    # Initialize the second agent
    history_tutor_agent = Agent(
        name="History Tutor",
        handoff_description="Specialist agent for historical questions",
        instructions="You provide assistance with historical queries. Explain important events and context clearly.",
        model_settings=ModelSettings(temperature=0.5, max_tokens=5000),
        model=model,
    )

    # Initialize the triage agent
    triage_agent = Agent(
        name="Triage Agent",
        instructions="You determine which agent to use based on the user's homework question",
        model=model,
        handoffs=[
            handoff(maths_tutor_agent, on_handoff=on_handoff, input_type=HandOffData),
            handoff(history_tutor_agent, on_handoff=on_handoff, input_type=HandOffData)
            ],
        # model_settings=ModelSettings(temperature=0.1, max_tokens=5000),
    )

    # # Draw the agent graph for debugging purposes
    # draw_graph(triage_agent, "./graphs/triage_agent_graph")

    result = await Runner.run(
        triage_agent,
        query,
        )
    print(f"Response >\n{result.final_output}")


async def main():
    """
    Main entry point for the application that demonstrates various agent capabilities.
    """
    
    # Choose which model to use for the examples
    # model = "deepseek-r1:14b"
    model = "qwen2.5:14b"
    # model = "llama3.2:3b"
    # model = "qwen2.5-coder:7b"
    
    # # Example query for basic agent
    # query = """
    # Hi, my name is Ace. I am a software engineer. I am trying to learn about agents.
    # I want to build an agent that can help me with my work. Can you help me with that?
    # """
    # await basic_agent(model, query)

    # # Example queries for agent with history
    # queries = [
    #     "Hello, my name is Ace. I live in the United States. What is the capital of the United States?",
    #     "How far is it from New York?",
    #     "Finally, What is the population of the last city I mentioned?",
    # ]
    # await agent_with_history(model, queries)
    
    # # Example of a agent with a structured output
    # query = "Tell me a joke about cats"
    # await agent_with_struct_output(model, query)
    
    # # Example of a agent with tools
    # query = "Calculate: 3 + 4 * 6."
    # await agent_with_tools(model, query)
    
    # Example of a handoff triage agent
    # query = "Give me the timeline of colonial rule of British in Africa?"
    query = "Help me with calculate sin of all angles in between 0 to 90 degree."
    await agent_with_handoffs(model, query)



if __name__ == "__main__":
    asyncio.run(main())