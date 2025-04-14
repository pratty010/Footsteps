from autogen_core.models import (
    UserMessage,
    AssistantMessage,
    SystemMessage,
    LLMMessage,
    CreateResult,
)

from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.cache_store.diskcache import DiskCacheStore
from autogen_ext.models.cache import CHAT_CACHE_VALUE_TYPE, ChatCompletionCache

from typing import Literal, Optional, Dict, Union, List
from pydantic import BaseModel

import asyncio
from diskcache import Cache
from rich import print
from dotenv import load_dotenv

load_dotenv()


def get_openai_client(
    model: str,
    base_url: str | None = None,
    api_key: str | None = None,
    max_retries: int = 2,
    max_tokens: int = 4096,
    temperature: float = 0.1, 
    timeout: int = 300,
    model_info: Dict = {
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "unknown",
        "structured_output": True,
    },
) -> OpenAIChatCompletionClient:
    """
    Create and configure an OpenAI chat completion client.

    Args:
        model: The name of the OpenAI model to use
        base_url: Optional custom API endpoint
        api_key: Optional API key (otherwise uses environment variable)
        max_retries: Number of retry attempts for failed requests
        max_tokens: Maximum tokens to generate in completion
        temperature: Controls randomness (0 = deterministic, 1 = random)
        timeout: Request timeout in seconds
        model_info: Dictionary of model capabilities

    Returns:
        Configured OpenAIChatCompletionClient instance
    """
    return OpenAIChatCompletionClient(
        model=model,
        base_url=base_url,
        api_key=api_key,
        max_retries=max_retries,
        max_tokens=max_tokens,
        temperature=temperature,
        model_info=model_info,
        timeout=timeout,
    )


def get_ollama_client(
    model: Literal["llama3.2:3b", "qwen2.5:14b", "deepseek-r1:14b", "qwen2.5-coder:7b"] = "qwen2.5-coder:7b",
    host: Optional[str] = "http://localhost:11434/",
    response_format: BaseModel = None,
    timeout: int = 120,
    model_capabilities: Dict = {
        "json_output": True,
        "function_calling": True,
        "vision": False,
        "structured_output": True,
    },
    options: Optional[Dict] = {
        "temperature": 0.0,
        "max_tokens": 4096,
    },
) -> OllamaChatCompletionClient:
    """
    Create and configure an Ollama chat completion client.

    Args:
        model: The Ollama model to use
        host: Ollama API endpoint URL
        response_format: Optional structured output format
        timeout: Request timeout in seconds
        model_capabilities: Dictionary of model capabilities
        options: Dictionary of model-specific parameters

    Returns:
        Configured OllamaChatCompletionClient instance
    """

    return OllamaChatCompletionClient(
        model=model,
        host=host,
        # response_format = response_format, # Uncomment this when you want to set the output to a Structured Type
        timeout=timeout,
        model_capabilities=model_capabilities,
        options=options,
    )


def get_gemini_client(
    model: Literal["gemini-2.0-flash", "gemini-2.5-pro-exp-03-25", "gemini-1.5-flash"] = "gemini-2.0-flash",
    # api_key: Optional[str] = os.getenv("GEMINI_API_KEY"),
    response_format: BaseModel = None,
    timeout: int = 120,
    model_capabilities: Dict = {
        "json_output": True,
        "function_calling": True,
        "vision": False,
        "structured_output": True,
    },
    options: Optional[Dict] = {
        "temperature": 0.0,
        "max_tokens": 4096,
    },
) -> OpenAIChatCompletionClient:
    """
    Create and configure a Gemini model client using OpenAI-compatible interface.

    Args:
        model: The Gemini model to use
        response_format: Optional structured output format
        timeout: Request timeout in seconds
        model_capabilities: Dictionary of model capabilities
        options: Dictionary of model-specific parameters

    Returns:
        Configured OpenAIChatCompletionClient instance for Gemini
    """

    return OpenAIChatCompletionClient(
        model=model,
        # api_key = api_key, # Use this if the GEMINI_API_KEY is not loaded as an env variable
        # response_format = response_format, # Uncomment this when you want to set the output to a Structured Type
        timeout=timeout,
        model_capabilities=model_capabilities,
        options=options,
    )


