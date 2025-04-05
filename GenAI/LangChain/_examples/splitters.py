from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
    Language
)
from langchain_experimental.text_splitter import SemanticChunker

from langchain_core.documents import Document
from langchain_ollama.embeddings import OllamaEmbeddings

from rich import print, pretty
from typing import Literal, Union

from _tools._lang.loaders import md_loader, python_loader

def char_splitter(data: Union[list[Document], list[str]], mode: Literal["split", "create"] = "split", metadatas: list[dict] = None, chunk_size: int = 1000, chunk_overlap: int = 200, **kwargs) -> list[Document]:
    """
    This function splits a given document into smaller chunks based on specified character separators.

    Parameters:
    data (Union[list[Document], list[str]]): The document to be split. It can be a list of Document objects or a list of strings.
    mode (Literal["split" , "create"], optional): The mode of operation. If "split", the function will split the Document objects. If "create", the function will create Document objects from the input strings. Defaults to "split".
    metadatas (list[dict], optional): The metadata for the Document objects. Only used when mode is "create". Defaults to None.
    chunk_size (int, optional): The maximum size of each chunk. Defaults to 1000.
    chunk_overlap (int, optional): The overlap between chunks. Defaults to 200.
    **kwargs: Additional keyword arguments for the CharacterTextSplitter.

    Returns:
    list: A list of smaller Document objects, each containing a chunk of the original document.
    """

    try:
        # Initialize the CharacterTextSplitter with specific parameters
        char_splitter = CharacterTextSplitter(
            separator=kwargs.get("separator", "\n\n"),  # The separator to split the document
            chunk_size=chunk_size,  # The maximum size of each chunk
            chunk_overlap=chunk_overlap,  # The overlap between chunks
            length_function=len,  # The function to calculate the length of a chunk
            is_separator_regex=kwargs.get("is_separator_regex", False),  # Whether the separator is a regular expression
        )

        # Use the create_documents method of the text_splitter to split the document
        if mode == "split":
            docs = char_splitter.split_documents(data)
        else:
            docs = char_splitter.create_documents(data, metadatas)

        # Assert that the loaded data is a list of Document
        assert isinstance(docs[0], Document)

        # Return the list of smaller documents
        return docs

    except Exception as e:
        raise Exception(f"Failed to split document.\nError: {str(e)}")
    

def rec_char_splitter(data: list, language: str = None, separators: list = None, mode: Literal["split", "create"] = "split", metadatas: list[dict] = None, chunk_size: int = 1000, chunk_overlap: int = 200, **kwargs) -> list:
    """
    This function splits a given document into smaller chunks based on specified character separators or language-specific separators.

    Parameters:
    data (list): The document to be split. It can be a list of strings or a list of Document objects.
    language (str, optional): The language of the document. If provided, the function will use language-specific separators. Defaults to None.
    separators (list, optional): A list of custom separators to split the document. If provided, the function will use these separators instead of language-specific ones. Defaults to None.
    mode (Literal["split", "create"], optional): The mode of operation. If "split", the function will split the Document objects. If "create", the function will create Document objects from the input strings. Defaults to "split".
    metadatas (list[dict], optional): The metadata for the Document objects. Only used when mode is "create". Defaults to None.
    chunk_size (int, optional): The maximum size of each chunk. Defaults to 1000.
    chunk_overlap (int, optional): The overlap between chunks. Defaults to 200.
    **kwargs: Additional keyword arguments for the CharacterTextSplitter.

    Returns:
    list: A list of smaller Document objects, each containing a chunk of the original document.

    Raises:
    Exception: If an error occurs during the splitting process.
    """
    # Get the list of supported languages
    supported_langs = [e.value for e in Language]

    try:
        if language:
            assert language in supported_langs, f"Unsupported language: {language}. Supported languages: {supported_langs}"

            # Initialize the RecursiveCharacterTextSplitter with specific parameters
            rec_char_splitter = RecursiveCharacterTextSplitter.from_language(
                language=language,
                separators=RecursiveCharacterTextSplitter.get_separators_for_language(f"Language.{language.capitalize()}"),
                chunk_size=chunk_size,  # The maximum size of each chunk
                chunk_overlap=chunk_overlap,  # The overlap between chunks
                length_function=len,  # The function to calculate the length of a chunk
                is_separator_regex=kwargs.get("is_separator_regex", False),  # Whether the separator is a regular expression
            )
        else:
            rec_char_splitter = RecursiveCharacterTextSplitter(
                separators=separators or [
                    "\n\n",
                    "\n",
                    " ",
                    ".",
                    ",",
                    "\u200b",  # Zero-width space
                    "\uff0c",  # Fullwidth comma
                    "\u3001",  # Ideographic comma
                    "\uff0e",  # Fullwidth full stop
                    "\u3002",  # Ideographic full stop
                    "",
                ],
                chunk_size=chunk_size,  # The maximum size of each chunk
                chunk_overlap=chunk_overlap,  # The overlap between chunks
                length_function=len,  # The function to calculate the length of a chunk
                is_separator_regex=kwargs.get("is_separator_regex", False),  # Whether the separator is a regular expression
                )

        # Use the create_documents method of the text_splitter to split the document
        if mode == "split":
            docs = rec_char_splitter.split_documents(data)
        else:
            docs = rec_char_splitter.create_documents(data, metadatas)

        # Assert that the loaded data is a list of Document
        assert isinstance(docs[0], Document)

        # Return the list of smaller documents
        return docs

    except Exception as e:
        raise Exception(f"Failed to split document.\nError: {str(e)}")

