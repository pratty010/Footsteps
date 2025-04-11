from langchain_core.tools import tool, ToolException
from langchain_core.tools import StructuredTool, BaseTool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage, BaseMessage

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from langchain.chat_models import init_chat_model

from rich import print
from typing import List, Dict
import json


# Define the tool using the @tool decorator
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    try:
       return a * b
    except Exception:
        raise ToolException(f"Error multiplying {a} and {b}")


# Define the tool using the StructuredTool class
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

add_tool = StructuredTool.from_function(
    func=add,
    description="Add two numbers",
    handle_tool_error=True,
    )


# Define the tool using the Langchain tool integration
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)


# Define the LLM with tools
tools = [multiply, add_tool, wiki_tool]

# Print the tools details
for tool in tools:
    print(tool.name, tool.description, tool.args, sep="\n", end="\n\n")

# Initialize the LLM
local_model = init_chat_model('ollama:qwen2.5:14b')
# google_model = init_chat_model('google_genai:gemini-2.0-flash')

# Bind the tools to the LLM
llm_with_tools = local_model.bind_tools(
    tools=tools,
    tool_choice="any"  # Use "required" if you want to force the model to use a tool
    )
# llm_with_tools = google_model.bind_tools(tools)

def simple_tool_usage(query: str) -> List[BaseMessage]:
    """
    Execute a simple flow of tool usage with LLM.

    Args:
        query: The user query to process

    Returns:
        The final AI response after tool execution
    """

    # Create an initial list of messages
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=query)
    ]

    # Invoke the initial query
    ai_msg = llm_with_tools.invoke(messages)
    # print(ai_msg.tool_calls)
    messages.append(ai_msg) # Add the AI message to the messages list
    # print(messages)
    
    # Invoke the tools separately and add the results to the messages list
    for tool_call in ai_msg.tool_calls:
        # print(tool_call)
        selected_tool = {"multiply": multiply, "add": add_tool, "wiki": wiki_tool}[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)
    print(messages)

    # Invoke the model again with the updated messages list with tool calls
    res = llm_with_tools.invoke(messages)

    return res

def call_tools(msg: AIMessage) -> List[Dict]:
    """
    Execute tool calls sequentially.

    Args:
        msg: The AI message containing tool calls

    Returns:
        List of executed tool calls with their outputs
    """
    tool_map = {tool.name: tool for tool in tools}
    tool_calls = msg.tool_calls.copy()
    for tool_call in tool_calls:
        tool_call["output"] = tool_map[tool_call["name"]].invoke(tool_call["args"])
    return tool_calls

class NotApproved(Exception):
    """Custom exception for when tool invocations are not approved."""
    pass

def human_approval(msg: AIMessage) -> AIMessage:
    """
    Requests human approval for tool invocations.

    Args:
        msg: Output from the chat model containing tool calls

    Returns:
        Original message if approved

    Raises:
        NotApproved: If the user doesn't approve the tool invocations
    """
    tool_strs = "\n\n".join(
        json.dumps(tool_call, indent=2) for tool_call in msg.tool_calls
    )
    input_msg = (
        f"Do you approve of the following tool invocations\n\n{tool_strs}\n\n"
        "Anything except 'Y'/'Yes' (case-insensitive) will be treated as a no.\n >>>"
    )
    resp = input(input_msg)
    if resp.lower() not in ("yes", "y"):
        raise NotApproved(f"Tool invocations not approved:\n\n{tool_strs}")
    return msg

def main():
    """Main function to demonstrate tool usage flows."""
    
    query = "What is 3 * 12? Also, what is 11 + 49?"
    
    # # Simple tool usage without any approval
    # result = simple_tool_usage(query)
    
    # Tool usage with approval
    chain = llm_with_tools | human_approval | call_tools
    result = chain.invoke(query)
    
    print(result)
    

if __name__ == "__main__":
    main()