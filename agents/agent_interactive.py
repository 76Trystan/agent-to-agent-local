from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
import asyncio
import json

current_model = "llama3.1:8b"

model = ChatOllama(
    model=current_model,      
    format="json",           
    temperature=0.3
)

async def run_agent(agent, query, tools_dict):
    messages = [HumanMessage(content=query)]
    
    while True:
        # Get agent response
        response = await agent.ainvoke({"messages": messages})
        
        # Check if response contains tool use
        if isinstance(response, dict) and "messages" in response:
            messages = response["messages"]
            last_message = messages[-1]
            
            # Check if this is a tool call
            if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                tool_call = last_message.tool_calls[0]
                tool_name = tool_call['name']
                tool_input = tool_call['args']
                
                print(f"Using tool: {tool_name}")
                print(f"Input: {tool_input}")
                
                # Execute the tool
                if tool_name in tools_dict:
                    tool = tools_dict[tool_name]
                    result = await tool.ainvoke(tool_input)
                    print(f"Result: {result}\n")
                    
                    # Add tool result to messages
                    from langchain_core.messages import ToolMessage
                    messages.append(ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call['id']
                    ))
                else:
                    print(f"Tool {tool_name} not found")
                    break
            else:
                # No more tool calls, return final response
                return str(last_message.content)
        else:
            return str(response)

async def main():
    # Initialize MCP client
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "streamable_http",
                "url": "http://127.0.0.1:8000/mcp",
            }
        }
    )

    # Get available tools from MCP server
    mcp_tools = await client.get_tools()
    
    print("Available tools:")
    tools_dict = {}
    for tool in mcp_tools:
        print(f"  - {tool.name}: {tool.description}")
        tools_dict[tool.name] = tool
    
    # Create the agent
    agent = create_agent(model, mcp_tools)

    print("\n")
    print("Running Math Agent...")
    #print("-"*100 + "\n")
    
    # Interactive mode (optional)
    print("\n" + "-"*50)
    print("Interactive Mode (type 'quit' to exit)")
    print("-"*50 + "\n")
    
    while True:
        user_input = input("Enter a math question: ").strip()
        if user_input.lower() == 'quit':
            break
        
        try:
            result = await run_agent(agent, user_input, tools_dict)
            print(f"Final Result: {result}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())