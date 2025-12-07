import os
import getpass
import asyncio
import nest_asyncio
from typing import List
from dotenv import load_dotenv
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool as langchain_tool

# Load environment variables
load_dotenv()

try:
    # A model with function/tool calling capabilities is required.
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
    print(f"Language model initialized: {llm.model}")
except Exception as e:
    print(f"Error initializing language model: {e}")
    llm = None

@langchain_tool
def search_information(query: str) -> str:
    """
    Provides factual information on a given topic. Use this tool
    to find answers to phrases like 'capital of France' or 'weather in London?'.
    """
    print(f"\n--- Tool Called: search_information with query: '{query}' ---")
    # Simulate a search tool with a dictionary of predefined results.
    simulated_results = {
        "weather in london": "The weather in London is currently cloudy with a temperature of 15°C.",
        "capital of france": "The capital of France is Paris.",
        "population of earth": "The estimated population of Earth is around 8 billion people.",
        "tallest mountain": "Mount Everest is the tallest mountain above sea level.",
        "default": f"Simulated search result for '{query}': No specific information found, but the topic seems interesting."
    }
    result = simulated_results.get(query.lower(), simulated_results["default"])
    print(f"--- TOOL RESULT: {result} ---")
    return result

tools = [search_information]

# --- Create a Tool-Calling Agent ---
if llm:
    # This prompt template requires an `agent_scratchpad` placeholder for the agent's internal steps.
    agent_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    # Bind tools to model
    llm_with_tools = llm.bind_tools(tools)

async def run_agent_with_tool(query: str):
    """Invokes the agent executor with a query and prints the final response."""
    print(f"\n--- Running Agent with Query: '{query}' ---")
    try:
        response = await llm_with_tools.ainvoke(query)
        if response.tool_calls:
            for tool_call in response.tool_calls:
                tool_result = search_information.invoke(tool_call["args"])
                print("\n--- Final Agent Response ---")
                print(tool_result)
        else:
            print("\n--- Final Agent Response ---")
            print(response.content)
    except Exception as e:
        print(f"\nAn error occurred during agent execution: {e}")

async def main():
    """Runs all agent queries concurrently."""
    tasks = [
        run_agent_with_tool("What is the capital of France?"),
        run_agent_with_tool("What's the weather like in London?"),
        run_agent_with_tool("Tell me something about dogs.")
    ]
    await asyncio.gather(*tasks)

nest_asyncio.apply()
asyncio.run(main())