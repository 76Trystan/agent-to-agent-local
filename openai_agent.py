import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel

# create an AsyncOpenAI client that points to Ollama and provides a dummy key
ollama_client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"   # OPenAI client requires an api_key even if Ollama does not
)

#---------------------------- specialist agents ----------------------------

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems, Explain your reasoning at each step and include examples.",
    model=OpenAIChatCompletionsModel(
        model="llama3:8b",
        openai_client=ollama_client,
    ),
)

poet_agent = Agent(
    name="Poet",
    handoff_description="Specialist in writing shakespearean poems",
    instructions="You write shakespearean poems. based on the user's input, write in the style of shakespeare as if you were a poet from that era.",
    model=OpenAIChatCompletionsModel(
        model="llama3:8b",
        openai_client=ollama_client,
    ),
)

#---------------------------- triage agent ----------------------------

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's prompt.",
    handoffs=[poet_agent, math_tutor_agent],
    model=OpenAIChatCompletionsModel(
        model="llama3:8b",
        openai_client=ollama_client,
    )
)

async def main():
    result = await Runner.run(poet_agent, "whats 6 times 7 plus 2?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

