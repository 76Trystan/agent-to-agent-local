import client
import asyncio
from agents import Agent, RunContextWrapper, Runner, HostedMCPTool, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.models.ollama import OllamaChatAPIModel

# ---------------------------- model config ----------------------------

current_model = "llama3.1:8b"  # Ollama model

# ---------------------------- handoff callback ----------------------------

def create_handoff_callback(agent_name):
    def callback(context: RunContextWrapper[None]):
        print(f"Handoff called. Agent Used: {agent_name}")
    return callback

# ---------------------------- MCP tools ----------------------------

math_mcp_tool = HostedMCPTool(
    tool_config={
        "type": "mcp",
        "server_label": "Server 1",
        "server_url": "http://0.0.0.0:8000/mcp",
        "require_approval": "never",
    }
)

# ---------------------------- specialist agents ----------------------------

math_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems using the tools provided.",
    tools=[math_mcp_tool],
    model=OllamaChatAPIModel(
        model=current_model,
        client=client.ollama_client,
    ),
)

poet_agent = Agent(
    name="Poet",
    handoff_description="Specialist in writing Shakespearean poems",
    instructions="You write Shakespearean poems in the style of the era, based on user input.",
    model=OllamaChatAPIModel(
        model=current_model,
        client=client.ollama_client,
    ),
)

weather_agent = Agent(
    name="Weather Expert",
    handoff_description="Specialist in collecting and presenting weather information",
    instructions="Provide accurate and up-to-date weather information using available tools.",
    model=OllamaChatAPIModel(
        model=current_model,
        client=client.ollama_client,
    ),
)

# ---------------------------- triage agent ----------------------------

triage_agent = Agent(
    name="Triage Agent",
    instructions=f"{RECOMMENDED_PROMPT_PREFIX} Decide which agent to use based on the user's prompt, and indicate your choice.",
    handoffs=[
        handoff(math_agent, on_handoff=create_handoff_callback("Math Tutor")),
        handoff(poet_agent, on_handoff=create_handoff_callback("Poet")),
        handoff(weather_agent, on_handoff=create_handoff_callback("Weather Expert")),
    ],
    model=OllamaChatAPIModel(
        model=current_model,
        client=client.ollama_client,
    ),
)

# ---------------------------- runner ----------------------------

async def main():
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        result = await Runner.run(triage_agent, user_input)
        print("Agent:", result)

if __name__ == "__main__":
    asyncio.run(main())
