import agents.agent as agent



def ask_agent(query: str):
    result = agent.triage_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result['messages'][-1].content

if __name__ == "__main__":
    response = ask_agent("name 3 states in australia and give small summary about each")
    print(response)