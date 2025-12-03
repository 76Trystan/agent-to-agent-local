import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunContextWrapper, Handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

current_model = "llama3.1:8b"


# create an AsyncOpenAI client that points to Ollama and provides a dummy key
ollama_client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"   # OPenAI client requires an api_key even if Ollama does not
)


#---------------------------- specialist agents ----------------------------

math_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems, Explain your reasoning at each step and include examples.",
    model=OpenAIChatCompletionsModel(
        model=current_model,
        openai_client=ollama_client,
    ),
)

poet_agent = Agent(
    name="Poet",
    handoff_description="Specialist in writing shakespearean poems",
    instructions="You write shakespearean poems. based on the user's input, write in the style of shakespeare as if you were a poet from that era.",
    model=OpenAIChatCompletionsModel(
        model=current_model,
        openai_client=ollama_client,
    ),
)

#---------------------------- triage agent ----------------------------

triage_agent = Agent(
    name="Triage Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}"You determine which agent to use based on the user's prompt. and provide which choice you made.""",
    handoffs=[Handoff(agent=math_agent, condition="contains math"), Handoff(agent=poet_agent, condition="contains a word that you could write a poem about")],
    model=OpenAIChatCompletionsModel(
        model=current_model,
        openai_client=ollama_client,
    )
)
#---------------------------- main program ----------------------------

async def main():
    result = await Runner.run(triage_agent, "whats 5 plus 3?")
    print(result.final_output)


def on_handoff(_: RunContextWrapper[None]):
    print("Handoff called: ", Agent.name)

if __name__ == "__main__":
    asyncio.run(main())

