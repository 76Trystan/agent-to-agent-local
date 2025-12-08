from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, Tool
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
import json

current_model = "llama3.1:8b"

model = ChatOllama(
    model=current_model,      
    format="json",           
    temperature=0.1
)