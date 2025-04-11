from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.embeddings import init_embeddings

from typing import Literal, Optional
from rich import print
from dotenv import load_dotenv

load_dotenv()

def init_Ollama_embed(
        model: Literal["nomic-embed-text:latest", "deepseek-r1:14b", "qwen2.5:14b", "llama3.2:3b"] = "nomic-embed-text:latest",
        base_url: str = "http://localhost:11434/",
        ) -> Optional[OllamaEmbeddings]:
    """
    Initialize and return an Ollama Embeddings model for the specified model and base URL.
    If an error occurs during initialization, it prints an error message.

    Args:
        model (Literal["nomic-embed-text:latest", "deepseek-r1:14b", "qwen2.5:14b", "llama3.2:3b"]): 
            The name of the Ollama model to use for embeddings. Defaults to "nomic-embed-text:latest".
        base_url (str): The base URL for the Ollama API. Defaults to "http://localhost:11434/".

    Returns:
        OllamaEmbeddings: An initialized OllamaEmbeddings object if successful.

    Raises:
        Exception: Prints an error message if initialization fails, but doesn't raise the exception.
    """

    try:
        embed_model = OllamaEmbeddings(
            model = model,
            base_url = base_url,
            # For additional options, Refer: https://python.langchain.com/api_reference/ollama/embeddings/langchain_ollama.embeddings.OllamaEmbeddings.html.
        )
        return embed_model
    except Exception as e:
        raise Exception(f"Failed to initialize Ollama Embedding for Model: {model}\nError: {str(e)}")

def init_Google_embed(
        model: Literal["models/text-embedding-004", "models/embedding-001"] = "models/text-embedding-004",
        request_options: dict = None,
        task_type: Literal["task_type_unspecified", "retrieval_query", "retrieval_document"," semantic_similarity", "classification", "clustering"] = "task_type_unspecified",
        ) -> GoogleGenerativeAIEmbeddings:
    """
    Initialize and return a Google Generative AI Embeddings model.

    This function creates an instance of GoogleGenerativeAIEmbeddings with the specified model,
    request options, and task type. If an error occurs during initialization, it prints an error message.

    Args:
        model (Literal): The name of the Google model to use for embeddings. Defaults to "models/text-embedding-004".
        request_options (dict): A dictionary of request options to pass to the Google API client. Example: {'timeout': 10}.
        task_type (Literal): The task type for the embeddings. Defaults to "task_type_unspecified".

    Returns:
        GoogleGenerativeAIEmbeddings: An initialized GoogleGenerativeAIEmbeddings object if successful.

    Raises:
        Exception: Prints an error message if initialization fails, but doesn't raise the exception.
    """
    try:
        embed_model = GoogleGenerativeAIEmbeddings(
             model = model,
             request_options = request_options,
             task_type = task_type,
             # For additional options, Refer: https://python.langchain.com/api_reference/google_genai/embeddings/langchain_google_genai.embeddings.GoogleGenerativeAIEmbeddings.html.
        )
        return embed_model
    except Exception as e:
        raise Exception(f"Failed to initialize Google Embeddings for Model: {model}\nError: {str(e)}")

def main():

    # embed_model = init_Ollama_embed()
    # embed_model = init_Google_embed()

    # # Single line langchain funtion to initialize the embedding model. Refer: https://python.langchain.com/api_reference/langchain/embeddings/langchain.embeddings.base.init_embeddings.html
    embed_model = init_embeddings(model="ollama:nomic-embed-text:latest")

 
    print(embed_model.embed_query("Hello there")[:10])
        
if __name__ == "__main__":
    main()