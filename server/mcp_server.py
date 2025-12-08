from fastmcp import FastMCP

mcp = FastMCP("Server 1")

#Tool
@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    return a + b

#Resource
@mcp.resource("data://status") # gets current server status
def get_status() -> str:
        return "Server is running and ready to accept requests"


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)