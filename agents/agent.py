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

async def setup_mcp():
    """Initialize MCP connection and get tools from the FastMCP server."""
    global mcp_tools, agent, session
    
    try:
        # Connect to the FastMCP server via HTTP
        print("Connecting to FastMCP server...")
        
        # Get list of tools from the server
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/tools")
            tools_data = response.json()
        
        tools_list = tools_data.get("tools", [])
        print(f"✓ Connected! Loaded {len(tools_list)} tools from MCP server:")
        
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
        print(f"✗ Error connecting to MCP server: {e}")
        print("Make sure your FastMCP server is running with: python server.py")
        raise

async def call_mcp_tool(tool_name: str, args: dict):
    """Call a tool on the MCP server."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/call",
            json={"tool": tool_name, "args": args}
        )
        result = response.json()
        return result.get("result", "")

def ask_agent(query: str):
    """Ask the agent a question."""
    if agent is None:
        return "Agent not initialized"
    try:
        print(f"\n[QUERY] {query}")
        result = agent.invoke({"messages": [{"role": "user", "content": query}]})
        response = result['messages'][-1].content
        print(f"[RESPONSE] {response}\n")
        return response
    except Exception as e:
        return f"Error: {str(e)}"

async def main():
    """Main function to initialize and run the agent system."""
    await setup_mcp()
    
    print("\n" + "=" * 70)
    print("AGENT SYSTEM WITH FASTMCP")
    print("=" * 70)
    
    ask_agent("Add 10 and 32")
    ask_agent("Multiply 5 by 8")
    ask_agent("Subtract 20 from 100")

if __name__ == "__main__":
    asyncio.run(main())