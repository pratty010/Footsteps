from langchain_community.document_loaders import (
    DirectoryLoader, 
    TextLoader,
    CSVLoader,
    JSONLoader,
    BSHTMLLoader,
    PythonLoader,
    PyMuPDFLoader,
    PyPDFLoader,
    WebBaseLoader,
    UnstructuredFileLoader,
    UnstructuredMarkdownLoader
)

from langchain_unstructured import UnstructuredLoader
from langchain_core.documents import Document

from rich import print
from typing import List, Literal

def dir_loader(
        dir_path: str,
        glob: Literal['**/[!.]*', '**/*.md', '**/*.txt', '**/*.csv', '**/*.py', '**/*.pdf', '**/*.html', '**/*.json'] = '**/*.md',
        show_progress: bool = True,
        recursive : bool = False,
        loader_cls: type[TextLoader] = TextLoader,
        **kwargs
        ) -> List[Document]:
    
    """
    Load documents from a directory using the specified parameters.

    Parameters:
    dir_path (str): The path to the directory containing the documents.
    glob (Literal['**/[!.]*', '**/*.md', '**/*.txt', '**/*.csv', '**/*.py', '**/*.pdf', '**/*.html', '**/*.json']): A string that specifies the pattern of files to load. Defaults to '*.md'.
    show_progress (bool): Whether to display a progress bar while loading documents. Defaults to True.
    recursive (bool): Whether to search for files recursively in subdirectories. Defaults to False.
    loader_cls (type[TextLoader]): The class of document loader to use. Defaults to TextLoader.
    **kwargs: Additional keyword arguments passed to the DirectoryLoader constructor.

    Returns:
    List[Document]: A list of loaded documents.
    
    Notes:
    - This function uses the `DirectoryLoader` from `langchain_community.document_loaders`.
    - The `glob` parameter specifies the pattern of files to load. It defaults to '*.md'.
    - The `show_progress` parameter controls whether a progress bar is displayed while loading documents.
    - The `recursive` parameter determines whether to search for files recursively in subdirectories.
    - The `loader_cls` parameter allows specifying a different document loader class, such as `TextLoader`, `CSVLoader`, etc. (Type[UnstructuredFileLoader] | Type[TextLoader] | Type[BSHTMLLoader] | Type[CSVLoader]) – Loader class to use for loading files. Defaults to UnstructuredFileLoader.
    - Additional keyword arguments can be passed to the `DirectoryLoader` constructor using `**kwargs`.

    Example Usage:
    - Load all Markdown files from a directory and its subdirectories using TextLoader
    loader = load_documents_from_directory('path/to/directory', loader_cls=TextLoader)

    Exceptions:
    - If the specified directory path does not exist or is inaccessible, a `FileNotFoundError` will be raised.
    - If there are issues with loading files, such as file format errors or permission issues, an exception will be raised.
    """

    try:
        # Create a DirectoryLoader object with the specified parameters
        loader = DirectoryLoader(
            path = dir_path,
            glob = glob,
            show_progress = show_progress,
            loader_cls = loader_cls,
            recursive = recursive,
            use_multithreading = kwargs.get('use_multithreading', False),  # Set to True for multithreading
            max_concurrency = kwargs.get('max_concurrency', 4),  # Set to desired concurrency level
            # For additional parameters, refer: https://python.langchain.com/docs/how_to/document_loader_directory/
        )

        # Load the documents from the directory using the DirectoryLoader object
        data = loader.load()

        # Assert that the loaded data is not empty
        assert len(data) > 0
        # Assert that each document in the loaded data is an instance of Document
        assert isinstance(data[0], Document)

        # Return the list of loaded documents
        return data
    
    except Exception as e:
        print(f"Error loading data from directory: {e}")
        return []

