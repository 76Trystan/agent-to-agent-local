from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.agents import create_agent
import agent

model = agent.model

# triage agent

@tool
def route_to_math_agent(query: str) -> str:
    """Route a math-related query to the math specialist agent."""
    result = agent.math_agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return result['messages'][-1].content

@tool
def route_to_weather_agent(query: str) -> str:
    """Route a weather-related query to the weather specialist agent."""
    result = agent.weather_agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return result['messages'][-1].content

triage_tools = [route_to_math_agent, route_to_weather_agent]
triage_agent = create_agent(model, triage_tools)