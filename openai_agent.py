import asyncio
from agents import Agent
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel

math_tutor_agent = Agent(   
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",

    model=OpenAIChatCompletionsModel( 
        model="llama3:8b",
        openai_client=AsyncOpenAI(base_url="http://localhost:11434/v1"),
        api_key="ollama"
    ),
)
async def main():
    result = await Runner.run(math_tutor_agent, "whats 7 times 9")
    print(result.final_output)
if __name__ == "__main__":
    asyncio.run(main())
    
