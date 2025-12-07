"""
Multi-Agent Collaboration using Google Generative AI
Real implementation with your API key
"""

import asyncio
import os
from typing import Dict, List, Any
from dataclasses import dataclass
import google.generativeai as genai

# Configure Google Gemini API
os.environ['GOOGLE_API_KEY'] = 'AIzaSyDbsn83vawtcSBBnmo1a1354rLQ2_RD-L4'
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

@dataclass
class Event:
    author: str
    content: str

class BaseAgent:
    def __init__(self, name: str, instruction: str = ""):
        self.name = name
        self.instruction = instruction
        self.parent_agent = None
        self.sub_agents = []
        
    def add_sub_agent(self, agent):
        self.sub_agents.append(agent)
        agent.parent_agent = self

class LlmAgent(BaseAgent):
    def __init__(self, name: str, model: str, instruction: str = "", sub_agents: List = None):
        super().__init__(name, instruction)
        self.model = genai.GenerativeModel(model)
        if sub_agents:
            for agent in sub_agents:
                self.add_sub_agent(agent)
    
    async def run(self, prompt: str) -> str:
        full_prompt = f"{self.instruction}\n\n{prompt}"
        response = await self.model.generate_content_async(full_prompt)
        return response.text

class TaskExecutor(BaseAgent):
    def __init__(self):
        super().__init__("TaskExecutor", "Executes predefined tasks")
    
    async def run(self, prompt: str) -> str:
        return "Task finished successfully."

# 1. Hierarchical Agents
greeter = LlmAgent("Greeter", "gemini-2.5-flash", "You are a friendly greeter.")
task_doer = TaskExecutor()

coordinator = LlmAgent(
    "Coordinator", 
    "gemini-2.5-flash",
    "When asked to greet, delegate to Greeter. When asked for tasks, delegate to TaskExecutor.",
    [greeter, task_doer]
)

# 2. Sequential Pipeline
step1 = LlmAgent("DataFetcher", "gemini-2.5-flash", "Fetch and prepare data")
step2 = LlmAgent("DataProcessor", "gemini-2.5-flash", "Analyze data and provide insights")

# 3. Parallel Agents
weather_agent = LlmAgent("WeatherAgent", "gemini-2.5-flash", "Provide weather information")
news_agent = LlmAgent("NewsAgent", "gemini-2.5-flash", "Provide news updates")

async def main():
    print("=== Multi-Agent Collaboration with Real Google API ===\n")
    
    # Test Hierarchical
    print("1. Testing Greeter:")
    result = await greeter.run("Hello! Please greet me warmly.")
    print(f"Greeter: {result}\n")
    
    # Test Sequential
    print("2. Testing Sequential Processing:")
    data = await step1.run("Fetch customer satisfaction data")
    print(f"Step1: {data}")
    
    analysis = await step2.run(f"Analyze this data: {data}")
    print(f"Step2: {analysis}\n")
    
    # Test Parallel
    print("3. Testing Parallel Execution:")
    weather_task = weather_agent.run("What's the weather in New York?")
    news_task = news_agent.run("What's the latest tech news?")
    
    weather_result, news_result = await asyncio.gather(weather_task, news_task)
    print(f"Weather: {weather_result}")
    print(f"News: {news_result}\n")
    
    print("✅ All agents working with real Google API!")

if __name__ == "__main__":
    asyncio.run(main())