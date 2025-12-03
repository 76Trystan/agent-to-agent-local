"""
Main file using Swarm framework pattern.
Demonstrates agent handoffs and tool use.
"""

from agents import Agent, Swarm, Response
from archived.client import query_llama
import sys


def main():
    print("=" * 60)
    print("SWARM-STYLE AGENT SYSTEM")
    print("=" * 60)
    print()
    
    
    # Create Scholar Agent
    scholar = Agent(
        name="Scholar",
        instructions="""You are Scholar, a thorough research assistant.

Your role:
- Answer questions comprehensively and accurately
- Use available functions when calculations are needed
- If you finish your research, hand off to FactChecker for validation

When you're done with your analysis, write:
HANDOFF: FactChecker
""",
        functions=["add", "multiply", "divide"]
    )
    
    # Create Fact Checker Agent
    fact_checker = Agent(
        name="FactChecker",
        instructions="""You are FactChecker, a validation specialist.

Your role:
- Review the Scholar's work for accuracy
- Check if calculations are correct
- Verify logic and reasoning

Respond with either:
- APPROVED: [explanation] if everything is correct
- REVISION NEEDED: [specific issues] if there are problems

If revision is needed, write:
HANDOFF: Scholar
""",
        functions=[]
    )
    
    # Create Swarm and register agents
    swarm = Swarm()
    swarm.register_agent(scholar)
    swarm.register_agent(fact_checker)
    
    # Get user input
    print("Ask a question (or 'quit' to exit):")
    user_question = input("> ").strip()
    
    if user_question.lower() in ['quit', 'exit', 'q']:
        print("Goodbye!")
        return
    
    if not user_question:
        print("No question provided.")
        return
    
    print("\n" + "=" * 60)
    print("PROCESSING WITH SWARM")
    print("=" * 60 + "\n")
    
    # Run the swarm starting with Scholar
    print(f"Starting with {scholar.name}...\n")
    
    response = swarm.run(
        agent=scholar,
        query=user_question,
        llama_client=query_llama
    )
    
    # Display results
    print("\n" + "=" * 60)
    print("CONVERSATION FLOW")
    print("=" * 60)
    
    for i, message in enumerate(response.messages, 1):
        print(f"\n[Message {i}]")
        print(message)
        print("-" * 60)
    
    print("\n" + "=" * 60)
    print(f"FINAL AGENT: {response.agent.name}")
    print("=" * 60)


if __name__ == "__main__":
    main()