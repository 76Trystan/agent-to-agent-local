import asyncio
import openai_agent
from agents import Runner
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

async def main():
    result = await Runner.run(openai_agent.triage_agent, "whats sydeney's weather like?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())