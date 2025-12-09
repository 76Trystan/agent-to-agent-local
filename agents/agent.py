from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.agents import create_agent
import json

current_model = "llama3.1:8b"

model = ChatOllama(
    model=current_model,      
    format="json",           
    temperature=0.3
)

math_tools = []
math_agent = create_agent(model, math_tools)

weather_tools = []
weather_agent = create_agent(model, weather_tools)

# triage agent

@tool
def route_to_math_agent(query: str) -> str:
    """Route a math-related query to the math specialist agent."""
    result = math_agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return result['messages'][-1].content

@tool
def route_to_weather_agent(query: str) -> str:
    """Route a weather-related query to the weather specialist agent."""
    result = weather_agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return result['messages'][-1].content

triage_tools = [route_to_math_agent, route_to_weather_agent]
triage_agent = create_agent(model, triage_tools)

def ask_agent(query: str):
    result = triage_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result['messages'][-1].content

if __name__ == "__main__":
    response = ask_agent("Use the add_numbers tool to add 10 and 32 and give reasoning as to why you chose that agent")
    print(response)