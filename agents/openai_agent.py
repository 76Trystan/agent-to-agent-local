import client
from agents import Agent, OpenAIChatCompletionsModel, RunContextWrapper, function_tool, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
import mcp_client

#change based on current model available in ollama
current_model = "llama3.1:8b"

#---------------------------- handoff call ----------------------------

def create_handoff_callback(agent_name):
    def callback(context: RunContextWrapper[None]):
        print(f"Handoff called. Agent Used: {agent_name}")
    return callback

#---------------------------- MCP Tool Wrapper ----------------------------

#Define call functions from MCP client
mcp = mcp_client.mcp

@function_tool
def mcp_add(a: int, b: int) -> str:
    """Add two numbers using MCP server"""
    return mcp.call_tool("add_numbers", {"a": a, "b": b})

@function_tool
def mcp_multiply(a: int, b: int) -> str:
    """Multiply two numbers using MCP server"""
    return mcp.call_tool("multiply_numbers", {"a": a, "b": b})

@function_tool
def mcp_read_status() -> str:
    """Check MCP server status"""
    return mcp.read_resource("data://status")

#---------------------------- specialist agents ----------------------------

math_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems, Explain your reasoning at each step and include examples.",
    tools=[mcp_add, mcp_multiply],
    model=OpenAIChatCompletionsModel(
        model=current_model,
        openai_client=client.ollama_client,
    ),
)

poet_agent = Agent(
    name="Poet",
    handoff_description="Specialist in writing shakespearean poems",
    instructions="You write shakespearean poems. based on the user's input, write in the style of shakespeare as if you were a poet from that era.",
    model=OpenAIChatCompletionsModel(
        model=current_model,
        openai_client=client.ollama_client,
    ),
)

weather_agent = Agent(
    name="Weather Expert",
    handoff_description="Specialist in collecdting weather information and presenting it to users",
    instructions="You provide accurate and up-to-date weather information for any city requested by the user. Use the available tools to fetch the latest weather data and present it clearly.",
    model=OpenAIChatCompletionsModel(
        model=current_model,
        openai_client=client.ollama_client,
    ),
)

#---------------------------- triage agent ----------------------------

triage_agent = Agent(
    name="Triage Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}"You determine which agent to use based on the user's prompt. and provide which choice you made.""",
    handoffs=[
    handoff(math_agent, on_handoff=create_handoff_callback("Math Tutor")),
    handoff(poet_agent, on_handoff=create_handoff_callback("Poet")),
    handoff(weather_agent, on_handoff=create_handoff_callback("Weather Expert")),
    ],
    model=OpenAIChatCompletionsModel(
        model=current_model,
        openai_client=client.ollama_client,
    )
)

def check_mcp_connection() -> bool:
    """Check if MCP server is accessible"""
    try:
        status = mcp.read_resource("data://status")
        return "Error" not in status
    except Exception as e:
        print(f"Warning: Cannot connect to MCP server: {e}")
        print("   Make sure to start: python server/mcp_server.py")
        return False


# Check connection on module load
if __name__ != "__main__":
    if check_mcp_connection():
        print("MCP server connected")
    else:
        print("MCP server not available (agents will work but tools may fail)")
