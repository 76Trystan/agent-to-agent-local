# Agent-to-Agent (A2A) Communication System

A flexible multi-agent system using the openAI agent SDK, built with Python and Ollama LLaMA models that enables autonomous agents to collaborate on complex tasks through sequential and parallel workflows.

---

## Overview

This project implements an **Agent-to-Agent (A2A) communication framework** where multiple AI agents with specialized roles can work together to accomplish tasks. Agents can operate:

- **Sequentially** – Passing outputs as inputs to the next agent.  
- **In parallel** – Running multiple agents simultaneously and aggregating results.  

The system is designed to be modular, so new agents or tools can be easily added.

---

## Features

- Multi-agent orchestration with a **triage agent** directing tasks.  
- Integration with **Ollama LLaMA models** for high-quality AI reasoning.  
- Asynchronous execution using `asyncio`.  
- Easily extensible with new specialist agents or tools.  

---

## Installation

### Requirements

- Python 3.11 or higher 
- Llama3.1 or higher 
- [Ollama CLI](https://ollama.com/docs/) installed and configured  
- Virtual environment recommended 