from langchain_community.document_loaders import (
    DirectoryLoader, 
    TextLoader,
    CSVLoader,
    UnstructuredMarkdownLoader,
    PythonLoader,
    PyMuPDFLoader,
    PyPDFLoader,
    WebBaseLoader
)

from langchain_unstructured import UnstructuredLoader

from langchain_text_splitters import (
    TextSplitter,
)

from langchain_core.documents import Document

from rich import pretty, print

def dir_loader(dir_path: str, glob: str="**/*.md", show_progress: bool = True, loader_cls=TextLoader, **kwargs) -> list[Document]:
    """
    This function loads data from a directory using the specified loader class and glob pattern.

    Parameters:
    dir_path (str): The path to the directory to load data from.
    glob (str, optional): The glob pattern to match files in the directory. Defaults to "**/*.md".
    show_progress (bool, optional): Whether to show progress during loading. Defaults to True.
    loader_cls (class, optional): The class to use for loading data. Defaults to TextLoader.
    **kwargs: Additional keyword arguments to pass to the loader class.

    Returns:
    list: A list of Document objects loaded from the directory.

    Note:
    This function initializes the DirectoryLoader with the specified parameters, loads data from the directory,
    prints the content of the first loaded document for debugging purposes, and returns the loaded documents.
    """
    try:
        # Initialize the DirectoryLoader with the specified parameters
        loader = DirectoryLoader(
            path = dir_path,
            glob=glob,
            show_progress = True,
            loader_cls=loader_cls,
            use_multithreading=kwargs.get('use_multithreading', False),
            max_concurrency=kwargs.get('max_max_concurrency', 4),
            sample_seed=kwargs.get('max_max_concurrency', None),
            silent_errors=kwargs.get('silent_errors', False),
        )

        # Load data from the directory
        data = loader.load()

        # Assert that the loaded data is a list of Document
        assert isinstance(data[0], Document)

        # # Print the content of the first loaded document for debugging purposes
        # pretty.pprint(docs[0].page_content)

        # Return the loaded documents
        return data
    
    except Exception as e:
        print(f"Error loading data from directory: {e}")
        return []

def file_loader(file_path: str, encoding: str = None, autodetect_encoding: bool = False, splitter: TextSplitter = None) -> list[Document]:
    """
    This function loads text data from a specified file into a list of Document objects.

    Parameters:
    file_path (str): The path to the text file to be loaded.
    encoding (str, optional): The encoding to be used for decoding the text file. If not provided, the encoding will be
        automatically detected. Defaults to None.
    autodetect_encoding (bool, optional): Whether to automatically detect the encoding of the text file. If set to True,
        the encoding will be detected based on the file's content. Defaults to False.

    Returns:
    list[Document]: A list of Document objects, where each Document represents a line in the text file.

    Note:
    This function uses the TextLoader class from the langchain_community.document_loaders module to load the text data.
    It asserts that the loaded data is a list of Document objects.
    """

    try: 
        # Create an instance of TextLoader with the specified file path and autodetect encoding
        loader = TextLoader(
            file_path = file_path,
            encoding=encoding,
            autodetect_encoding=autodetect_encoding,
        )

        # Load data from the text file
        if splitter:
            data = loader.load_and_split(splitter)
        else:
            data = loader.load()

        # Assert that the loaded data is a list of Document
        assert isinstance(data[0], Document)

        return data
    
    except Exception as e:
        print(f"Error loading data from text file: {e}")
        return []

