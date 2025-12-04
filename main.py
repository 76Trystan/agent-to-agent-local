import asyncio
import openai_agent
from agents import Agent, Runner, RunContextWrapper
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

async def main():
    result = await Runner.run(openai_agent.triage_agent, "solve the quadratic equation 2x^2 + 5x -3 = 0")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())