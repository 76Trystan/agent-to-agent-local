from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.agents import create_agent
import asyncio
import json
import httpx

current_model = "llama3.1:8b"

model = ChatOllama(
    model=current_model,      
    format="json",           
    temperature=0.3
)

# Global variables
mcp_tools = []
agent = None
session = None

#initialise MCP Connection
async def setup_mcp():
    global mcp_tools, agent, session
    
    try:
        # Connect to the FastMCP server via HTTP
        print("Connecting to FastMCP server...")
        
        # Get list of tools from the server
        async with httpx.AsyncClient() as client:
            response = await client.get("http://127.0.0.1:8000/mcp")
            tools_data = response.json() 
        
        tools_list = tools_data.get("tools", [])
        print(f"MCP Connected, Loaded {len(tools_list)} tools from MCP server:")
        
        # Create tool functions dynamically
        for tool_info in tools_list:
            tool_name = tool_info.get("name", "unknown")
            tool_desc = tool_info.get("description", "")
            print(f"  - {tool_name}: {tool_desc}")
            
            # Create a closure to capture the tool name
            def create_tool_func(tname, tdesc):
                def tool_func(**kwargs):
                    """Call MCP tool"""
                    try:
                        print(f"[MCP TOOL USED] {tname} with args {kwargs}")
                        # Run async function from sync context
                        loop = asyncio.get_event_loop()
                        result = loop.run_until_complete(
                            call_mcp_tool(tname, kwargs)
                        )
                        return str(result)
                    except Exception as e:
                        return f"Error: {str(e)}"
                
                tool_func.__name__ = tname
                tool_func.__doc__ = tdesc
                return tool_func
            
            # Create the tool function
            func = create_tool_func(tool_name, tool_desc)
            
            # Wrap it with @tool decorator
            langchain_tool = tool(func)
            mcp_tools.append(langchain_tool)
        
        # Create agent with all MCP tools
        agent = create_agent(model, mcp_tools)
        
    except Exception as e:
        print(f"Could notconnect to MCP Server{e}")
        raise

# tool call function
async def call_mcp_tool(tool_name: str, args: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/call",
            json={"tool": tool_name, "args": args}
        )
        result = response.json()
        return result.get("result", "")

# agent ask query
def ask_agent(query: str):
    if agent is None:
        return "Agent not initialized"

    try:
        print(f"\nUser Prompt: {query}")

        result = agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })

        response = result["messages"][-1].content

        print(f"Response: {response}\n")
        return response

    except Exception as e:
        return f"Error: {e}"

# entry point with prompt
async def main(prompt: str = None):
    await setup_mcp()
    if prompt:
        return ask_agent(prompt)

if __name__ == "__main__":
    user_prompt = "whats 8 plus 5"  
    response = asyncio.run(main(user_prompt))
    print("Final response:", response)