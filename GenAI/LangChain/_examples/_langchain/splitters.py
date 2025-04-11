from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
    Language,
    HTMLHeaderTextSplitter,
    HTMLSectionSplitter,
    RecursiveJsonSplitter
)

from langchain_core.documents import Document

from rich import print
from typing import Literal, Union, List, Dict, Tuple
import json

from _examples.loaders import md_loader, file_loader

def char_splitter(
    data: Union[List[Document], List[str], str],
    operations: Literal['create-docs', 'split-text', 'split-docs', 'transform-docs'] = 'create-docs',
    separator: str = "\n\n",
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    metadatas: List[Dict] = None,
    **kwargs
    ) -> List[Union[Document, str]]:
    """
    Splits a given document into smaller chunks based on specified character separators.

    Parameters:
    data: The document to be split. It can be a list of Document objects, a list of strings, or a single string.
    operations: The mode of operation.
        - 'create-docs': Creates Document objects from a list of strings.
        - 'split-text': Splits a single string into smaller strings.
        - 'split-docs': Splits a list of Document objects into smaller Document objects.
        - 'transform-docs': Transforms a list of Document objects into smaller Document objects.
        Defaults to 'create-docs'.
    separator: The separator to split the document. Defaults to "\n\n".
    chunk_size: The maximum size of each chunk. Defaults to 1000.
    chunk_overlap: The overlap between chunks. Defaults to 200.
    metadatas: The metadata for the Document objects. Only used when operations is 'create-docs'. Defaults to None.
    **kwargs: Additional keyword arguments for the CharacterTextSplitter.

    Returns:
    A list of smaller Document objects or strings, depending on the 'operations' parameter.
            
    Raises:
    Exception: If an error occurs during the splitting process.
    """

    try:
        char_splitter = CharacterTextSplitter(
            separator=separator,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=kwargs.get("is_separator_regex", False),
        )

        # Use the create_documents method for splitting list of strs
        if operations == 'create-docs':

            # Assert that the loaded data is a list of strs
            assert isinstance(data[0], str)
                
            # Create documents from the input data using the character splitter
            docs = char_splitter.create_documents(data, metadatas = metadatas)
            
            # Assert that the documents returned is a list of Document
            assert isinstance(docs[0], Document)

        # Use the Document splitter functions to split/transform into smaller documents.
        elif operations in ['split-docs', 'transform-docs']:
            
            # Assert that the loaded data is a list of Documents
            assert isinstance(data[0], Document)
            
            # docs = char_splitter.split_documents(data)
            docs = char_splitter.transform_documents(data)
            
            # Assert that the documents returned is a list of Document
            assert isinstance(docs[0], Document)
        
        # Split a text into smaller chunks
        else:
            
            # Assert that the loaded data is a string.
            assert isinstance(data, str)
            
            docs = char_splitter.split_text(data)
            
            # Assert that the documents returned is a list of Document
            # Assert that the documents returned is a list of strings
            assert isinstance(docs[0], str)
            assert isinstance(docs[0], str)
            
            
        # Return the list of split documents
        return docs

    except Exception as e:
        raise Exception(f"Failed to split document.\nError: {e}")
    