async def llm_with_streaming(
    client: Union[OllamaChatCompletionClient, OpenAIChatCompletionClient],
    messages: List[LLMMessage],
) -> None:
    """
    Demonstrate streaming responses from an LLM client.
    
    Args:
        client: The LLM client to use for streaming
        messages: List of messages to send to the LLM
    """

    # Create a stream.
    stream = client.create_stream(messages=messages)

    # Iterate over the stream and print the responses.
    print("Streamed responses:")
    async for chunk in stream:  # type: ignore
        if isinstance(chunk, str):
            # The chunk is a string.
            print(chunk, end="", flush=True)
        # Uncomment if you want to print the whole response together at the end.
        else:
            # The final chunk is a CreateResult object.
            assert isinstance(chunk, CreateResult) and isinstance(chunk.content, str)
            # The last response is a CreateResult object with the complete message.
            print("\n\n------------\n")
            print("The complete response:", flush=True)
            print(chunk.content, flush=True)
    print()


async def llm_with_cache(
    client: Union[OllamaChatCompletionClient, OpenAIChatCompletionClient],
    messages: List[LLMMessage],
) -> None:
    """
    Demonstrate caching LLM responses for repeated queries.
    
    Args:
        client: The LLM client to wrap with caching
        messages: List of messages to send to the LLM
    """
    # Initialize the CacheStore using diskcache
    cache_store = DiskCacheStore[CHAT_CACHE_VALUE_TYPE](Cache("./_data/_tmp"))
    cache_client = ChatCompletionCache(client, cache_store)

    # First request will call the LLM
    response = await cache_client.create(messages)
    print(response)  # Should print response from LLM

    # Second request with same messages will return cached response
    response = await cache_client.create(messages)
    print(response)  # Should print cached response

    await cache_client.close()


async def llm_with_history(
    client: Union[OllamaChatCompletionClient, OpenAIChatCompletionClient],
    messages: List[LLMMessage],
    follow_up_query: str,
) -> None:
    """
    Demonstrate maintaining conversation context with follow-up queries.
    
    Args:
        client: The LLM client to use
        messages: Initial list of messages
        follow_up_query: The follow-up question to ask
    """

    # Call for response for the first query
    response = await client.create(messages)

    # Add the response as an assistant message and follow up query as User message
    messages.append(AssistantMessage(content=response.content, source="assistant"))
    messages.append(UserMessage(content=follow_up_query, source='user'))

    # Invoke the LLM with the history and the new query
    response = await client.create(messages)

    # Store the final response
    messages.append(AssistantMessage(content=response.content, source="assistant"))
    
    print(messages)
    

class StructuredOutput(BaseModel):
    """Defines the structure for formatted LLM responses."""
    answer: str
    reason: str


async def llm_with_struct_output(
    client: Union[OllamaChatCompletionClient, OpenAIChatCompletionClient],
    messages: List[LLMMessage],
) -> None:
    """
    Demonstrate getting structured output from an LLM.
    
    Args:
        client: The LLM client configured with a response format
        messages: List of messages to send to the LLM
    """

    response = await client.create(messages)
    assert isinstance(response.content, str)
    parsed_response = StructuredOutput.model_validate_json(response.content)
    # print(parsed_response)
    print(f"> Response: {parsed_response.answer}")
    print(f"> Reasoning: {parsed_response.reason}")
    
    print(f"> Usage: {response.usage}")


async def main():
    """Main function to demonstrate various LLM interaction patterns."""
    
    # Define the base conversation
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="Give me top 3 tools to scan an IP for open ports?", source="user"),
    ]
    
    # Use case for a normal LLM call - normal or streamed
    client = get_ollama_client('llama3.2:3b')
    # client = get_gemini_client('gemini-1.5-flash')
    response = await client.create(messages)
    assert isinstance(response.content, str)
    print(f"> Response: {response.content}")
    print(f"> Usage: {response.usage}")
    
    # Use case for LLM with streamed output
    await llm_with_streaming(client, messages)
    
    # Use case for LLM to cache your past queries and results.
    await llm_with_cache(client, messages)
    
    # Use Case for LLM with history 
    follow_up_query = "Give me some common command lines for the 2nd tool."
    await llm_with_history(client, messages, follow_up_query)
    
    # # Use Case for LLM call with Structured Output
    # client = get_ollama_client('llama3.2:3b', response_format=StructuredOutput)
    # # client = get_gemini_client('gemini-1.5-flash', response_format=StructuredOutput)
    # await llm_with_struct_output(
    #     client,
    #     messages
    # )
    
    # Clean up resources
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())