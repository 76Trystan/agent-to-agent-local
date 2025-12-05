from agents import AsyncOpenAI


current_model = "llama3.1:8b"

# create an AsyncOpenAI client that points to Ollama and provides a dummy key
ollama_client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"   # OpenAI client requires an api_key even if Ollama does not
)


