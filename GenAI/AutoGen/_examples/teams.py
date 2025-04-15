from autogen_agentchat.agents import (
    AssistantAgent,
    UserProxyAgent,
)
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination
from autogen_agentchat.teams import (
    RoundRobinGroupChat,
    SelectorGroupChat, 
    MagenticOneGroupChat
)
from autogen_agentchat.ui import Console

from autogen_core import CancellationToken
from autogen_core.tools import FunctionTool

from autogen_ext.tools.langchain import LangChainToolAdapter

from _examples.models import get_ollama_client
from _tools._prompts.basic_prompts import (
    generate_web_researcher_prompt,
    generate_critic_agent_prompt,
)

from langchain_community.tools import TavilySearchResults

import asyncio
from dotenv import load_dotenv

load_dotenv()

async def web_research_rr_team(
    client,
    task: str,
):
    """
    Coordinates a web research task using multiple agents.

    Args:
        client: The model client used for running model tasks.
        task: A description of the web research task to be performed.
    """

    # Initialize the web search tool to retrieve search results
    web_tool = LangChainToolAdapter(TavilySearchResults(max_results=1))
    
    # Create the assistant agent responsible for web research
    web_researcher = AssistantAgent(
        name="web_researcher",
        description="Responsible for performing web searches and returning findings.",
        model_client=client,
        system_message=generate_web_researcher_prompt(),
        tools=[web_tool],
        model_client_stream=True,
        reflect_on_tool_use=True,
    )

    # Create the critic agent to assess and provide feedback on the researcher's findings
    critic = AssistantAgent(
        name="critic",
        description="Evaluates and provides feedback on the web researcher's findings.",
        model_client=client,
        system_message=generate_critic_agent_prompt(), 
        model_client_stream=True,
    )
    
    # Create a user proxy agent to interact with the user through console input
    user_proxy = UserProxyAgent("user_proxy", input_func=input)
    
    # Termination condition to end the task upon critic's approval
    text_termination = TextMentionTermination("APPROVE")
    
    # Assemble the agents into a round-robin communication group
    group_chat = RoundRobinGroupChat(
        participants=[web_researcher, critic, user_proxy],
        max_turns=10,
        termination_condition=text_termination,
    )

    # Run the group chat asynchronously with console output
    await Console(
        group_chat.run_stream(
            task=task,
        )
    )
    
    # Close the agents to free up resources
    await web_researcher.close()
    await critic.close()
    await user_proxy.close()


def add(a: int, b: int) -> int:
    """
    Adds two numbers together.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    
    return a + b

def multiply(a: int, b: int) -> int:
    """
    Multiplies two numbers together.
    
    Args:
        a (int): The first number.
        b (int): The second number.
        
    Returns:
       int: The product of the two numbers.
    """
    
    return a * b

async def calculator_sg_team(
    client,
    task: str,
):
    """
    Coordinates a mathematical calculation task using specialized agents.
    
    This function sets up a SelectorGroupChat with specialized agents for
    different mathematical operations (addition and multiplication).
    The selector chat dynamically chooses which agent should respond based
    on the nature of the mathematical task.

    Args:
        client: The model client used for running model tasks.
        task (str): A description of the mathematical calculation to be performed.

    Returns:
        None: The function outputs the conversation to the console.
    """

    # Create function tools for basic calculator operations
    add_tool = FunctionTool(add, description="Adds two numbers together.", strict=True)
    multiply_tool = FunctionTool(multiply, description="Multiplies two numbers together.", strict=True)

    # Create specialized agent for addition operations
    addition_agent = AssistantAgent(
        name="add",
        model_client=client,
        tools=[add_tool, multiply_tool],
        description="Specialized in performing addition operations.",
        model_client_stream=True,
    )
    
    # Create specialized agent for multiplication operations
    multiplication_agent = AssistantAgent(
        name="multiply",
        model_client=client,
        tools=[multiply_tool],
        description="Specialized in performing multiplication operations.",
        model_client_stream=True,
    )
    
    # Create an agent to reply back the final answer once the task is completed
    reply_agent = AssistantAgent(
        name="reply",
        system_message="Reply with answer and DONE when the task is done.",
        model_client=client,
        model_client_stream=True,
    )

    # Define a termination condition based on text mention
    termination = TextMentionTermination("DONE")
    
    # Create a selector group chat to dynamically choose the appropriate agent
    team = SelectorGroupChat(
        participants=[addition_agent, multiplication_agent, reply_agent],
        model_client=client,
        max_turns=10,               # Limit conversation to n turns
        max_selector_attempts=2,   # Number of attempts to select an agent
        # allow_repeated_speaker=True,  # Uncomment to allow the same agent to speak multiple times
        termination_condition=termination,
    )

    # Run the group chat and display output in the console
    await Console(
        team.run_stream(
            task=task,
            # cancellation_token=CancellationToken(),  # Uncomment to enable cancellation
            ),
        )
    
    
    # Close the agents to free up resources
    await addition_agent.close()
    await multiplication_agent.close()
    await reply_agent.close()

async def main():
    
    client = get_ollama_client('qwen2.5:14b')
  

    # task = "Write a code to print the first 10 numbers in the Fibonacci sequence."
    # task = "Greatest achievements of the year 2021 in the field of Cyber Security."
    # await web_research_rr_team(
    #     client=client,
    #     task=task,
    # )
    
    task = "Calculate: 2 * 11 + 2 * 10."
    await calculator_sg_team(
        client=client,
        task=task,
    )
    
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())