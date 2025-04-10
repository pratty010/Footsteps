# LangChain: Quick Start Guide

LangChain simplifies building applications powered by language models. Use pre-built components to focus on development, not infrastructure.
## Installation

1.  **Clone:** `git clone <repository_url>`
2.  **Navigate:** `cd <langchain_directory>`
3.  **Install:** `pip install -r requirements.txt`

## Usage

### Examples Directory (`./_examples`)

1.  [`models.py`](./_examples/models.py): Initialize Gen AI models.
    *   `init_Ollama_model()`: Initializes an Ollama model.
    *   `init_Google_model()`: Initializes a Google model.

2.  [`embeddings.py`](./_examples/embeddings.py): Initialize embedding models.
    *   `init_Ollama_embed`: Initializes an Ollama Embeddings model.
    *   `init_Google_embed`: Initializes a Google Generative AI Embeddings model.

3.  [`loaders.py`](./_examples/loaders.py): Load documents from various sources.
    *   `dir_loader()`: Loads documents from a directory.
    *   `file_loader()`: Loads documents from a single text file.
    *   `csv_loader()`: Loads documents from a CSV file.
    *   `md_loader()`: Loads documents from a Markdown file.
    *   `json_loader()`: Loads documents from a JSON file.
    *   `python_loader()`: Loads a Python script as a document.
    *   `pdf_loader()`: Loads documents from a PDF file.
    *   `web_loader()`: Loads documents from web pages.

4.  [`splitters.py`](./_examples/splitters.py): Split documents into chunks.
    *   `char_splitter()`: Splits text by characters.
    *   `rec_char_splitter()`: Splits text recursively by separators.
    *   `md_header_splitter()`: Splits Markdown documents by headers.
    *   `html_splitter()`: Splits HTML documents by headers.
    *   `rec_json_splitter()`: Splits JSON data recursively.

5.  [`vector_store.py`](./_examples/vector_store.py): Create and manage vector stores.
    *   `CreateVS`: Class for initializing vector stores.
        *   `__init__`: Initializes the CreateVS instance with an embedding model.
        *   `__call__`: Initializes and returns a Vector Store instance.
        *   `add_documents`: Adds documents to the Vector Store.
        *   `add_texts`: Adds texts to the Vector Store.
        *   `delete_documents`: Deletes documents from the Vector Store.
        *   `get_vs_retriever`: Creates a retriever instance from the Vector Store.

## FAQ

### General

- **What is LangChain?**

  A framework for building applications powered by language models.
  
- **Why use LangChain?**

  Simplifies AI integration: text generation, document loading, splitting, embeddings, vector stores, chains, and agents.

- **What are Chains?**

  Sequences of calls to language models or utilities.

- **What are Agents?**

  Language models that take actions using defined tools.


### Getting Started

- **Where are examples?**

  [`_examples`](./_examples) directory.

  
### Troubleshooting

- **Missing dependencies?**

  `pip install -r requirements.txt`

- **Unexpected model results?**

  Experiment with prompts and model parameters.  Consult model documentation and LangChain documentation.
