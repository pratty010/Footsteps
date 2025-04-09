# LangChain

If you're new to LangChain, this project is designed to help you get started quickly and easily. By using our pre-built components and abstractions, you can focus on developing your application rather than reinventing the wheel.

## Requirements

LangChain requires several dependencies to function properly. These dependencies are listed in the [`requirements.txt`](./requirements.txt) file.

## Installation

To install LangChain and its dependencies, follow these steps:

1. Clone the repository using a package manager of your choice (e.g., pip).
2. Navigate to the project directory.
3. Install the dependencies using pip (or the chosen package manager).

For example, you can use `pip` as follows:
```bash
pip install -r requirements.txt
```

## Usage:

### Examples Directory

1. [`Models.py`](./_examples/models.py): Easy and basic setup scripts for various open source or free Gen AI models.
    * `init_Ollama_model()`: Initializes an Ollama model for text generation or chat completion.
    * `init_Google_model()`: Initializes a Google Generative AI model for text generation or chat completion.

2. [`Embeddings.py`](./_examples/embeddings.py) : Easy and basic setup scripts for various open source or free embedding models.
    * `init_Ollama_embed`: Initializes an Ollama Embeddings model with the specified settings.
    * `init_Google_embed`: Initializes a Google Generative AI Embeddings model with the specified settings.

3. [`Loaders.py`](./_examples/loaders.py) : Easy and basic setup scripts for various Langchain supported loaders.


## Frequently Asked Questions (FAQs)

### General
- **What is LangChain?**
  LangChain is a unified toolkit for building applications with language models.

- **Why use LangChain?**
  LangChain simplifies the process of integrating AI into applications by providing pre-built components and abstractions for common tasks such as text generation, retrieval, and more.

If you have any specific questions about using LangChain, feel free to ask!
