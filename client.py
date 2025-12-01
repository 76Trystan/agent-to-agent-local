import requests
import json

# Define the Ollama API endpoint for generating responses

OLLAMA_API_URL = "http://localhost:11434/api/generate" #Ollama's default local server URL
MODEL_NAME = "llama3:8b"  # change model if needed (not using llama3:70b as it will crash my computer)

def generate_llama3_response(prompt, model="llama3", stream=False):

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }

    try:
        if stream:
            response = requests.post(OLLAMA_API_URL, json=payload, stream=True)
            response.raise_for_status() # Raise an exception for bad status codes

            full_response = ""
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    try:
                        json_data = json.loads(decoded_line)
                        if "response" in json_data:
                            full_response += json_data["response"]
                            print(json_data["response"], end="", flush=True) # Print incrementally
                    except json.JSONDecodeError:
                        print(f"Could not decode JSON from line: {decoded_line}")
            return full_response
        else:
            response = requests.post(OLLAMA_API_URL, json=payload)
            response.raise_for_status()
            return response.json()["response"]

    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to Ollama server."
    except requests.exceptions.RequestException as e:
        return f"Error during API request: {e}"

if __name__ == "__main__":
    user_prompt = "Name 5 countries"

    print(f"Sending prompt to Llama 3: '{user_prompt}'")

    # Stream the response in chunks
    print("\nStreaming Response")
    response_streamed = generate_llama3_response(user_prompt, stream=True) 
    print("\n(Stream complete)")