# OpenAI Agents SDK: Quick Start Guide

## Introduction

OpenAI Agents SDK provides a streamlined framework for building and deploying AI agents that can think, reason, and interact with tools to solve complex tasks. Based on our current implementation, the SDK enables you to:

- Create agents with different configuration approaches, including direct OpenAI client usage, global settings, or custom model providers
- Implement specialized agents for various use cases, from basic query responses to complex multi-agent systems
- Maintain conversation context and history across interactions
- Generate structured outputs for consistent data handling
- Integrate tools that extend agent capabilities
- Configure agents with custom instructions and model parameters
- Handle agent handoffs between specialized services

The SDK simplifies working with OpenAI's underlying APIs by providing intuitive interfaces through the `Runner.run()` method, standardized configuration patterns, and easy-to-implement agent templates as demonstrated in our examples directory.

Whether you're building travel planning assistants, query routing systems, or specialized tools that require structured outputs, this SDK provides the foundation for creating reliable, adaptable AI applications tailored to your specific requirements.

## Installation

1.  **Clone:** `git clone <repository_url>`
2.  **Navigate:** `cd <openai_agent_directory>`
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

2. [`example_agents.py`](./_examples/example_agents.py): Showcases various agent implementations including:
   * `basic_agent()`: A simple agent implementation that responds to user queries
   * `agent_with_handoffs()`: Demonstrates agent triage system that can route queries to specialized agents
   * `agent_with_history()`: Shows how to maintain conversation history across multiple queries
   * `agent_with_struct_output()`: Demonstrates returning structured data from an agent
   * `agent_with_tools()`: Shows how to use tools with agents
   * `HandOffData`: A data structure for agent handoff information
   * A `main()` function that demonstrates different agent capabilities with example queries

3. 