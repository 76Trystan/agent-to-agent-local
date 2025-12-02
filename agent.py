from tools import TOOLS



Agents = {

    "scholar": {
        "name": "scholar",
        "system_prompt": "You are a scholarly research assistant. Provide detailed and accurate information.",
        "tools": [TOOLS.add, TOOLS.subtract, TOOLS.divide, TOOLS.quadratic]
    },


    # will add these soon, just testing scholar for now

    #"weather-man": {
    #   "name": "weather-man",
    #    "system_prompt": "You are a Weather Agent with access to real-time weather data.",
    #    "tools": ["get_current_weather", "get_weather_forecast"]
    #},

    #"Mathematician": {
    #    "name": "scholar",
    #   "system_prompt": "You are a mathematicion assistant. Provide detailed and accurate mathematical solutions.",
    #    "tools": ["add", "subtract", "divide", "quadratic"]
    #}

}