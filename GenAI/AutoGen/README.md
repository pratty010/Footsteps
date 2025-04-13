# AutoGen Framework: Key Concepts

## Introduction
AutoGen is a framework from Microsoft Research that enables building multi-agent systems where AI agents can collaborate with humans and use tools to solve complex tasks. The framework allows agents to:

- Engage in multi-step reasoning processes
- Generate and execute plans to accomplish goals
- Use a variety of tools including code execution, API calls, and web browsing
- Maintain context through extended conversation chains
- Revise approaches based on feedback and new information

This framework provides a flexible architecture for creating advanced conversational systems where multiple specialized agents can work together, maintain state, and execute complex reasoning flows with improved reliability.

## Installation

1.  **Clone:** `git clone <repository_url>`
2.  **Navigate:** `cd <autogen_directory>`
3.  **Install:** `pip install -r requirements.txt`


## Usage

### Examples Directory (`./_examples`)

1. [`models.py`](./_examples/models.py): Initialize and work with Gen AI models.
   * `get_ollama_client()`: Creates an Ollama client with configurable parameters including model type (llama3.2:3b, qwen2.5:14b, etc.), host, timeout, and model capabilities like JSON output and function calling.
   * `get_gemini_client()`: Creates a Gemini client that works with Google's models (gemini-2.0-flash, gemini-2.5-pro-exp, gemini-1.5-flash) and supports similar configuration options as the Ollama client, including response format, timeout settings, and model capabilities.
   * Contains a `StructuredOutput` schema class for defining structured model outputs with fields for answer and reason.
   * `llm_with_streaming()`: Implements streaming responses from LLMs, displaying content chunks as they arrive.
   * `llm_with_cache()`: Implements caching for LLM responses to avoid redundant API calls, using DiskCacheStore for persistence.
   * `llm_with_history()`: Manages conversation context by appending responses and follow-up queries to the message history.
   * `llm_with_struct_output()`: Processes structured output responses and extracts the formatted data.
   * Demonstrates various usage patterns in the `main()` function:
     - Standard LLM calls with both Ollama and Gemini models
     - Streaming responses with `llm_with_streaming()`
     - Caching with `llm_with_cache()`
     - Conversation history with `llm_with_history()`
     - Structured output generation (commented example)