def rec_char_splitter(
    data: Union[List[Document], List[str], str],
    operations: Literal['create-docs', 'split-text', 'split-docs', 'transform-docs'] = 'create-docs',
    separators: List[str] = [
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
    metadatas: List[Dict] = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    language: str = None,
    **kwargs
    ) -> List[Union[Document, str]]:
    """
    Splits a given document into smaller chunks recursively based on specified character separators.

    Parameters:
    data: The document to be split. It can be a list of Document objects, a list of strings, or a single string.
    operations: The mode of operation.
        - 'create-docs': Creates Document objects from a list of strings.
        - 'split-text': Splits a single string into smaller strings.
        - 'split-docs': Splits a list of Document objects into smaller Document objects.
        - 'transform-docs': Transforms a list of Document objects into smaller Document objects.
        Defaults to 'create-docs'.
    separators: The list of separators to split the document. Defaults to a predefined list.
    metadatas: The metadata for the Document objects. Only used when operations is 'create-docs'. Defaults to None.
    chunk_size: The maximum size of each chunk. Defaults to 1000.
    chunk_overlap: The overlap between chunks. Defaults to 200.
    language: The language to use for separators. If provided, the separators will be fetched based on the language. Defaults to None.
    **kwargs: Additional keyword arguments for the RecursiveCharacterTextSplitter.

    Returns:
    A list of smaller Document objects or strings, depending on the 'operations' parameter.

    Raises:
    Exception: If an error occurs during the splitting process.
    """

    if language:
        # Get the list of supported languages
        supported_langs = [e.value for e in Language]

        assert language in supported_langs, f"Unsupported language: {language}. Supported languages: {supported_langs}"

        # Fetch the list of valid separators
        separators = RecursiveCharacterTextSplitter.get_separators_for_language(language)

    try:
        # Initialize the RecursiveCharacterTextSplitter with specific parameters
        rec_char_splitter = RecursiveCharacterTextSplitter(
            separators= separators,
            chunk_size=chunk_size,  # The maximum size of each chunk
            chunk_overlap=chunk_overlap,  # The overlap between chunks
            length_function=len,  # The function to calculate the length of a chunk
            is_separator_regex=kwargs.get("is_separator_regex", False),  # Whether the separator is a regular expression
        )

        # Use the create_documents method of the text_splitter to split the document
        if operations == "create-docs":

            # Assert that the loaded data is a list of strings
            assert isinstance(data[0], str)

            docs = rec_char_splitter.create_documents(data, metadatas)

            # Assert that the documents returned is a list of Document
            assert isinstance(docs[0], Document)

        # Use the Document splitter functions to split/transform into smaller documents.
        elif operations in ['split-docs', 'transform-docs']:
            # Assert that the loaded data is a list of Document objects
            assert isinstance(data[0], Document)
            
            docs = rec_char_splitter.split_documents(data)

            # Assert that the documents returned is a list of Document
            assert isinstance(docs[0], Document)

        else:
            # Assert that the loaded data is a list of Document objects
            assert isinstance(data[0], Document)

            docs = rec_char_splitter.split_text(data)

            # Assert that the documents returned is a list of Document
            assert isinstance(docs[0], Document)

        # Return the list of smaller documents
        return docs

    except Exception as e:
        raise Exception(f"Failed to split document.\nError: {e}")

def md_header_splitter(
    data: str, 
    headers_to_split_on: List[Tuple[str, str]] = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ],
    return_each_line: bool = False,
    strip_headers: bool = True,
    ) -> List[Document]:
    """
    Splits a markdown document into smaller chunks based on specified headers.

    Parameters:
    data: The markdown document to be split.
    headers_to_split_on: The list of headers to split on. Each tuple contains the header prefix (e.g., "#") and the header name (e.g., "Header 1"). Defaults to a predefined list of headers.
    return_each_line: Whether to return each line as a separate document. Defaults to False.
    strip_headers: Whether to strip the headers from the content of the chunks. Defaults to True.
    Returns:
    A list of Document objects, each containing a chunk of the original document.

    Raises:
    Exception: If an error occurs during the splitting process.
    """
    try:
        # Create an instance of MarkdownHeaderTextSplitter
        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on,
            return_each_line=return_each_line,
            strip_headers=strip_headers,
        )
        
        # Split the Markdown document into smaller chunks
        docs = markdown_splitter.split_text(data)

        # Return the list of smaller Document objects
        return docs
    
    except Exception as e:
        
        raise Exception(f"Failed to split Markdown document.\nError: {str(e)}")

def html_splitter(
    data: str, 
    headers_to_split_on: List[Tuple[str, str]] = [
        ("h1", "Header 1"),
        ("h2", "Header 2"),
        ("h3", "Header 3"),
        ],
    ) -> List[Document]:
    """
    Splits an HTML document into smaller chunks based on specified headers using HTMLSectionSplitter.
    
    Parameters:
    data: The HTML document to be split.
    headers_to_split_on: The list of headers to split on. Each tuple contains the header tag (e.g., "h1") and the header name (e.g., "Header 1"). Defaults to a predefined list of headers.
    Returns:
    A list of Document objects, each containing a chunk of the original document.
        
    Raises:
    Exception: If an error occurs during the splitting process.
    """
    try:
        # Refer to this for other options: https://python.langchain.com/api_reference/text_splitters/html.html
        # Create an instance of HTMLSectionSplitter
        html_splitter = HTMLSectionSplitter(
            headers_to_split_on=headers_to_split_on,
        )
        
        # Split the HTML document into smaller chunks
        docs = html_splitter.split_text(data)

        # Return the list of smaller Document objects
        return docs
    
    except Exception as e:
        
        raise Exception(f"Failed to split HTML document.\nError: {e}")

