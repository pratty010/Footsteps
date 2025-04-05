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
    RunContextWrapper,
    handoff
)

from agents.extensions.visualization import draw_graph

import asyncio
import os
from rich import print
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL") or ""
API_KEY = os.getenv("API_KEY") or ""
MODEL_NAME = os.getenv("MODEL_NAME") or ""

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set EXAMPLE_BASE_URL, EXAMPLE_API_KEY, EXAMPLE_MODEL_NAME via env var or code."
    )

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    max_retries=2,
    timeout=120,
)
set_tracing_disabled(disabled=True)

class LocalModelProvider(ModelProvider):
    def get_model(self, model_name: str | None) -> Model:
        return OpenAIChatCompletionsModel(model=model_name or MODEL_NAME, openai_client=client)

CUSTOM_MODEL_PROVIDER = LocalModelProvider()


def on_handoff(ctx: RunContextWrapper[None]):
    print("Handoff called")

async def main():

    # Initialize the first agent
    maths_tutor_agent = Agent(
        name = "Math Tutor",
        handoff_description="Specialist agent for mathematical questions",
        instructions="You provide help with math problems. Explain your reasoning at each step and include examples.",
        model_settings=ModelSettings(temperature=0.1, max_tokens=5000),
    )

    # Initialize the second agent
    history_tutor_agent = Agent(
        name="History Tutor",
        handoff_description="Specialist agent for historical questions",
        instructions="You provide assistance with historical queries. Explain important events and context clearly.",
        model_settings=ModelSettings(temperature=0.5, max_tokens=5000),
    )


    # Initialize the triage agent
    triage_agent = Agent(
        name="Triage Agent",
        instructions="You determine which agent to use based on the user's homework question",
        handoffs=[history_tutor_agent, maths_tutor_agent],
        # model_settings=ModelSettings(temperature=0.1, max_tokens=5000),
    )

    # # Draw the agent graph for debugging purposes
    # draw_graph(triage_agent, "./graphs/triage_agent_graph")

    print("-" * 80)
    result = await Runner.run(
        triage_agent,
        "Give me the timeline of colonial rule of British in Africa? Also, help me explain the basic concepts of trignometry.",
        run_config=RunConfig(model_provider=CUSTOM_MODEL_PROVIDER),
        )
    print(result.final_output)
    print("-" * 80)



if __name__ == "__main__":
    asyncio.run(main())