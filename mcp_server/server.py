from fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print(f"[SERVER] add called with {a} + {b}")
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print(f"[SERVER] multiply called with {a} * {b}")
    return a * b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print(f"[SERVER] subtract called with {a} - {b}")
    return a - b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide two numbers"""
    print(f"[SERVER] divide called with {a} / {b}")
    if b == 0:
        return "Error: Cannot divide by zero"
    return a / b



if __name__ == "__main__":
    print("Starting FastMCP Math Server...")
    mcp.run(transport="streamable-http")