def md_splitter(data: str, headers_to_split_on, strip_headers: bool = False) -> list[Document]:
    """
    This function splits a given Markdown document into smaller chunks based on specified headers.

    Parameters:
    data (str): The Markdown document to be split. It should be a string containing the Markdown content.
    headers_to_split_on (list): A list of Markdown headers (e.g., "# Header 1", "## Header 2") to split the document on.
    strip_headers (bool, optional): Whether to remove the headers from the split chunks. Defaults to False.

    Returns:
    list[Document]: A list of smaller Document objects, each containing a chunk of the original Markdown document.
    """

    try:
        # Create an instance of MarkdownHeaderTextSplitter
        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on,
            strip_headers=strip_headers,
        )
        
        # Split the Markdown document into smaller chunks
        docs = markdown_splitter.split_text(data)

        # Return the list of smaller Document objects
        return docs
    except Exception as e:
        raise Exception(f"Failed to split Markdown document.\nError: {str(e)}")

def semantic_text_splitter(data: Union[list[Document], list[str]], mode: Literal["split", "create"] = "split", metadatas: list[dict] = None) -> list[Document]:
    """
    This function splits a given document into smaller chunks based on semantic similarity using Ollama embeddings.

    Parameters:
    data (Union[list[Document], list[str]]): The document to be split. It can be a list of Document objects or a list of strings.
    mode (Literal["split", "create"], optional): The mode of operation. If "split", the function will split the Document objects. If "create", the function will create Document objects from the input strings. Defaults to "split".
    metadatas (list[dict], optional): The metadata for the Document objects. Only used when mode is "create". Defaults to None.

    Returns:
    list[Document]: A list of smaller Document objects, each containing a chunk of the original document.

    Raises:
    Exception: If an error occurs during the splitting process.
    """
    try:
        ollama_embd = OllamaEmbeddings(model = "mistral:7b-instruct-v0.3-q4_K_M")

        # Create an instance of SemanticChunker
        semeantic_splitter = SemanticChunker(
            embeddings=ollama_embd,
        )

        # Use the create_documents method of the text_splitter to split the document
        if mode == "split":
            docs = semeantic_splitter.split_documents(data)
        else:
            docs = semeantic_splitter.create_documents(data, metadatas)

        # Assert that the loaded data is a list of Document
        assert isinstance(docs[0], Document)

        # Return the list of smaller documents
        return docs

    except Exception as e:
        raise Exception(f"Failed to split document.\nError: {str(e)}")

def main():

    # Look for more splitter examples here: https://python.langchain.com/docs/concepts/text_splitters/
    
    md_file_path = "_data/Chocolate Factory/Write_Up.md"
    py_file_path = "./_data/code/tmp_code_b53ed68599bcc955795e1fc2189b7f1f5df4de8ef1633dd44404dfa5cd29167f.py"
    
    data = md_loader(md_file_path)
    # data = python_loader(py_file_path)
    # print(data)

    # texts = char_splitter(data)
    # texts = rec_char_splitter(data)
    # texts = rec_char_splitter(data, "python")
    # texts = md_splitter(data)
    texts = semantic_text_splitter(data)

    print(texts)


if __name__ == "__main__":
    main()