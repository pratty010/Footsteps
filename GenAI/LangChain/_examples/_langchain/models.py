from langchain_ollama import OllamaLLM, ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
from langchain.chat_models import init_chat_model

from pydantic import BaseModel, Field
from typing import Literal, Optional, Union
from typing_extensions import Annotated, TypedDict
from rich import print
from dotenv import load_dotenv

load_dotenv()

def init_Ollama_model(
            model: Literal["deepseek-r1:14b", "qwen2.5:14b", "llama3.2:3b"] = "qwen2.5:14b",
            base_url: str = "http://localhost:11434/",
            api_key: str = "SomethingSomething",
            temperature: float = 0.3,
            num_ctx: Literal[-1, -2, 5000] = 5000,
            num_predict: Optional[int] = None,
            format: Optional[str] = None,
            verbose: bool = False,
            extract_reasoning: bool = False,
            type: Literal["LLM", "Chat"] = "Chat",
            ) -> Union[ChatOllama, OllamaLLM]:
    """
    Initialize and configure an Ollama model for text generation or chat completion.

    This function creates either a ChatOllama or OllamaLLM instance based on the specified
    parameters, allowing for customization of model behavior and connection settings.

    Parameters:
        model (Literal["deepseek-r1:14b", "qwen2.5:14b", "llama3.2:3b"]): The Ollama model to use. Defaults to "qwen2.5:14b".
        base_url (str): The URL of the Ollama API endpoint. Defaults to "http://localhost:11434/".
        api_key (str): API key for authentication with Ollama. Defaults to "SomethingSomething".
        temperature (float): Controls randomness in output generation. Higher values (e.g., 0.8) make output more random, lower values (e.g., 0.2) make it more deterministic. Defaults to 0.3.
        num_ctx (int): Maximum context length (in tokens) the model can use. Defaults to 5000. Use -1 for infinite context, -2 to fill context.
        num_predict (Optional[int]): Maximum number of tokens to generate. If None, defaults to 128. Defaults to None.
        format (Optional[str]): Output format specification. Defaults to None (no specific format).
        verbose (bool): Whether to enable verbose logging. Defaults to False.
        extract_reasoning (bool): Whether to extract reasoning from model responses. Only works with Ollama3.2+ models. Defaults to False.
        type (Literal["LLM", "Chat"]): Type of model to initialize - either a standard LLM or a Chat model. Defaults to "Chat".

    Returns:
        Union[ChatOllama, OllamaLLM]: An initialized Ollama model instance of the specified type.

    Raises:
        ValueError: If an invalid type is specified.
        Exception: If model initialization fails for any reason.
    """
    try:
        common_kwargs = {
            "model": model,
            "base_url": base_url,
            "api_key": api_key,
            "temperature": temperature,
            "num_ctx": num_ctx,
            "num_predict": num_predict,
            "format": format,
            "verbose": verbose,
            "extract_reasoning": extract_reasoning,
        }
        if type == "Chat":
            local_model = ChatOllama(**common_kwargs)
        elif type == "LLM":
            local_model = OllamaLLM(**common_kwargs)
        else:
            raise ValueError("Invalid type. Choose either 'LLM' or 'Chat'")

        return local_model

    except Exception as e:
        raise Exception(f"Failed to initialize Ollama Model: {model}\nError: {str(e)}")

