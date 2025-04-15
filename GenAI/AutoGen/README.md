# AutoGen Framework: Key Concepts

## Introduction

AutoGen is a framework from Microsoft Research that enables building multi-agent systems where AI agents can collaborate with humans and use tools to solve complex tasks. The framework allows agents to:

- Engage in multi-step reasoning processes
- Generate and execute plans to accomplish goals
- Use a variety of tools including code execution, API calls, and web browsing
- Maintain context through extended conversation chains
- Revise approaches based on feedback and new information

In our implementation, we've expanded on these capabilities by:

- Integrating multiple LLM providers (Ollama, Gemini, OpenAI) with configurable parameters
- Implementing various interaction patterns like streaming, caching, and conversation history management
- Creating structured output schemas for consistent agent responses
- Developing specialized agents including basic assistants, user proxies, code execution agents, and Society of Mind (SoM) agents
- Enabling tool usage with examples like binary verification tools
- Supporting team collaboration patterns between multiple agents

This framework provides a flexible architecture for creating advanced conversational systems where multiple specialized agents can work together, maintain state, and execute complex reasoning flows with improved reliability.

## Installation

1.  **Clone:** `git clone <repository_url>`
2.  **Navigate:** `cd <autogen_directory>`
3.  **Install:** `pip install -r requirements.txt`


## Usage

### Examples Directory (`./_examples`)

1. [`models.py`](./_examples/models.py): Initialize and work with Gen AI models.
   * `get_ollama_client()`: Creates an Ollama client with configurable parameters for models (llama3.2:3b, qwen2.5:14b, deepseek-r1:14b, qwen2.5-coder:7b), host, timeout, and various model capabilities.
   * `get_gemini_client()`: Creates a Gemini client for working with Google's models like gemini-1.5-flash.
   * `get_openai_client()`: Creates an OpenAI client with configurable parameters including model name, base URL, API key, and model capabilities.
   * Contains `StructuredOutput` schema class for defining structured model outputs.
   * Implements various LLM interaction patterns:
     - `llm_with_streaming()`: Displays content chunks as they arrive
     - `llm_with_cache()`: Caches responses to avoid redundant API calls
     - `llm_with_history()`: Manages conversation context
     - `llm_with_struct_output()`: Processes structured output responses

2. [`agents.py`](./_examples/agents.py): Implements various agent types and patterns.
   * Defines `StructuredOutput` schema for structured agent responses
   * `basic_assistant_agent()`: Creates and invokes a basic assistant agent
   * `agent_with_streaming()`: Demonstrates agents with streaming capabilities
   * `agent_with_tools()`: Shows how to create agents with access to tools like `check_binary_tool`
   * `basic_user_proxy_agent()`: Creates a user proxy agent for human interaction
   * `code_exec_agent()`: Implements a code execution agent using `LocalCommandLineCodeExecutor`
   * `som_agent()`: Creates a Society of Mind agent with writer and critic sub-agents
   * Each function demonstrates different agent capabilities, including structured output, tool usage, streaming, and multi-agent collaboration

3. [`teams.py`](./_examples/teams.py): Showcases how to build and manage collaborative agent teams. This example illustrates the implementation of different team communication patterns, such as:
   - **Round-Robin Group Chat**: Demonstrates a coordinated approach for web research tasks using multiple agents. Agents, including a web researcher, a critic for feedback, and a user proxy, engage in a dynamic dialogue to complete research assignments.
   - **Selector Group Chat**: Coordinates mathematical calculation tasks using agents specialized in specific operations like addition and multiplication. The SelectorGroupChat smartly determines which agent should respond based on the task at hand, ensuring efficient problem-solving.
   - Each team setup includes agents using advanced functionality like streaming model clients, termination conditions, and tool usage for enriched collaboration.

The examples directory showcases both basic and advanced patterns for working with LLMs and agents in the AutoGen framework, providing implementation samples for various use cases.

