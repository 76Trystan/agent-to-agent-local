from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Server 1")

@mcp.tool()
def add(a: int, b: int) -> int:
    print(f"[SERVER] add called with {a} + {b}")
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    print(f"[SERVER] multiply called with {a} * {b}")
    return a * b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    print(f"[SERVER] subtract called with {a} - {b}")
    return a - b

@mcp.tool()
def divide(a: float, b: float) -> float:
    print(f"[SERVER] divide called with {a} / {b}")
    if b == 0:
        return 0 # returns zero if cannot calculate
    return a / b



if __name__ == "__main__":
    print("Starting FastMCP Server...")
    mcp.run(transport="streamable-http")