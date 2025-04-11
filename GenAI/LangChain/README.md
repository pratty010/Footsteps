# LangChain: Quick Start Guide

LangChain simplifies building applications powered by language models. Use pre-built components to focus on development, not infrastructure.

## Installation

1.  **Clone:** `git clone <repository_url>`
2.  **Navigate:** `cd <langchain_directory>`
3.  **Install:** `pip install -r requirements.txt`

## Usage

### Examples Directory (`./_examples`)

#### LangChain Examples (`./_examples/_langchain`)

1.  [`models.py`](./_examples/_langchain/models.py): Initialize Gen AI models.
    *   `init_Ollama_model()`: Initializes an Ollama model with customizable parameters (model type, temperature, context length, etc.). Supports both Chat and LLM types.
    *   `init_Google_model()`: Initializes a Google Generative AI model with various configuration options. Supports Gemini models and both Chat and LLM types.
    *   `structured_output_llm()`: Configures language models to produce structured output according to defined schemas.
    *   Contains schema classes (`ConversationalResponse`, `StoryResponse`, `FinalResponse`) for structured model outputs.
    *   Demonstrates different invocation patterns including standard calls, streaming, and structured output generation.

2.  [`embeddings.py`](./_examples/_langchain/embeddings.py): Initialize embedding models.
    *   `init_Ollama_embed()`: Initializes an Ollama Embeddings model suitable for vector operations.
    *   `init_Google_embed()`: Initializes a Google Generative AI Embeddings model with configurable task types (e.g., 'retrieval_document').

3.  [`loaders.py`](./_examples/_langchain/loaders.py): Load documents from various sources.
    *   `dir_loader()`: Loads documents from a directory.
    *   `file_loader()`: Loads documents from a single text file (shown in use in `vector_store.py`).
    *   `csv_loader()`: Loads documents from a CSV file.
    *   `md_loader()`: Loads documents from a Markdown file.
    *   `json_loader()`: Loads documents from a JSON file.
    *   `python_loader()`: Loads a Python script as a document.
    *   `pdf_loader()`: Loads documents from a PDF file.
    *   `web_loader()`: Loads documents from web pages.

4.  [`splitters.py`](./_examples/_langchain/splitters.py): Split documents into chunks.
    *   `char_splitter()`: Splits text by characters.
    *   `rec_char_splitter()`: Splits text recursively by separators with configurable parameters for chunk size and overlap (shown in use in `vector_store.py`).
    *   `md_header_splitter()`: Splits Markdown documents by headers.
    *   `html_splitter()`: Splits HTML documents by headers.
    *   `rec_json_splitter()`: Splits JSON data recursively.

5.  [`vector_store.py`](./_examples/_langchain/vector_store.py): Create and manage vector stores.
    *   `Init_VS`: Class for initializing and managing different types of vector stores (InMemory, Chroma, Qdrant, FAISS).
        *   `__init__()`: Initializes with an embedding model and specifies the vector store type.
        *   `__call__()`: Creates and returns a configured vector store instance with optional custom parameters.
        *   `add_documents()`: Adds Document objects to the vector store with optional custom IDs.
        *   `add_texts()`: Adds text strings with optional metadata and IDs to the vector store.
        *   `delete_documents()`: Removes documents from the vector store by their IDs.
        *   `get_vs_retriever()`: Creates a configurable retriever from the vector store with customizable search parameters.
    *   Contains a practical `main()` function showing a complete workflow: initializing embeddings, creating a vector store, adding documents, and performing similarity searches.

6.  [`tools_usage.py`](./_examples/_langchain/tools_usage.py): Define and use tools with language models.
    *   Simple calculation tools: `multiply()` and `add()` for numeric operations.
    *   Tool execution functions:
        *   `simple_tool_usage()`: Demonstrates a complete tool usage flow from query to final response.
        *   `call_tools()`: Executes tool calls sequentially using a tool mapping approach.
        *   `human_approval()`: Prompts for user confirmation before executing tool calls.
    *   Custom exceptions like `NotApproved` for handling tool execution errors.
    *   `main()` function showing how to chain tools with approval processes.

7.  [`agent.py`](./_examples/_langchain/agent.py): Create and use agents with language models.
    *   Integrates multiple tools (web search and document retrieval) with a language model.
    *   `TavilySearchResults`: Tool for searching the web for current information.
    *   Document processing workflow: loads web content, splits into chunks, creates vector embeddings.
    *   `create_retriever_tool()`: Creates a specialized tool for searching a specific knowledge base.
    *   Agent initialization using LangChain Hub prompt templates.
    *   Demonstrates chat history usage to maintain context across interactions.
    *   Shows complete agent setup with tool binding, executor configuration, and response handling.
    *   Includes commented test sections for individual components (search, retriever, LLM).

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

- **How do I create a custom chain?**
  Use the Chain class or combine existing chains with the SequentialChain class.
  
- **How do I use document loaders?**
  Import the appropriate loader from `langchain.document_loaders` and initialize it with your file path.

### Troubleshooting

- **Missing dependencies?**
  `pip install -r requirements.txt`

- **Unexpected model results?**
  Experiment with prompts and model parameters. Consult model documentation and LangChain documentation.

- **Memory issues with large documents?**
  Use appropriate document splitters and chunk sizes.

## Advanced Usage

- **Memory**: Add conversational memory to chains and agents with `ConversationBufferMemory`
- **Retrieval**: Create RAG applications with document retrievers
- **Custom Tools**: Define your own tools for agents to use
- **Output Parsers**: Control the format of LLM outputs

## Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [Community Discord](https://discord.gg/langchain)
