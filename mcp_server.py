
#MCP Server for HTTP/SSE (Server-Sent Events)
#runs on localhost:8000 and can be tested with a browser


from fastmcp import FastMCP


# Initialize server
mcp = FastMCP("Local a2a Server")

# Define tools
@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def get_greeting(name: str) -> str:
    return f"Hello, {name}! Welcome to the A2A system."

# Define resources
@mcp.resource("config://settings") # gets server config settings
def get_settings() -> str:
    return """Server Configuration:
- Name: My A2A Server
- Version: 1.0.0
- Environment: Development
- Port: 8000"""

@mcp.resource("data://status") # gets current server status
def get_status() -> str:

    return "Server is running and ready to accept requests"

# Run the server
if __name__ == "__main__":
    import sys
    import logging
    
    # Suppress startup messages for stdio mode
    if '--stdio' in sys.argv:
        logging.basicConfig(level=logging.ERROR)
        mcp.run(transport="stdio")
    else:
        # HTTP starting up messages
        print("-" * 60)
        print("Starting up MCP Server...")
        print("-" * 60)
        print("\nServer URL: http://localhost:8000")
        print("\nAvailable Tools:")
        print("  - add_numbers(a, b)")
        print("  - get_greeting(name)")
        print("  - process_data(data, operation)")
        print("\nPress Ctrl+C to stop")
        print("-" * 60)
        mcp.run(transport="http", host="127.0.0.1", port= 8000)