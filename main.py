from prompts_example import SCHOLAR_SYSTEM_PROMPT, FACT_CHECK_PROMPT, MAX_ITERATIONS
from client import query_llama
#from tools import TOOLS
import sys

def main():
    '''Program work flow: User -> Scholar -> Weather Agent (if needed) -> Fact Checker -> (Revise if needed) -> Output'''

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
    scholar_response = query_llama(SCHOLAR_SYSTEM_PROMPT, user_message, temperature=0.3)
    
    if scholar_response.startswith("ERROR"):
        print(f"Scholar Agent Error: {scholar_response}")
        return
    
    print(f"Scholar Agent's Answer:\n{scholar_response}\n")
    print("-" * 100 + "\n")


    # Step 2: Fact Checker validates Scholar's answer
    print("Fact Checker Agent is now validating Scholar's answer...\n")
    
    validation_request = f"""Original Question: {user_message}

Answer to Validate:
{scholar_response}

Please validate this answer for factual accuracy and completeness."""
    
    fact_check_feedback = query_llama(FACT_CHECK_PROMPT, validation_request, temperature=0.3)
    
    if fact_check_feedback.startswith("ERROR"):
        print(f"Fact Checker failed: {fact_check_feedback}")
        print(f"\nReturning Scholar's answer without validation.")
        print(f"\nFINAL ANSWER:\n{scholar_response}")
        return
    
    print(f"Fact Checker's Evaluation:\n{fact_check_feedback}\n")
    print("-" * 100 + "\n")

    # Step 3: Check if approved or needs revision
    if "APPROVED" in fact_check_feedback:
        # Answer is good - return it
        print("Answer has been approved by Fact Checker!\n")
        print("-" * 100)
        print("FINAL ANSWER")
        print("-" * 100)
        print(scholar_response)
    
    elif "REVISE" in fact_check_feedback or "REVISION" in fact_check_feedback:
        # Answer needs improvement - Scholar revises
        print("Revision Requested. Scholar is revising based on feedback...\n")
        
        revision_request = f"""Your previous answer to the question "{user_message}":
{scholar_response}

Fact Checker's feedback:
{fact_check_feedback} 

Please provide a revised answer that addresses all the concerns raised."""
        
        revised_response = query_llama(SCHOLAR_SYSTEM_PROMPT, revision_request, temperature=0.3)
        
        if revised_response.startswith("ERROR"):
            print(f"Revision failed: {revised_response}")
            print(f"\nReturning original answer.")
            print(f"\nFINAL ANSWER:\n{scholar_response}")
            return
        
        print(f"Scholar's Revised Answer:\n{revised_response}\n")
        print("-" * 100 + "\n")
        
        print("-" * 100)
        print("FINAL ANSWER (Revised)")
        print("-" * 100)
        print(revised_response)
    
    else:
        # Unclear validation result error, return original answer
        print("Unclear validation result. Returning Scholar's original answer.\n")
        print("-" * 100)
        print("FINAL ANSWER")
        print("-" * 100)
        print(scholar_response)


if __name__ == "__main__":
    main()