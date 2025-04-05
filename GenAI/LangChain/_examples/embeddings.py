from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_core.embeddings import Embeddings
from rich import print
from typing import List

# For Local Embedding models using Ollama
class CreateOllamaEmbeddings:
    def __init__(self, model_name: str = "nomic-embed-text:latest", base_url: str = "http://localhost:11434/"):
        """
        Initialize the CreateOllamaEmbeddings class with the specified model name and base URL.

        Parameters:
        - model_name (str): The name of the Ollama model to use for embeddings. Default is "mistral-nemo:12b-instruct-2407-q4_K_M".
        - base_url (str): The base URL of the Ollama model server. Default is "http://localhost:11434/".

        Returns:
        - None
        """
        self.model_name = model_name
        self.base_url = base_url
        self.embed_model = OllamaEmbeddings(
            model=self.model_name,
            base_url=self.base_url,
        )


    def __call__(self):
        """
        Returns the initialized OllamaEmbeddings instance.

        This method allows the OllamaEmbeddings instance to be called as a function,
        returning the underlying OllamaEmbeddings object.

        Parameters:
        None

        Returns:
        OllamaEmbeddings: The initialized OllamaEmbeddings instance.
        """
        return self.embed_model



    def embed_query(self, query: str) -> list[float]:
        """
        Embeds a single query string into a list of float values representing the query's embedding.

        Parameters:
        - query (str): The input query string to be embedded.

        Returns:
        - list[float]: A list of float values representing the query's embedding.

        Raises:
        - Exception: If an error occurs during the embedding process, it will be caught and printed.
        """
        try:
            embedding = self.embed_model.embed_query(query)
            return embedding
        except Exception as e:
            print(f"Error occurred while embedding query: {e}")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        Embeds a list of document strings into a list of lists of float values representing the documents' embeddings.

        Parameters:
        - texts (list[str]): A list of input document strings to be embedded. Each string represents a document.

        Returns:
        - list[list[float]]: A list of lists of float values representing the documents' embeddings. Each inner list contains the embedding values for a single document.

        Raises:
        - Exception: If an error occurs during the embedding process, it will be caught and printed.
        """
        try:
            embeddings = self.embed_model.embed_documents(texts)
            return embeddings
        except Exception as e:
            print(f"Error occurred while embedding documents: {e}")

# To Create your very own Embedding Model
class CustomEmbeddings(Embeddings):
    """Custom embedding model integration.

    # TODO: Populate with relevant params.
    Key init args — completion params:
        model: str
            Name of ParrotLink model to use.

    See full list of supported init args and their descriptions in the params section.

    # TODO: Replace with relevant init params.
    Instantiate:
        .. code-block:: python

            from langchain_parrot_link import ParrotLinkEmbeddings

            embed = ParrotLinkEmbeddings(
                model="...",
                # api_key="...",
                # other params...
            )

    Embed single text:
        .. code-block:: python

            input_text = "The meaning of life is 42"
            embed.embed_query(input_text)

        .. code-block:: python

            # TODO: Example output.

    # TODO: Delete if token-level streaming isn't supported.
    Embed multiple text:
        .. code-block:: python

             input_texts = ["Document 1...", "Document 2..."]
            embed.embed_documents(input_texts)

        .. code-block:: python

            # TODO: Example output.

    # TODO: Delete if native async isn't supported.
    Async:
        .. code-block:: python

            await embed.aembed_query(input_text)

            # multiple:
            # await embed.aembed_documents(input_texts)

        .. code-block:: python

            # TODO: Example output.

    """

    def __init__(self, model: str):
        self.model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed search docs."""
        return [[0.5, 0.6, 0.7] for _ in texts]

    def embed_query(self, text: str) -> List[float]:
        """Embed query text."""
        return self.embed_documents([text])[0]

    # optional: add custom async implementations here
    # you can also delete these, and the base class will
    # use the default implementation, which calls the sync
    # version in an async executor:

    # async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
    #     """Asynchronous Embed search docs."""
    #     ...

    # async def aembed_query(self, text: str) -> List[float]:
    #     """Asynchronous Embed query text."""
    #     ...

def main():

    # Check https://python.langchain.com/docs/integrations/text_embedding/ for other use case.

    embed_model = CreateOllamaEmbeddings()
    # embed_model = CustomEmbeddings("test-model")

    print(embed_model.embed_documents(["Hello", "world"]))
    print(embed_model.embed_query("Hello"))

if __name__ == "__main__":
    main()