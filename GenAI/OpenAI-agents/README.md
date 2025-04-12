# OpenAI Agents SDK: Quick Start Guide

## Introduction
OpenAI Agents SDK provides tools to build AI agents that can think, reason, and interact with tools to solve complex tasks. The SDK enables you to create applications with AI agents that can:

- Reason through multi-step problems
- Generate and execute plans to accomplish goals
- Use a set of tools including code, APIs, web browsing, and more
- Maintain context through extended interactions
- Think and revise their approaches based on new information or constraints

This SDK simplifies developing with the OpenAI Assistant API by providing a Python interface for creating agents that can use specialized tools, maintain state, and execute complex reasoning flows with improved reliability.

Whether you're building a coding assistant, a document analyzer, or a complex decision-making system, the OpenAI Agents SDK helps you create more capable and controlled AI applications that can adapt to your specific requirements.

## Installation

1.  **Clone:** `git clone <repository_url>`
2.  **Navigate:** `cd <langchain_directory>`
3.  **Install:** `pip install -r requirements.txt`

## Usage

### Examples Directory (`./_examples`)

The `_examples` directory contains several files demonstrating different ways to use the OpenAI Agents SDK:
1. [`model.py`](./_examples/model.py): Initialize and configure various AI agent models.
   * Demonstrates three configuration approaches for OpenAI agents:
     * Using an OpenAI client directly with explicit configurations
     * Using global settings with `set_default_openai_client` and `set_default_openai_api`
     * Using a custom model provider with local settings via `ModelProvider` class
   * Contains implementation of a `CustomModelProvider` class that uses external clients for model inference
   * Shows how to configure agents with different instruction sets and model parameters
   * Provides examples of running agents with different configurations using the `Runner.run()` method
   * Demonstrates environment variable handling for API keys and model settings
   * Includes practical examples for travel planning scenarios to showcase agent capabilities

2. [`agent_examples.py`](./_examples/agent_examples.py): Showcases various agent implementations including:
   * `basic_agent()`: A simple agent implementation that responds to user queries
   * `agent_with_handoffs()`: Demonstrates agent triage system that can route queries to specialized agents
   * `agent_with_history()`: Shows how to maintain conversation history across multiple queries
   * `agent_with_struct_output()`: Demonstrates returning structured data from an agent
   * `agent_with_tools()`: Shows how to use tools with agents
   * `HandOffData`: A data structure for agent handoff information
   * A `main()` function that demonstrates different agent capabilities with example queries
