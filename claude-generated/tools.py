import math
import re

sqrt = math.sqrt

#functions

#addition function
def add(a: int, b: int):
    try:
        result = int(a) + int(b)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

#subtract function
def subtract(a: int, b: int):
    try:
        result = int(a) - int(b)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
#multiplication function
def multiply(a, b):
    try:
        result = float(a) * float(b)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

#division function
def divide(a, b):
    try:
        if float(b) == 0:
            return {"success": False, "error": "Division by zero"}
        result = float(a) / float(b)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
    #quadratic function
def quadratic(a, b, c):
    try:
        if a and b and c == 0:
            return {"success": False, "error": "Invalid coefficients"}
        result = (-b*(sqrt(b^2 - 4*a*c)))/(2*a)
        return {"success": True, "x = ": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


# registry of tools

TOOLS = {
    "add": {
        "function": add,
        "description": "Add two numbers together",
        "example": "add(5, 3)"
    },
    "subtract": {
        "function": subtract,
        "description": "Add two numbers together",
        "example": "subtract(5, 3)"
    },
    "multiply": {
        "function": multiply,
        "description": "Multiply two numbers together",
        "example": "multiply(4, 5)"
    },
    "divide": {
        "function": divide,
        "description": "Divide first number by second",
        "example": "divide(10, 2)"
    },
    "quadratic": {
        "function": quadratic,
        "description": "solve the quadratic equation for given coefficients a, b, and c",
        "example": "quadratic(2, 5, -3)"
    }   
}


def get_tool_function(tool_name):
    """Get a tool's function by name"""
    if tool_name in TOOLS:
        return TOOLS[tool_name]["function"]
    return None


def get_tools_list():
    """Get description of available tools"""
    output = "AVAILABLE TOOLS:\n"
    for name, info in TOOLS.items():
        output += f"  • {name}: {info['description']}\n"
        output += f"    Example: {info['example']}\n"
    return output


#execution function

def execute_agent_tools(agent_response):
    """
    Execute tools called by agent.
    Works with Swarm framework.
    """
    # Look for TOOL_CALL: function_name(args)
    pattern = r'TOOL_CALL:\s*(\w+)\((.*?)\)'
    matches = re.findall(pattern, agent_response)
    
    if not matches:
        return agent_response
    
    output = agent_response + "\n\n--- Tool Results ---\n"
    
    for tool_name, args_string in matches:
        tool_func = get_tool_function(tool_name)
        
        if not tool_func:
            output += f"\n{tool_name}: Tool not found\n"
            continue
        
        args = [arg.strip() for arg in args_string.split(',')]
        result = tool_func(*args)
        
        if result["success"]:
            output += f"\n{tool_name}({args_string}): {result['result']}\n"
        else:
            output += f"\n{tool_name}({args_string}): Error - {result['error']}\n"
    
    return output