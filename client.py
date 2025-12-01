import requests
import json

# Define the Ollama API endpoint for generating responses

OLLAMA_API_URL = "http://localhost:11434/api/generate" #Ollama's default local server URL
MODEL_NAME = "llama3:8b"  # change model if needed (not using llama3:70b as it will crash my computer)

def query_llama(system_prompt, user_message, temperature=0.35):

    prompt = f"{system_prompt}\n\nUser: {user_message}\n\nAssistant:"

    payload = {
        "model": MODEL_NAME,
        "prompt": user_message,
        "stream": True,
        "options": {
            "temperature": temperature,
            "num_predict": 2000
        }
    }

    try:
        # Sending request to Ollama API
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120, stream=True)
        response.raise_for_status()

        # Parse response
        result = response.json()
        return result["response"].strip()
    
    except requests.exceptions.Timeout:
        return "ERROR: Request timed out. Llama took too long to respond."
    except requests.exceptions.ConnectionError:
        return "ERROR: Cannot connect to Ollama. Is it running? (ollama serve)"
    
    except Exception as e:
        return f"ERROR: {str(e)}"




'''
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Query Llama 3 via Ollama")
    parser.add_argument("-p", "--prompt", help="Prompt text", default=None)
    args = parser.parse_args()
    
    user_prompt = args.prompt or input("Enter your prompt: ")
    print(f"Sending prompt to Llama 3: '{user_prompt}'")
    
    response = query_llama("", user_prompt)
    print("\nResponse:")
    print(response)
    '''