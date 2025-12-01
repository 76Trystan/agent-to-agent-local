import requests
import json

# Configuration for the local Ollama Llama 3 API
LLAMA3_API_URL="http://localhost:11434"

def generate_llama3_response(prompt, model_name="llama3", stream=False):
        """
        Sends a prompt to the local Ollama Llama 3 model and returns the response.

        Args:
            prompt (str): The text prompt to send to the model.
            model_name (str): llmama3:8b
            stream (bool): If True, the response will be streamed in chunks.
                           If False, the full response will be returned at once.

        Returns:
            str: The generated response from Llama 3.
        """

        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": stream
        }

        try:
            response = requests.post(f"{LLAMA3_API_URL}/generate", json=payload, stream=stream)
            response.raise_for_status()

            if stream:
                full_response = ""
                for chunk in response.iter_lines():
                    if chunk:
                        decoded_chunk = chunk.decode('utf-8')
                        full_response += decoded_chunk
                        print(decoded_chunk, end='', flush=True)
                return full_response
            else:
                return response.json().get("text", "")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

            

