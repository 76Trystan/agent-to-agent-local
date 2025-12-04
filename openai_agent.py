import client
from agents import Agent, OpenAIChatCompletionsModel, RunContextWrapper, Handoff, function_tool, ModelSettings
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

#change based on current model available in ollama
current_model = "llama3.1:8b"

#---------------------------- handoff call ----------------------------

def on_handoff(_: RunContextWrapper[None]):
    print("Handoff called: ", Agent.name)

#---------------------------- specialist agents ----------------------------

math_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems, Explain your reasoning at each step and include examples.",
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

#---------------------------- triage agent ----------------------------

triage_agent = Agent(
    name="Triage Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}"You determine which agent to use based on the user's prompt. and provide which choice you made.""",
    handoffs=[math_agent, poet_agent],
    model=OpenAIChatCompletionsModel(
        model=current_model,
        openai_client=client.ollama_client,
    )
)
