import requests
import json

# Ollama API endpoint (runs locally)
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:8b"


def query_llama(system_prompt, user_message, temperature=0.4):
      
    # Combines system prompt and user message
    full_prompt = f"{system_prompt}\n\nUser: {user_message}\n\nAssistant:"
    
    # Prepare request payload
    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False, 
        "options": {
            "temperature": temperature,
            "num_predict": 2000  # Max tokens to generate
        }
    }
    
    try:
        # Send request to Ollama
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Get the raw response text for debugging
        raw_response = response.text  

        # Parse JSON response
        try:
            result = response.json()
        except json.JSONDecodeError as e:
            return f"ERROR: Invalid JSON response from Ollama. Check debug output above."
        
        # grabbing the generated text
        if "response" in result:
            generated_text = result["response"].strip() # strips whitespace
            return generated_text
        else:
            return f"ERROR: 'response' key not found in Ollama output. Keys: {list(result.keys())}"
        
    #Error handling
    except requests.exceptions.Timeout: # error handling for timeout
        return "ERROR: Request timed out. Llama took too long to respond."
    
    except requests.exceptions.ConnectionError: # error handling for connection issues
        return "ERROR: Cannot connect to Ollama. Is it running? Try: ollama serve"
    
    except requests.exceptions.HTTPError as e: # error handling for HTTP errors
        return f"ERROR: HTTP error from Ollama: {e}"
    
    except Exception as e: # general error handling
        return f"ERROR: Unexpected error: {type(e).__name__}: {str(e)}"