def csv_loader(file_path: str, source_column: str = None, encoding = None, autodetect_encoding: bool = False, csv_args: dict = {
    "delimiter": ",",
    "quotechar": '"',
    },
    splitter: TextSplitter = None,
    **kwargs,
    ) -> list[Document]:
    """
    This function loads data from a CSV file into a list of Document objects.

    Parameters:
    file_path (str): The path to the CSV file to be loaded.
    source_column (str, optional): The name of the column to be used as the source for the Document objects.
        Defaults to None, which means that the entire CSV file will be loaded as a single Document.
    encoding (str, optional): The encoding to be used for decoding the CSV file. If not provided, the encoding will be
        automatically detected. Defaults to None.
    autodetect_encoding (bool, optional): Whether to automatically detect the encoding of the CSV file. If set to True,
        the encoding will be detected based on the file's content. Defaults to False.
    csv_args (dict, optional): Additional arguments to be passed to the CSV reader. Defaults to {"delimiter": ",", "quotechar": '"'}
    splitter (TextSplitter, optional): A TextSplitter object to be used for splitting the loaded data into smaller chunks.
        Defaults to None, which means that the entire CSV file will be loaded as a single Document.
    **kwargs: Additional keyword arguments to pass to the CSVLoader class.

    Returns:
    list[Document]: A list of Document objects, where each Document represents a row in the CSV file.

    Note:
    This function uses the CSVLoader class from the langchain_community.document_loaders module to load the CSV data.
    It asserts that the loaded data is a list of Document objects.
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

        # load data from CSV
        if splitter:
            data = loader.load_and_split(splitter)
        else:
            data = loader.load()

        # Assert that the loaded data is a list of Document
        assert isinstance(data[0], Document)

        return data

    except Exception as e:
        print(f"Error loading data from CSV file: {e}")
        return []

def md_loader(file_path: str, mode: str = "single", splitter: TextSplitter = None) -> list[Document]:
    """
    This function loads data from a Markdown file using the UnstructuredMarkdownLoader.

    Parameters:
    file_path (str): The path to the Markdown file to be loaded.
    mode (str, optional): The mode in which to load the Markdown file.
        Defaults to "single", which means that the entire Markdown file will be loaded as a single Document.
        Other possible values include "multi" for loading multiple Markdown documents from a single file.
    splitter (TextSplitter, optional): A TextSplitter object to be used for splitting the loaded data into smaller chunks.
        Defaults to None, which means that the entire Markdown file will be loaded as a single Document.

    Returns:
    list[Document]: A list of Document objects, where each Document represents a Markdown document.
        If the mode is "single", the list will contain a single Document.
        If the mode is "multi", the list will contain multiple Document objects, each representing a separate Markdown document.

    Raises:
    None

    Note:
    This function uses the UnstructuredMarkdownLoader class from the langchain_community.document_loaders module to load the Markdown data.
    It asserts that the loaded data contains Document object.
    If an error occurs during loading, it prints an error message and returns an empty list.
    """
    try:
        # Create an instance of UnstructuredMarkdownLoader with the specified file path
        loader = UnstructuredMarkdownLoader(
            file_path=file_path,
            mode=mode,
        )

        # Load data from the Markdown file
        if splitter:
            data = loader.load_and_split(splitter)
        else:
            data = loader.load()

        # Assert that the loaded data contains Document object
        assert isinstance(data[0], Document)

        # Return the loaded data
        return data
    except:
        print(f"Error loading data from Markdown file: {sys.exc_info()[1]}")
        return []

def python_loader(file_path: str, splitter: TextSplitter = None) -> list[Document]:
    """
    This function loads data from a Python (.py) file using PythonLoader.
    It then returns a list of Document objects, each representing a line in the Python file.

    Parameters:
    file_path (str): The path to the Python (.py) file.
    splitter (TextSplitter, optional): A TextSplitter object to be used for splitting the loaded data into smaller chunks.
        Defaults to None, which means that the entire Python file will be loaded as a single Document.

    Returns:
    list[Document]: A list of Document objects, each representing a line in the Python file.

    Raises:
    None

    Note:
    The PythonLoader reads the file line by line and creates a Document object for each line.
    The page_content of each Document object is the content of the corresponding line in the Python file.
    """
    # Create an instance of PythonLoader with the specified file path
    loader = PythonLoader(file_path)

    # Load data from the Python file
    if splitter:
        data = loader.load_and_split()
    else:
        data = loader.load()

    # Assert that the loaded data contains Document objects
    assert isinstance(data[0], Document)

    # Return the loaded data
    return data

def pdf_loader(file_path: str, extraction_mode: str, extract_images: bool = False,  splitter: TextSplitter = None, **kwargs) -> list[Document]:
    """
    This function loads data from a PDF file using PyMuPDFLoader. It extracts text, images, and tables from the PDF file.

    Parameters:
    file_path (str): The path to the PDF file to be loaded.
    extract_images (bool, optional): Whether to extract images from the PDF file. Defaults to False.
    extraction_mode (str, optional): The mode in which to extract text from the PDF file. Defaults to "plain".
    splitter (TextSplitter, optional): A TextSplitter object to be used for splitting the loaded data into smaller chunks. Defaults to None.
    **kwargs: Additional keyword arguments to pass to the PyMuPDFLoader class.

    Returns:
    list[Document]: A list of Document objects, where each Document represents a page in the PDF file.

    Note:
    The function uses PyMuPDFLoader to load the PDF file. It asserts that the loaded data contains exactly one Document object per page.
    If an error occurs during loading, it prints an error message and returns an empty list.
    """
    loader = PyMuPDFLoader(
        file_path=file_path,
        password=kwargs.get("password", None),
        extract_images=extract_images,
        mode=extraction_mode,
        extract_tables=kwargs.get("extract_tables", None),
    )

    # Load data from the PDF file
    if splitter:
        data = loader.load_and_split(splitter)
    else:
        data = loader.load()

    # Assert that the loaded data contains Document object
    assert len(data) == 1
    assert isinstance(data[0], Document)

    # Return the loaded data
    return data

def web_loader(url_path: str, splitter: TextSplitter = None) -> list[Document]:
    """
    This function loads data from a webpage using the UnstructuredLoader.

    Parameters:
    url_path (str): The URL of the webpage to be loaded.
    splitter (TextSplitter, optional): A TextSplitter object to be used for splitting the loaded data into smaller chunks.
        Defaults to None, which means that the entire webpage will be loaded as a single Document.

    Returns:
    list[Document]: A list of Document objects, where each Document represents a webpage.
        If the webpage contains multiple sections, the list will contain multiple Document objects, each representing a separate section.

    Raises:
    None

    Note:
    This function uses the UnstructuredLoader class from the langchain_unstructured module to load the webpage data.
    It asserts that the loaded data contains Document object.
    If an error occurs during loading, it prints an error message and returns an empty list.
    """
    try:
        # Create an instance of WebLoader with the specified URL
        loader = UnstructuredLoader(
            web_url=url_path,
        )

        # Load data from the webpage
        if splitter:
            data = loader.load_and_split(splitter)
        else:
            data = loader.load()

        # Assert that the loaded data contains Document object
        assert isinstance(data[0], Document)

        # Return the loaded data
        return data

    except Exception as e:
        print(f"Error loading data from webpage: {e}")
        return []


def main():

    # Look into the following for even more loaders: https://python.langchain.com/docs/integrations/document_loaders/

    dir_test_path = "./_knowledge/_sec_tools"
    file_test_path  = "./_knowledge/_sec_tools/nmap/tool_help.txt"
    csv_test_path = "./_data/Fin/historical.csv"
    md_test_path = "./_data/Chocolate Factory/Write_Up.md"
    python_test_path = "./_data/code/tmp_code_786742c6dd80cc2f248dc29c259da228f8cbc52ddebdf9e7f6533de589c42444.py"
    pdf_test_path = "./_data/10k/uber_2021.pdf"
    url_test_path = "https://python.langchain.com/docs/how_to/chatbots_memory/"
    

    data = dir_loader(dir_test_path, "**/*.txt")
    # data = file_loader(file_test_path, autodetect_encoding=True)
    # data = csv_loader(csv_test_path, autodetect_encoding=True)
    # data = md_loader(md_test_path)
    # data = python_loader(python_test_path)
    # data = pdf_loader(pdf_test_path, extraction_mode="page",extract_images=True)
    # data = web_loader(url_test_path)

    pretty.pprint(data)

    

if __name__ == "__main__":
    main()