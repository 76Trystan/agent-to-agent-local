import asyncio
from fastmcp import Client, FastMCP

# In-memory server (ideal for testing)
server = FastMCP("Server 1")
client = Client(server)

# HTTP server
client = Client("http://0.0.0.0:8000/mcp")

async def main():
    async with client:
        # Basic server interaction
        await client.ping()
        
        # List available operations
        tools = await client.list_tools()
        print(tools)
        #resources = await client.list_resources()
        #print(resources)
        #prompts = await client.list_prompts()
        #print(prompts)

        
        # Execute operations
        #result = await client.call_tool("add_numbers", {"a": 5, "b": 4})
        #print(result.data)

asyncio.run(main())