def init_Google_model(
            model: Literal["gemini-2.5-pro-exp-03-25", "gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-pro", "imagen-3.0-generate-002"] = "gemini-2.0-flash",
            google_api_key: Optional[str] = None,
            temperature: float = 0.3,
            max_output_tokens: Optional[int] = None,
            max_retries: int = 2,
            timeout : float = 120.0,
            verbose: bool = False,
            type: Literal["LLM", "Chat"] = "Chat",
            ) -> Union[ChatGoogleGenerativeAI, GoogleGenerativeAI]:
    """
    Initialize and configure a Google Generative AI model for text generation or chat completion.

    This function creates either a ChatGoogleGenerativeAI or GoogleGenerativeAI instance based on the specified
    parameters, allowing for customization of model behavior and connection settings.

    Parameters:
        model (Literal): The Google Generative AI model to use. Defaults to "gemini-2.0-flash".
        google_api_key (str, optional): API key for authentication with Google AI. Defaults to None.
        temperature (float): Controls randomness in output generation. Higher values make output more random, lower values make it more deterministic. Must be between 0.0 and 2.0. Defaults to 0.3.
        max_output_tokens (Optional[int]): Maximum number of tokens to generate. If None, defaults to 64.
        max_retries (int): Maximum number of retries for generation attempts. Defaults to 2.
        timeout (float): Maximum number of seconds to wait for a response. Defaults to 120.0.
        verbose (bool): Whether to enable verbose logging. Defaults to False.
        type (Literal["LLM", "Chat"]): Type of model to initialize - either a standard LLM or a Chat model. Defaults to "Chat".

    Returns:
        Union[ChatGoogleGenerativeAI, GoogleGenerativeAI]: An initialized Google Generative AI model instance of the specified type.

    Raises:
        ValueError: If an invalid type is specified.
        Exception: If model initialization fails for any reason.
    """
    try:
        common_kwargs = {
            "model": model,
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
            "max_retries": max_retries,
            "timeout": timeout,
            "verbose": verbose,
        }

        if google_api_key:
            common_kwargs["api_key"] = google_api_key

        if type == "Chat":
            google_model = ChatGoogleGenerativeAI(**common_kwargs)
        elif type == "LLM":
            google_model = GoogleGenerativeAI(**common_kwargs)
        else:
            raise ValueError("Invalid type. Choose either 'LLM' or 'Chat'")

        return google_model

    except Exception as e:
        raise Exception(f"Failed to initialize Google Gen AI Model: {model}\nError: {str(e)}")

# TypedDict schema for the conversational response
class ConversationalResponse(TypedDict):
    """Respond in a conversational manner. Be kind and helpful."""
    
    # We could have specified setup as:

    # setup: str                    # no default, no description
    # setup: Annotated[str, ...]    # no default, no description
    # setup: Annotated[str, "foo"]  # default, no description

    response = Annotated[str, ..., "A conversational response to the user's query"]

# BaseClass schema for the story
class StoryResponse(BaseModel):
    """Write a story for a given topic."""
    
    topic: str = Field(..., description="The topic of the story")
    story: str = Field(..., description="The story itself")
    num_lines: int = Field(..., description="The number of lines in the story")
    rating: Optional[int] = Field(None, description="How good the story is, from 1 to 10")

# Final response schema
class FinalResponse(BaseModel):
    """Container for either conversational or story responses."""
    final_output: Union[ConversationalResponse, StoryResponse]

def structured_output_llm(
    llm,
    schema
    ):
    """
    Configure an LLM to produce structured output according to a specified schema.
    
    Parameters:
        llm: The language model to use
        schema: The schema to structure the output
    """
    # Bind the schema to the LLM
    llm_with_structured_output = llm.with_structured_output(FinalResponse)
    # result = llm_with_structured_output.invoke("Write a story about a cat who likes to code.")
    result = llm_with_structured_output.invoke("How are you doing today?")
    print(result)
    
    
    llm_with_structured_output = llm.with_structured_output(schema)


def main():
    """Main function to demonstrate the usage of the models."""
    # local_model = init_Ollama_model(model='llama3.2:3b')
    # result = local_model.invoke("What is the mountain peak in the world?")

    # google_model = init_Google_model(type="LLM")
    # result = google_model.invoke("What is the distance between the highest and deepest point on earth?")

    # Single line langchain funtion to initialize the model. Refer: https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html
    # google_model = init_chat_model('google_genai:gemini-2.0-flash')
    local_model = init_chat_model('ollama:qwen2.5:14b')
    
    
    print('-' * 100)
    # For non-streamed response use case
    result = local_model.invoke("What is the distance between the highest and deepest point on earth?")
    print(result.content)
    print(result.response_metadata) # This is a dictionary with keys: model_name, finish_reason, usage_metadata
    print(result.usage_metadata) # This is a dictionary with keys: input_tokens, output_tokens, total_tokens
    
    # # For streamed response use case
    # for chunk in local_model.stream("What is the distance between the highest and deepest point on earth?"):
    #     print(chunk.content, end="", flush=True)
    # print()
    
    # print('-' * 100)
    
    # For structured output use case
    # structured_output_llm(local_model, FinalResponse)

    

if __name__ == '__main__':
    main()