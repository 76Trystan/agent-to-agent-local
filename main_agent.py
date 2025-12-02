from agent import Agents
from client import query_llama
from tools import TOOLS
import sys

def main():
    '''Program work flow: User -> Scholar -> Math tools (if needed) -> Output'''

    print("-" * 100)
    print("Starting Agent-to-Agent Local System")
    print("-" * 100)
    print("\nAsk your question here or type 'quit' to exit.")
    
    user_message = input("> ").strip()

    if user_message.lower() in ['quit', 'exit', 'q']:
        print("Exiting A2A Program...")
        return
    
    if not user_message:
        print("Please enter a valid prompt.")
        return
    
    print("\n" + "-" * 100)
    print("Processing...")
    print("-" * 100 + "\n")

    # First step -> Scholar Agent researches the question
    print("Scholar Agent is researching your question...\n")
    scholar_response = query_llama(Agents, user_message, temperature=0.3)
    
    if scholar_response.startswith("ERROR"):
        print(f"Scholar Agent Error: {scholar_response}")
        return
    
    print(f"Scholar Agent's Answer:\n{scholar_response}\n")
    print("-" * 100 + "\n")




if __name__ == "__main__":
    main()