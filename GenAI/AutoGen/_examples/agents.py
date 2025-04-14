from autogen_agentchat.agents import (
    AssistantAgent,
    UserProxyAgent,
    SocietyOfMindAgent,
    CodeExecutorAgent,
)

from autogen_agentchat.teams import RoundRobinGroupChat

from autogen_agentchat.messages import (
    ChatMessage,
    TextMessage,
)

from autogen_agentchat.conditions import TextMentionTermination

from autogen_core import CancellationToken
from autogen_core.tools import FunctionTool
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
# from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor

from autogen_agentchat.ui import Console


from typing import List
from pydantic import BaseModel

import asyncio
from rich import print
from dotenv import load_dotenv

from _examples.models import get_ollama_client, get_gemini_client
from _tools.kali_tools import is_binary_installed

load_dotenv()

class StructuredOutput(BaseModel):
    """The response format for the agent as a Pydantic base model."""
    answer: str
    reason: str


async def basic_assistant_agent(
    client,
    messages: List[ChatMessage],
    name: str = "assistant",
    system_message: str = "You are a helpful AI assistant. Solve tasks using your tools. Reply with TERMINATE when all the tasks has been completed.",
    description: str = "An agent that provides assistance with ability to use tools.",
) -> None:
    """
    Creates and invokes a basic assistant agent with the provided client.

    Args:
        client: LLM client to use for the agent
        messages: List of chat messages to send to the agent
        name: Name of the assistant agent
        system_message: System prompt for the assistant
        description: Description of the assistant agent
    """
    # Define a basic assistant agent with the passed client
    assistant = AssistantAgent(
        name=name,
        system_message=system_message,
        description=description,
        model_client=client,
        # output_content_type = StructuredOutput, # Uncomment if you want answer in a particular struct form.
    )
    
    # Invoke the agent
    response = await assistant.on_messages(
        messages,
        CancellationToken(),
    )

    print(f"> Response: {response.chat_message.content}")  # Print out the output
    print(f"> Inner Messages: {response.inner_messages}")  # Print out the internal messages for agent calls
    print(f"> Usage: {response.chat_message.models_usage}")  # Print out the total usage in the agent call

    await assistant.close()


async def agent_with_streaming(
    client,
    messages: List[ChatMessage],
) -> None:
    """
    Creates and invokes an assistant agent with streaming capabilities.
    
    Args:
        client: LLM client to use for the agent
        messages: List of chat messages to send to the agent
    """

    # Define a basic assistant agent with the passed client
    agent = AssistantAgent(
        name="assistant",
        model_client=client,
        model_client_stream=True,
    )
    
    # # Option 1: read each message from the stream (as shown in the previous example).
    # async for message in agent.on_messages_stream(
    #     messages,
    #     cancellation_token=CancellationToken(),
    # ):
    #     print(message)

    # Option 2: use Console to print all messages as they appear.
    await Console(
        agent.on_messages_stream(
            messages,
            cancellation_token=CancellationToken(),
        ),
        output_stats=True,  # Enable stats printing.
    )
    
    await agent.close()


async def agent_with_tools(
    client,
    messages: List[ChatMessage],
) -> None:
    """
    Creates and invokes an assistant agent with access to tools.

    Args:
        client: LLM client to use for the agent
        messages: List of chat messages to send to the agent
    """

    # This step is automatically performed inside the AssistantAgent if the tool is a Python function.
    check_binary_tool = FunctionTool(is_binary_installed, description="Check if a binary is installed on the system", strict=True)

    # # The schema is provided to the model during AssistantAgent's on_messages call.
    # print(check_binary_tool.schema)

    agent = AssistantAgent(
        name="assistant",
        model_client=client,
        tools=[check_binary_tool],
        reflect_on_tool_use=True,
        # output_content_type=StructuredOutput, # Not working: Raise a ticket for the same to AutoGen.
        )
    
    await Console(
        agent.on_messages_stream(
            messages,
            CancellationToken(),
        ),
        output_stats=True,  # Enable stats printing.
    )
    
    await agent.close()
    
    
async def basic_user_proxy_agent() -> None:
    """Creates and invokes a basic user proxy agent that can interact with the user."""

    user_proxy_agent = UserProxyAgent(
        name="user_proxy",
    )
    response = await user_proxy_agent.on_messages(
        [TextMessage(content="What is your name? ", source="user")], cancellation_token=CancellationToken()
    )
    print(f"Your name is {response.chat_message.content}")


async def code_exec_agent(
    messages: List[ChatMessage],
) -> None:
    """
    Creates and invokes a code executor agent that can run code.

    Args:
        messages: List of chat messages to send to the agent
    """

    # Create a code executor agent that uses a Local Terminal to execute code.
    # Better to use Docker Container from class autogen_ext.code_executors.docker for safe exec.
    code_executor = LocalCommandLineCodeExecutor(work_dir="./_data/_code")
    await code_executor.start()

    code_executor_agent = CodeExecutorAgent(
        name="coder",
        code_executor=code_executor,
    )

    await Console(
        code_executor_agent.on_messages_stream(
            messages,
            CancellationToken(),
        ),
        output_stats=True,  # Enable stats printing.
    )

    # Stop the code executor.
    await code_executor.stop()
    
    
async def som_agent(
    client,
    messages: List[ChatMessage],
) -> None:
    """
    Creates and invokes a Society of Mind agent with a writer and critic.
    
    Args:
        client: LLM client to use for the agent
        messages: List of chat messages to send to the agent
    """

    # Create the writer agent
    writer = AssistantAgent(
        "writer",
        model_client=client,
        system_message="You are a writer, write well.",
        model_client_stream=True,
    )

    # Create the critic agent
    critic = AssistantAgent(
        "critic",
        model_client=client,
        system_message="You are an editor, provide critical feedback. Respond with 'APPROVE' if the text addresses all feedbacks.",
        model_client_stream=True,
    )

    # Define termination condition and create a team
    inner_termination = TextMentionTermination("APPROVE")
    inner_team = RoundRobinGroupChat(
        [writer, critic],
        termination_condition=inner_termination,
        max_turns=2,
    )

    # Create the Society of Mind agent with the team
    society_of_mind_agent = SocietyOfMindAgent(
        "society_of_mind",
        team=inner_team,
        model_client=client,
    )

    # Display the conversation with the console
    await Console(
        society_of_mind_agent.on_messages_stream(
            messages,
            CancellationToken(),
        ),
        output_stats=True,  # Enable stats printing.
    )

    # Close all agents
    await writer.close()
    await critic.close()
    await society_of_mind_agent.close()


async def main():
    """Main function to demonstrate agent capabilities."""

    messages = [
        # TextMessage(content="Check if gobuster binary is installed.", source="user",),
        # TextMessage(content="Calculate distance between capitals of India and US. Make assumptions.", source="user",),
#         TextMessage(content='''Print output for this code:
# ```python
# for i in range(10):
#     print(2 * i)
# ```
#                     ''',
#                     source="user",
#                     ),
        TextMessage(content="What are the best 5 achievements in science for the year 2021.", source="user",)
    ]
    
    # Initialize an LLM client
    client = get_ollama_client("qwen2.5:14b")
    # client = get_gemini_client("gemini-1.5-flash")
    
    # Choose which agent type to run
    
    # await basic_assistant_agent(client, messages)
    # await agent_with_streaming(client, messages)
    # await agent_with_tools(client, messages)
    # await agent_with_struct_output(client, messages)
    # await user_proxy_run()
    # await code_exec_agent(messages)
    await som_agent(client, messages)
    
    # Close the client when done
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())