def rec_json_splitter(
    data: dict,
    max_chunk_size: int = 2000,
    min_chunk_size: int = 1500,
    ) -> List[Document]:
    """
    Splits a JSON document into smaller chunks recursively based on its structure.
    
    Parameters:
    data: The JSON data to be split.
    max_chunk_size: The maximum size of each chunk. Defaults to 2000.
    min_chunk_size: The minimum size of each chunk. Defaults to 1500.
    Returns:
    A list of Document objects, each containing a chunk of the original JSON data.
        
    Raises:
    Exception: If an error occurs during the splitting process.
    """
    try:
        # Initialize the RecursiveJsonSplitter with specified parameters
        json_splitter = RecursiveJsonSplitter(
            max_chunk_size = max_chunk_size,
            min_chunk_size = min_chunk_size,
        )
        
        # Split the JSON data into smaller chunks
        docs = json_splitter.split_text(json_data=data)

        # Return the list of smaller Document objects
        return docs
    
    except Exception as e:
        
        raise Exception(f"Failed to split HTML document.\nError: {str(e)}")

# # In works
# def semantic_text_splitter(
#     data: Union[list[Document], list[str]],
#     mode: Literal["split", "create"] = "split",
#     metadatas: list[dict] = None
#     ) -> list[Document]:
    
#     """
#     This function splits a given document into smaller chunks based on semantic similarity using Ollama embeddings.

#     Parameters:
#     data (Union[list[Document], list[str]]): The document to be split. It can be a list of Document objects or a list of strings.
#     mode (Literal["split", "create"], optional): The mode of operation. If "split", the function will split the Document objects. If "create", the function will create Document objects from the input strings. Defaults to "split".
#     metadatas (list[dict], optional): The metadata for the Document objects. Only used when mode is "create". Defaults to None.

#     Returns:
#     list[Document]: A list of smaller Document objects, each containing a chunk of the original document.

#     Raises:
#     Exception: If an error occurs during the splitting process.
#     """
#     try:
#         ollama_embd = OllamaEmbeddings(model = "mistral:7b-instruct-v0.3-q4_K_M")

#         # Create an instance of SemanticChunker
#         semeantic_splitter = SemanticChunker(
#             embeddings=ollama_embd,
#         )

#         # Use the create_documents method of the text_splitter to split the document
#         if mode == "split":
#             docs = semeantic_splitter.split_documents(data)
#         else:
#             docs = semeantic_splitter.create_documents(data, metadatas)

#         # Assert that the loaded data is a list of Document
#         assert isinstance(docs[0], Document)

#         # Return the list of smaller documents
#         return docs

#     except Exception as e:
#         raise Exception(f"Failed to split document.\nError: {str(e)}")


def main():

    # Look for more splitter examples here: https://python.langchain.com/docs/concepts/text_splitters/
    
    strs_data = ["Help me understand this!!", "I don't know how this works"]
    md_file_path = "./_data/_sample/hello.md"
    html_file_path = "./_data/_sample/sample.html"
    json_file_path = "./_data/_sample/sample.json"
    
    # docs_data = md_loader(md_file_path)
    file_data = file_loader(json_file_path)
    
    # # For character splitter use cases
    # texts = char_splitter(strs_data, separator="", chunk_size=5, chunk_overlap=1)
    # texts = char_splitter(strs_data[0], 'split-text', separator="", chunk_size=1,chunk_overlap=0)
    # texts = char_splitter(docs_data, operations="split-docs", separator=" ", chunk_size=50, chunk_overlap=0)
    
    # # For Recursive Character split use cases
    # # Get the list of supported languages
    # supported_langs = [e.value for e in Language]
    # print(supported_langs)
    
    # texts = rec_char_splitter(strs_data, chunk_size=5, chunk_overlap=1)
    # texts = rec_char_splitter(docs_data, 'split-docs', language='markdown')
    
    
    # texts = md_header_splitter(file_data[0].page_content)
    
    # texts = html_splitter(file_data[0].page_content, headers_to_split_on=[("h1", "Header 1"), ("h2", "Header 2"), ("h3", "Header 3"),("p", "Header 4")])
    
    texts = rec_json_splitter(json.loads(file_data[0].page_content))

    print(texts)

if __name__ == "__main__":
    main()