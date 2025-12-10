from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

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

    # Get available tools
    tools = await client.get_tools()
    
    print("Available tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")


if __name__ == "__main__":
    asyncio.run(main())