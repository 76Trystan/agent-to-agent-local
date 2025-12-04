import math


# ---------------------------- Functions ----------------------------

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
    sqrt = math.sqrt

    try:
        if a and b and c == 0:
            return {"success": False, "error": "Invalid coefficients"}
        result = (-b*(sqrt(b^2 - 4*a*c)))/(2*a)
        return {"success": True, "x = ": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
    

def get_weather(city: str):
    # Mocked weather data will change this to api later
    weather_data = {
        "Sydney": {"temperature": "25°C", "condition": "Sunny"},
        "Canberra": {"temperature": "10°C", "condition": "Cloudy"},
        "Melbourne": {"temperature": "10°C", "condition": "Rainy"},
    }
    
    if city in weather_data:
        return {"success": True, "data": weather_data[city]}
    else:
        return {"success": False, "error": f"Weather data for '{city}' not found."}


#---------------------------- tool profiles ----------------------------

TOOLS = {

    # Mathematics tools
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
    },



    # Weather tool
    "weather": {
        "function": get_weather,
        "description": "Retrieve the current weather for a specified city based on the data fetched from the weather function.",
        "example": "whats the weather in Sydney like in the next few days?"
    },

}
