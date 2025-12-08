import client
from agents import Agent, OpenAIChatCompletionsModel, RunContextWrapper, Runner, HostedMCPTool, function_tool, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

#change based on current model available in ollama
current_model = "llama3.1:8b"


#---------------------------- handoff call ----------------------------

def create_handoff_callback(agent_name):
    def callback(context: RunContextWrapper[None]):
        print(f"Handoff called. Agent Used: {agent_name}")
    return callback


#---------------------------- specialist agents ----------------------------

math_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems, using the tools provided, solve the mathematics question",
    tools=[
            HostedMCPTool(
                tool_config={
                    "type": "mcp",
                    "server_label": "Server 1",
                    "server_url": "http://0.0.0.0:8000/mcp",
                    "require_approval": "never",
                }
            )
        ],
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