def file_loader(
        file_path: str, 
        encoding: str = None, 
        autodetect_encoding: bool = False,
        ) -> List[Document]:
    
    """
    Load documents from a text file using the specified parameters.

    Parameters:
    file_path (str): The path to the text file.
    encoding (str): The character encoding of the file. Defaults to None.
    autodetect_encoding (bool): Whether to automatically detect the file's encoding. Defaults to False.

    Returns:
    List[Document]: A list of loaded documents.

    Notes:
    - This function uses the `TextLoader` from `langchain_community.document_loaders`.
    - The `encoding` parameter specifies the character encoding of the file. If None, the system default will be used.
    - The `autodetect_encoding` parameter determines whether to automatically detect the file's encoding. If True, the loader will attempt to detect the encoding based on the content of the file.

    Examples:
    - Load a text file with UTF-8 encoding:
      >>> file_loader("path/to/textfile.txt", encoding="utf-8")
    - Load a text file and attempt to detect its encoding automatically:
      >>> file_loader("path/to/textfile.txt", autodetect_encoding=True)

    Exceptions:
    - If the file path does not exist or is inaccessible, a `FileNotFoundError` will be raised.
    - If there are issues with loading files, such as file format errors or permission issues, an exception will be raised.
    """

    try:
        # Create an instance of TextLoader with the specified file path and autodetect encoding
        loader = TextLoader(
            file_path = file_path,
            encoding=encoding,
            autodetect_encoding=autodetect_encoding,
        )

        # Load data from the text file
        data = loader.load()

        # Assert the the documents are not empty
        assert len(data) > 0
        # Assert that each document in the loaded data is an instance of Document
        assert isinstance(data[0], Document)

       # Return the list of loaded documents
        return data
    
    except Exception as e:
        print(f"Error loading data from text file: {e}")
        return []

def csv_loader(
        file_path: str,
        source_column: str = None,
        encoding = None,
        autodetect_encoding: bool = False,
        csv_args: dict = {
            "delimiter": ",",
            "quotechar": '"',
            },
            **kwargs,
            ) -> List[Document]:
    
    """
    Load documents from a CSV file using the specified parameters.

    Parameters:
    file_path (str): The path to the CSV file.
    source_column (str, optional): The column name that contains the document content. Defaults to None.
    encoding (str, optional): The character encoding of the file. Defaults to None.
    autodetect_encoding (bool, optional): Whether to automatically detect the file's encoding. Defaults to False.
    csv_args (dict, optional): Additional arguments for parsing the CSV file. Defaults to {"delimiter": ",", "quotechar": '"'}.
    **kwargs: Additional keyword arguments passed to the CSVLoader constructor.

    Returns:
    List[Document]: A list of loaded documents.

    Notes:
    - This function uses the `CSVLoader` from `langchain_community.document_loaders`.
    - The `source_column` parameter specifies the column name that contains the document content. If None, the entire row will be considered as a document.
    - The `encoding` parameter specifies the character encoding of the file. If None, the system default will be used.
    - The `autodetect_encoding` parameter determines whether to automatically detect the file's encoding. If True, the loader will attempt to detect the encoding based on the content of the file.
    - Additional keyword arguments can be passed to the `CSVLoader` constructor using `**kwargs`.

    Example Usage:
    - Load a CSV file with a specific column as document content and UTF-8 encoding
      >>> csv_loader("path/to/csvfile.csv", source_column="content", encoding="utf-8")
    - Load a CSV file and attempt to detect its encoding automatically
      >>> csv_loader("path/to/csvfile.csv", autodetect_encoding=True)

    Exceptions:
    - If the specified file path does not exist or is inaccessible, a `FileNotFoundError` will be raised.
    - If there are issues with loading files, such as file format errors or permission issues, an exception will be raised.
    """
    
    try:
        # create instance of a CSV loader
        loader = CSVLoader(
            file_path = file_path,
            source_column=source_column,
            encoding=encoding,
            autodetect_encoding=autodetect_encoding,
            csv_args= csv_args,
            metadata_columns = kwargs.get("metadata_columns", ()),
            content_columns = kwargs.get("content_columns", ()),
        )

        # load data from CSV file
        data = loader.load()

        # Assert loaded data is not empty
        assert len(data) > 0
        # Assert that the loaded data is a list of Document
        assert isinstance(data[0], Document)

        # Return the list of Documents
        return data

    except Exception as e:
        print(f"Error loading data from CSV file: {e}")
        return []

