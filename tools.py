import json
import requests
import os

# tool functions 

def add(a: int, b: int):
    return {"result ": a + b}



# tool profiles

TOOLS = {
    "add"
    "description": "Adds two numbers together.",
    "parameters": {
        "a": "int",
        "b": "int"
    }}