from langchain.chat_models import init_chat_model
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain import hub

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rich import print
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Create a web search tool with TavilySearchResults
# This tool allows our agent to search the web for information
search = TavilySearchResults(max_results=2)
# # Uncomment to test search tool individually:
# tool_res = search.invoke("what is the current GDP of India?")
# print(tool_res)

# Create a retriever tool using FAISS vector store and Google's embeddings
# First load and process documents from LangSmith docs
loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
docs = loader.load()
# Split documents into manageable chunks
documents = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200
).split_documents(docs)
# Create vector store using Google's embeddings
vector = FAISS.from_documents(documents, GoogleGenerativeAIEmbeddings(model="models/text-embedding-004"))
retriever = vector.as_retriever()

# # Uncomment to test retriever individually:
# ret_res = retriever.invoke("how can langsmith help with testing?")
# print(ret_res)

# Create a retriever tool with a specific description to help the agent know when to use it
retriever_tool = create_retriever_tool(
    retriever,
    "langsmith_search",
    "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
)

# Combine both tools into a list for the agent to use
tools = [search, retriever_tool]

# Initialize the Ollama chat model with Qwen 2.5 (14B parameter version)
llm = init_chat_model(model="ollama:qwen2.5:14b")
# Bind tools to the LLM so it knows what tools are available
llm_with_tools = llm.bind_tools(tools)

# # Uncomment to test the LLM with tools directly:
# response = llm_with_tools.invoke([HumanMessage(content="What's the weather in france?")])
# print(f"ContentString: {response.content}")
# print(f"ToolCalls: {response.tool_calls}")

# Get the OpenAI functions agent prompt from LangChain Hub
prompt = hub.pull("hwchase17/openai-functions-agent")
# # Uncomment to see the prompt template:
# print(prompt.messages)

# Create the agent with the LLM, tools, and prompt
agent = create_tool_calling_agent(llm, tools, prompt)
# Create an agent executor that handles the interaction between the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True) # verbose=True shows debugging info

# # Uncomment to test the agent without using chat history/memory:
# response = agent_executor.invoke({"input": "how can langsmith help with testing?"})
# response = agent_executor.invoke({"input": "What's the weather in France?"})

# Run the agent with chat history to test memory/context retention
response = agent_executor.invoke(
    {
        "chat_history": [
            HumanMessage(content="hi! my name is Trap and I live in San Jose."),
            AIMessage(content="Hello Trap! How can I assist you today?"),
        ],
        "input": "Which state does my city reside in?",
    }
)

# Display the final response
print(response)