def md_loader(
        file_path: str, 
        mode: Literal["elements", "single", "multi", "all"] = "elements",
        **kwargs
        ) -> List[Document]:

    """
    Load documents from a Markdown file using the specified parameters.

    Parameters:
    file_path (str): The path to the Markdown file.
    mode (Literal["single", "multi", "all", "elements"]): Specifies how to handle multiple sections in a single Markdown file. Defaults to "single".
    **kwargs: Additional keyword arguments passed to the MDLoader constructor.

    Returns:
    List[Document]: A list of loaded documents.

    Notes:
    - This function uses the `MDLoader` from `langchain_community.document_loaders`.
    - The `mode` parameter specifies how to handle multiple sections in a single Markdown file. It can be "single" (load each section as a separate document), "multi" (load all sections into a single document), or "all" (load each section and combine them into a single document).
    - Additional keyword arguments can be passed to the `MDLoader` constructor using `**kwargs`.

    Example Usage:
    - Load a Markdown file with multiple sections as separate documents
      >>> md_loader("path/to/markdownfile.md", mode="single")
    - Load a Markdown file and combine all sections into a single document
      >>> md_loader("path/to/markdownfile.md", mode="all")

    Exceptions:
    - If the specified file path does not exist or is inaccessible, a `FileNotFoundError` will be raised.
    - If there are issues with loading files, such as file format errors or permission issues, an exception will be raised.
    """

    try:
        # Create an instance of MDLoader with the specified parameters
        loader = UnstructuredMarkdownLoader(
            file_path = file_path,
            mode = mode,
            **kwargs
        )

        # Load data from the Markdown file using the MDLoader object
        data = loader.load()

        # Assert that the loaded data is not empty
        assert len(data) > 0
        # Assert that each document in the loaded data is an instance of Document
        assert isinstance(data[0], Document)

        # Return the list of loaded documents
        return data

    except Exception as e:
        print(f"Error loading data from Markdown file: {e}")
        return []

def json_loader(
        file_path: str,
        jq_schema: str,
        text_content: bool = False,
        **kwargs
        ) -> List[Document]:

    """
    Load documents from a JSON file using the specified parameters.

    Parameters:
    file_path (str): The path to the JSON file.
    jq_schema (str): A JSON query schema to filter and extract data.
    text_content (bool, optional): Whether to treat the content as plain text. Defaults to False.
    **kwargs: Additional keyword arguments passed to the JSONLoader constructor.
    Returns:
    List[Document]: A list of loaded documents.

    Notes:
    - This function uses the `JSONLoader` from `langchain_community.document_loaders`.
    - The `jq_schema` parameter specifies a JSON query schema to filter and extract data.
    - The `text_content` parameter determines whether to treat the content as plain text. If True, the loader will treat the content as plain text.
    Example Usage:
    - Load a JSON file with a specific schema
      >>> json_loader("path/to/jsonfile.json", jq_schema='{"key": "value"}')
    - Load a JSON file and treat the content as plain text
      >>> json_loader("path/to/jsonfile.json", text_content=True)

    Exceptions:
    - If the specified file path does not exist or is inaccessible, a `FileNotFoundError` will be raised.
    - If there are issues with loading files, such as file format errors or permission issues, an exception will be raised.
    """

    try:
        # Create an instance of JSONLoader with the specified parameters
        loader = JSONLoader(
            file_path = file_path,
            jq_schema = jq_schema,
            text_content = text_content,
            # Add any additional parameters here. Refer: https://python.langchain.com/docs/how_to/document_loader_json/
        )

        # Load data from the JSON file using the JSONLoader object
        data = loader.load()

        # Assert that the loaded data is not empty
        assert len(data) > 0
        # Assert that each document in the loaded data is an instance of Document
        assert isinstance(data[0], Document)

        # Return the list of loaded documents
        return data

    except Exception as e:
        print(f"Error loading data from JSON file: {e}")
        return []
 
