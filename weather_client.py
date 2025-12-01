import requests
from datetime import datetime, timedelta

def get_weather_forecast(city=None, latitude=None, longitude=None):
    """
    Get 7-day weather forecast.
    
    Args:
        city: City name
        latitude: Latitude coordinate
        longitude: Longitude coordinate
    
    Returns:
        Dictionary with weather data or error message
    """
    
    # If city provided, get coordinates first
    if city and not (latitude and longitude):
        coords = get_coordinates(city)
        if "error" in coords:
            return coords
        latitude = coords["latitude"]
        longitude = coords["longitude"]
    
    # Default to Sydney if nothing provided
    if not latitude or not longitude:
        latitude = -33.8688
        longitude = 151.2093
        city = "Sydney"
    
    try:
        # Open-Meteo API (free, no key needed)
        url = "https://api.open-meteo.com/v1/forecast"
        
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "windspeed_10m_max",
                "weathercode"
            ],
            "timezone": "auto",
            "forecast_days": 7
        }
        
        print(f"[DEBUG] Fetching weather for {city or f'({latitude}, {longitude})'}...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Format the response
        return format_weather_data(data, city or f"({latitude}, {longitude})")
        
    except requests.exceptions.Timeout:
        return {"error": "Weather API request timed out"}
    
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to weather API. Check internet connection."}
    
    except Exception as e:
        return {"error": f"Weather API error: {str(e)}"}


def get_coordinates(city):
    """
    Get coordinates for a city using geocoding API.
    
    Args:
        city: City name
    
    Returns:
        Dictionary with latitude and longitude
    """
    try:
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {"name": city, "count": 1}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return {
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "city": result["name"],
                "country": result.get("country", "")
            }
        else:
            return {"error": f"City '{city}' not found"}
        
    except Exception as e:
        return {"error": f"Geocoding error: {str(e)}"}


def format_weather_data(data, location):
    """
    Format raw weather data into readable structure.
    
    Args:
        data: Raw API response
        location: Location name
    
    Returns:
        Formatted weather dictionary
    """
    daily = data["daily"]
    
    # Weather code descriptions
    weather_descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        95: "Thunderstorm",
    }
    
    forecast = []
    
    for i in range(len(daily["time"])):
        day_data = {
            "date": daily["time"][i],
            "temp_max": daily["temperature_2m_max"][i],
            "temp_min": daily["temperature_2m_min"][i],
            "precipitation": daily["precipitation_sum"][i],
            "wind_speed": daily["windspeed_10m_max"][i],
            "condition": weather_descriptions.get(daily["weathercode"][i], "Unknown")
        }
        forecast.append(day_data)
    
    # Calculate averages
    avg_temp_max = sum(d["temp_max"] for d in forecast) / len(forecast)
    avg_temp_min = sum(d["temp_min"] for d in forecast) / len(forecast)
    total_precipitation = sum(d["precipitation"] for d in forecast)
    
    return {
        "location": location,
        "forecast": forecast,
        "summary": {
            "avg_temp_max": round(avg_temp_max, 1),
            "avg_temp_min": round(avg_temp_min, 1),
            "total_precipitation": round(total_precipitation, 1),
            "days": len(forecast)
        }
    }


def format_weather_for_llm(weather_data):
    """
    Format weather data into a string for LLM consumption.
    
    Args:
        weather_data: Dictionary from get_weather_forecast()
    
    Returns:
        Formatted string
    """
    if "error" in weather_data:
        return f"Weather API Error: {weather_data['error']}"
    
    location = weather_data["location"]
    forecast = weather_data["forecast"]
    summary = weather_data["summary"]
    
    output = f"Weather Forecast for {location}:\n\n"
    
    # Daily forecast
    for day in forecast:
        output += f"{day['date']}: {day['condition']}\n"
        output += f"  Temperature: {day['temp_min']}°C to {day['temp_max']}°C\n"
        output += f"  Precipitation: {day['precipitation']}mm\n"
        output += f"  Wind: {day['wind_speed']} km/h\n\n"
    
    # Summary
    output += f"7-Day Summary:\n"
    output += f"  Average high: {summary['avg_temp_max']}°C\n"
    output += f"  Average low: {summary['avg_temp_min']}°C\n"
    output += f"  Total precipitation: {summary['total_precipitation']}mm\n"
    
    return output


# Test function
if __name__ == "__main__":
    print("Testing Weather API...\n")
    
    # Test with Sydney
    weather = get_weather_forecast(city="Sydney")
    
    if "error" in weather:
        print(f"Error: {weather['error']}")
    else:
        print(format_weather_for_llm(weather))