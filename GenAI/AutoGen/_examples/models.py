from autogen_core.models import UserMessage, AssistantMessage, SystemMessage, LLMMessage, CreateResult
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
    
    return OllamaChatCompletionClient(
        model = model,
        host = host,
        # response_format = response_format, # Uncomment this when you want to set the output to a Structured Type
        timeout = timeout,
        model_capabilities = model_capabilities,
        options = options,
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
    
    return OpenAIChatCompletionClient(
        model = model,
        # api_key = api_key, # Use this if the GEMINI_API_KEY is not loaded as an env variable
        # response_format = response_format, # Uncomment this when you want to set the output to a Structured Type
        timeout = timeout,
        model_capabilities = model_capabilities,
        options = options,
    )

async def llm_with_streaming(
    client: Union[OllamaChatCompletionClient, OpenAIChatCompletionClient],
    messages: List[LLMMessage],
) -> None:
    
    # Create a stream.
    stream = client.create_stream(messages=messages)

    # Iterate over the stream and print the responses.
    print("Streamed responses:")
    async for chunk in stream:  # type: ignore
        if isinstance(chunk, str):
            # The chunk is a string.
            print(chunk, end = "", flush=True)
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
    
    # Then initialize the CacheStore, in this case with diskcache.Cache.
    # You can also use redis like:
    # from autogen_ext.cache_store.redis import RedisStore
    # import redis
    # redis_instance = redis.Redis()
    # cache_store = RedisCacheStore[CHAT_CACHE_VALUE_TYPE](redis_instance)
    cache_store = DiskCacheStore[CHAT_CACHE_VALUE_TYPE](Cache("./_data/_tmp"))
    cache_client = ChatCompletionCache(client, cache_store)

    response = await cache_client.create(messages)
    print(response)  # Should print response from LLM
    response = await cache_client.create(messages)
    print(response)  # Should print cached response

    await cache_client.close()

async def llm_with_history(
    client: Union[OllamaChatCompletionClient, OpenAIChatCompletionClient],
    messages: List[LLMMessage],
    follow_up_query: str,
) -> None:
    
    # Call for response for the first query
    response = await client.create(messages)
    # Add the response as an assistant message and follow up query as User message
    messages.append(AssistantMessage(content=response.content, source = "assistant"))
    messages.append(UserMessage(content=follow_up_query, source='user'))
    # Invoke the LLM with the history and the new query
    response = await client.create(messages)
    # Store the final response
    messages.append(AssistantMessage(content=response.content, source = "assistant"))
    
    print(messages)
    
class StructuredOutput(BaseModel):
    answer: str
    reason: str

async def llm_with_struct_output(
    client: Union[OllamaChatCompletionClient, OpenAIChatCompletionClient],
    messages: List[LLMMessage],
) -> None:
    
    response = await client.create(messages)
    assert isinstance(response.content, str)
    parsed_response = StructuredOutput.model_validate_json(response.content)
    # print(parsed_response)
    print(f"> Response: {parsed_response.answer}")
    print(f"> Reasoning: {parsed_response.reason}")
    
    print(f"> Usage: {response.usage}")

async def main():
    
    messages = [
        SystemMessage(content = "You are a helpful assistant."),
        UserMessage(content = "Give me top 3 tools to scan an IP for open ports?", source="user"),
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
    
    
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())