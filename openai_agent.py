import asyncio
import math
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunContextWrapper, Handoff, function_tool, ModelSettings
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from tools import TOOLS

current_model = "llama3.1:8b"


# create an AsyncOpenAI client that points to Ollama and provides a dummy key
ollama_client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"   # OPenAI client requires an api_key even if Ollama does not
)
def on_handoff(ctx: RunContextWrapper[None]):
    print("Handoff called")
    
@function_tool
def quadratic(a, b, c):
    sqrt = math.sqrt

    try:
        if a and b and c == 0:
            return {"success": False, "error": "Invalid coefficients"}
        result = (-b*(sqrt(b^2 - 4*a*c)))/(2*a)
        return {"success": True, "x = ": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


#---------------------------- specialist agents ----------------------------

math_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems, Explain your reasoning at each step and include examples.",
    tools=[quadratic],
    model_settings=ModelSettings(tool_choice="quadratic"),
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
    handoffs=[math_agent, poet_agent],
    model=OpenAIChatCompletionsModel(
        model=current_model,
        openai_client=ollama_client,
    )
)
#----------------------------- tools ----------------------------

# currently needs to be implemented

tools = [
    TOOLS["add"],
    TOOLS["subtract"],
    TOOLS["multiply"],
    TOOLS["divide"],
    TOOLS["quadratic"]
]

def quadratic(a, b, c):
    sqrt = math.sqrt

    try:
        if a and b and c == 0:
            return {"success": False, "error": "Invalid coefficients"}
        result = (-b*(sqrt(b^2 - 4*a*c)))/(2*a)
        return {"success": True, "x = ": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

#---------------------------- main program ----------------------------

async def main():
    result = await Runner.run(triage_agent, "solve the quadratic equation 2x^2 + 5x -3 = 0")
    print(result.final_output)


def on_handoff(_: RunContextWrapper[None]):
    print("Handoff called: ", Agent.name)

if __name__ == "__main__":
    asyncio.run(main())

