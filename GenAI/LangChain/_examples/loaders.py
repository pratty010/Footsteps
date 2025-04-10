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
    UnstructuredMarkdownLoader,
)

from langchain_core.documents import Document

from rich import print
from typing import List, Literal, Type

def dir_loader(
        dir_path: str,
        glob: Literal['**/[!.]*', '**/*.md', '**/*.txt', '**/*.csv', '**/*.py', '**/*.pdf', '**/*.html', '**/*.json'] = '**/*.md',
        show_progress: bool = True,
        recursive : bool = False,
        loader_cls: Type[TextLoader | CSVLoader | BSHTMLLoader | UnstructuredFileLoader] = TextLoader,
        **kwargs
        ) -> List[Document]:
    """
    Loads documents from a directory using the specified loader class and glob pattern.
    
    Args:
        dir_path (str): The path to the directory containing the documents.
        glob (Literal['**/[!.]*', '**/*.md', '**/*.txt', '**/*.csv', '**/*.py', '**/*.pdf', '**/*.html', '**/*.json'], optional):
            The glob pattern to match files in the directory. Defaults to '**/*.md'.
        show_progress (bool, optional): Whether to show a progress bar during loading. Defaults to True.
        recursive (bool, optional): Whether to recursively load documents from subdirectories. Defaults to False.
        loader_cls (Type[TextLoader | CSVLoader | BSHTMLLoader | UnstructuredFileLoader], optional):
            The class of the document loader to use. Defaults to TextLoader.

    Returns:
        List[Document]: A list of loaded documents.

    Notes:
       - The `loader_cls` parameter can be any subclass of `TextLoader`, `CSVLoader`, `BSHTMLLoader`, or `UnstructuredFileLoader`.
       - The `glob` parameter can be any of the following literals: '**/[!.]*', '**/*.md', '**/*.txt', '**/*.csv', '**/*.py', '**/*.pdf', '**/*.html', '**/*.json'.
       - The `show_progress` parameter can be either True or False.
       - The `recursive` parameter can be either True or False.

    Examples:
        >>> documents = load_documents(dir_path='data', glob='**/*.md')
        >>> print(documents)

    Exceptions:
       ValueError: If the specified glob pattern is not supported.
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
        mode: Literal['single', 'elements', 'paged'] = "elements",
        **kwargs
        ) -> List[Document]:

    """
    Load documents from a Markdown file using the specified parameters.

    Parameters:
    file_path (str): The path to the Markdown file.
    mode (Literal['single', 'elements', 'paged'): Specifies how the markdown file is split into documents.
        'single' creates a single document for the entire file.
        'elements' creates a document for each element in the file (e.g., headings, paragraphs).
        'paged' attempts to split the document into pages. Defaults to "elements".
    **kwargs: Additional keyword arguments passed to the UnstructuredMarkdownLoader constructor.

    Returns:
    List[Document]: A list of loaded documents.

    Notes:
    - This function uses the `UnstructuredMarkdownLoader` from `langchain_community.document_loaders`.
    - Additional keyword arguments can be passed to the `UnstructuredMarkdownLoader` constructor using `**kwargs`.

    Example Usage:
    - Load a Markdown file as a single document:
      >>> md_loader("path/to/markdownfile.md", mode="single")
    - Load a Markdown file and create a document for each element:
      >>> md_loader("path/to/markdownfile.md", mode="elements")
    - Load a Markdown file and attempt to split it into pages:
      >>> md_loader("path/to/markdownfile.md", mode="paged")

    Exceptions:
    - If the specified file path does not exist or is inaccessible, a `FileNotFoundError` will be raised.
    - If there are issues with loading files, such as file format errors or permission issues, an exception will be raised.
    """

    try:
        # Create an instance of UnstructuredMarkdownLoader with the specified parameters
        loader = UnstructuredMarkdownLoader(
            file_path = file_path,
            mode = mode,
            **kwargs
        )

        # Load data from the Markdown file using the UnstructuredMarkdownLoader object
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
    Load a Python script as a document using the specified parameters.

    Parameters:
    file_path (str): The path to the Python script file.
    
    Returns:
    List[Document]: A list containing a single Document object representing the content of the Python script.

    Notes:
    - This function uses the `PythonLoader` from `langchain_community.document_loaders`.
    Example Usage:
    - Load a Python script and treat its content as plain text
      >>> python_loader("path/to/script.py")

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
        print(f"Error loading data from text file: {e}")
        return []

def pdf_loader(
        file_path: str,
        loader_type: Type[PyPDFLoader | PyMuPDFLoader] = PyPDFLoader,
        mode : Literal["single", "page"] = "page",
        extraction_mode: Literal['plain', 'layout'] = "layout",
        extract_images: bool = False,
        **kwargs,
        ) -> List[Document]:

    """
    Load documents from a PDF file using the specified parameters.

    Parameters:
    file_path (str): The path to the PDF file.
    loader_type (Type[PyPDFLoader | PyMuPDFLoader]): Specifies which PDF loader to use. Defaults to `PyPDFLoader`.
    mode (Literal["single", "page"]): Specifies how to handle multiple pages in a single PDF file. Defaults to "page".
    extraction_mode (Literal['plain', 'layout']): Specifies the extraction mode for text content. Defaults to "layout".
    extract_images (bool, optional): Whether to extract images from the PDF. Defaults to False.
    **kwargs: Additional keyword arguments passed to the loader constructor.
    Returns:
    List[Document]: A list of loaded documents.

    Notes:
    - This function uses either `PyPDFLoader` or `PyMuPDFLoader` from `langchain_community.document_loaders`.
    - The `mode` parameter specifies how to handle multiple pages in a single PDF file. It can be "single" (load each page as a separate document) or "page" (load all pages into a single document).
    - The `extraction_mode` parameter specifies the extraction mode for text content. It can be "plain" (extract plain text) or "layout" (extract text with layout information).
    - Additional keyword arguments can be passed to the loader constructor using `**kwargs`.

    Example Usage:
    - Load a PDF file with multiple pages as separate documents
      >>> pdf_loader("path/to/pdffile.pdf", mode="single")
    - Load a PDF file and combine all pages into a single document
      >>> pdf_loader("path/to/pdffile.pdf", mode="page")

    Exceptions:
    - If the specified file path does not exist or is inaccessible, a `FileNotFoundError` will be raised.
    - If there are issues with loading files, such as file format errors or permission issues, an exception will be raised.
    """

    try:
        loader = loader_type(
            file_path = file_path,
            mode = mode,
            extraction_mode = extraction_mode,
            extract_images = extract_images,
            password=kwargs.get("password", None),
        )

        # # Uncomment if using PyMuPDFLoader instead of PyPDFLoader
        # PyMuPDFLoader(
        #     file_path=file_path,
        #     password=kwargs.get("password", None),
        #     extract_images=extract_images,
        #     mode=extraction_mode,
        #     extract_tables=kwargs.get("extract_tables", None),
        # )

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

def web_loader(
        url_paths: List[str],
        requests_per_second: int = 2,
        default_parser: str = 'html.parser',
        autoset_encoding: bool = True,
        show_progress: bool = True,
        **kwargs
        ) -> List[Document]:
    
    """
    Load documents from web pages using the specified parameters.

    Parameters:
    url_paths (List[str]): A list of URLs to load.
    requests_per_second (int, optional): The number of requests per second. Defaults to 2.
    default_parser (str, optional): The default parser for HTML content. Defaults to 'html.parser'.
    autoset_encoding (bool, optional): Whether to automatically set the encoding. Defaults to True.
    show_progress (bool, optional): Whether to show a progress bar. Defaults to True.
    **kwargs: Additional keyword arguments passed to the WebBaseLoader constructor.
    Returns:
    List[Document]: A list of loaded documents.

    Notes:
    - This function uses the `WebBaseLoader` from `langchain_community.document_loaders`.
    - The `requests_per_second` parameter specifies the number of requests per second.
    - The `default_parser` parameter specifies the default parser for HTML content.
    - The `autoset_encoding` parameter determines whether to automatically set the encoding.
    - The `show_progress` parameter controls whether a progress bar is shown during loading.

    Example Usage:
    - Load documents from multiple web pages
      >>> web_loader(["https://example.com/page1", "https://example.com/page2"])

    Exceptions:
    - If there are issues with loading files, such as network errors or permission issues, an exception will be raised.
    """

    try:
        # Initialize the loader with the URL paths and show progress bar
        loader = WebBaseLoader(
            web_paths=url_paths,
            requests_per_second = requests_per_second,
            default_parser = default_parser,
            autoset_encoding = autoset_encoding,
            show_progress = show_progress,
            # For any additional keyword arguments, Refer: https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.web_base.WebBaseLoader.html
        )
       
       # Load data from the web pages
        data = loader.load()
        
        # Check if the data is loaded successfully
        assert data is not None and len(data) > 0
        # Assert that the loaded data contains Document object
        assert isinstance(data[0], Document)

        # Return the loaded data
        return data

    except Exception as e:
        print(f"Error loading data from webpage: {e}")
        return []

def main():

    # Look into the following for even more loaders: https://python.langchain.com/docs/integrations/document_loaders/
    dir_test_path = "./_data/_sample"
    file_test_path  = "./_data/_sample/sample.txt"
    csv_test_path = "./_data/_sample/sample.csv"
    md_test_path = "./_data/_sample/hello.md"
    json_test_path = "./_data/_sample/sample.json"
    python_test_path = "./_data/_sample/example.py"
    pdf_test_path = "./_data/_sample/layout-parser-paper.pdf"
    url_test_paths = ["https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.web_base.WebBaseLoader.html",]
    

    # data = dir_loader(dir_test_path)
    # data = file_loader(file_test_path, autodetect_encoding=True)
    # data = csv_loader(csv_test_path, autodetect_encoding=True)
    # data = md_loader(md_test_path)
    # data = json_loader(json_test_path, jq_schema=".image")
    # data = python_loader(python_test_path)
    # data = pdf_loader(pdf_test_path, extract_images=True)
    data = web_loader(url_paths=url_test_paths)

    print(data)

    

if __name__ == "__main__":
    main()