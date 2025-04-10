from langchain_ollama import OllamaLLM, ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
from langchain.chat_models import init_chat_model

from typing import Literal, Optional, Union
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

def main():

    # local_model = init_Ollama_model(model='llama3.2:3b')
    # result = local_model.invoke("What is the mountain peak in the world?")

    # google_model = init_Google_model(type="LLM")
    # result = google_model.invoke("What is the distance between the highest and deepest point on earth?")


    # Single line langchain funtion to initialize the model. Refer: https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html
    google_model = init_chat_model('google_genai:gemini-2.0-flash')
    result = google_model.invoke("What is the distance between the highest and deepest point on earth?")

    print(result)

if __name__ == '__main__':
    main()