def python_loader(file_path: str) -> List[Document]:

    """
    Load documents from a Python file using the specified parameters.

    Parameters:
    file_path (str): The path to the Python file.

    Returns:
    List[Document]: A list of loaded documents.

    Notes:
    - This function uses the `PythonLoader` from `langchain_community.document_loaders`.
    - The loader will extract code blocks and comments as separate documents.

    Example Usage:
    - Load a Python file
      >>> python_loader("path/to/pythonfile.py")

    Exceptions:
    - If the specified file path does not exist or is inaccessible, a `FileNotFoundError` will be raised.
    - If there are issues with loading files, such as file format errors or permission issues, an exception will be raised.
    """

    try:
        # Create an instance of PythonLoader with the specified file path
        loader = PythonLoader(file_path)

        # Load data from the Python file
        data = loader.load()

        # Assert that the loaded data is not empty
        assert len(data) > 0
        # Assert that the loaded data contains Document objects
        assert isinstance(data[0], Document)

        # Return the loaded data
        return data
    
    except Exception as e:
        print(f"Error loading data from JSON file: {e}")
        return []

def pdf_loader(
        file_path: str, 
        extraction_mode: Literal["plain", "structured"] = "plain",
        extract_images: bool = False,
        **kwargs
        ) -> List[Document]:
    """
    Load documents from a PDF file using PyMuPDFLoader. It extracts text and images from the PDF file.

    Parameters:
    file_path (str): The path to the PDF file to be loaded.
    extraction_mode (Literal["plain", "structured"]): Specifies how to extract text from the PDF file. Defaults to "plain".
    extract_images (bool, optional): Whether to extract images from the PDF file. Defaults to False.
    **kwargs: Additional keyword arguments to pass to the PyMuPDFLoader class.

    Returns:
    list[Document]: A list of Document objects, where each Document represents a page in the PDF file.

    Note:
    The function uses PyMuPDFLoader to load the PDF file. It asserts that the loaded data contains exactly one Document object per page.
    If an error occurs during loading, it prints an error message and returns an empty list.
    """

    try:
        loader = PyMuPDFLoader(
            file_path=file_path,
            password=kwargs.get("password", None),
            extract_images=extract_images,
            mode=extraction_mode,
            extract_tables=kwargs.get("extract_tables", None),
        )

        # Load data from the PDF file
        data = loader.load()

        # Assert that the loaded data contains Document object
        assert len(data) > 0
        assert isinstance(data[0], Document)

        # Return the loaded data
        return data
    except Exception as e:
        print(f"Error loading data from PDF file: {e}")
        return []

# def web_loader(
#         url_paths: List[str],
#         type: Literal['Simple', 'Advanced'] = 'Simple'
#         ) -> List[Document]:
    
#     try:
#         if type == 'Simple':
#             loader = WebBaseLoader(
#                 web_paths=url_paths,
#                 show_progress=True,
#             )
#         elif type == 'Advanced':
#             loader = UnstructuredLoader(
#                 web_url = url_paths[0]
#             )
        
#         data = loader.load()
        
#         # Assert that the loaded data contains Document object
#         assert isinstance(data[0], Document)

#         # Return the loaded data
#         return data

#     except Exception as e:
#         print(f"Error loading data from webpage: {e}")
#         return []

def main():

    # Look into the following for even more loaders: https://python.langchain.com/docs/integrations/document_loaders/
    dir_test_path = "./_data/_sample"
    file_test_path  = "./_data/_sample/sample.txt"
    csv_test_path = "./_data/_sample/sample.csv"
    md_test_path = "./_data/_sample/hello.md"
    json_test_path = "./_data/_sample/sample.json"
    python_test_path = "./_data/code/tmp_code_786742c6dd80cc2f248dc29c259da228f8cbc52ddebdf9e7f6533de589c42444.py"
    pdf_test_path = "./_data/10k/uber_2021.pdf"
    url_test_path = "https://python.langchain.com/docs/how_to/chatbots_memory/"
    

    data = dir_loader(dir_test_path)
    # data = file_loader(file_test_path, autodetect_encoding=True)
    # data = csv_loader(csv_test_path, autodetect_encoding=True)
    # data = md_loader(md_test_path)
    # data = json_loader(json_test_path, jq_schema=".image")
    # data = python_loader(python_test_path)
    # data = pdf_loader(pdf_test_path, extraction_mode="page",extract_images=True)
    # data = web_loader([url_test_path], type='Advanced')

    print(data)

    

if __name__ == "__main__":
    main()