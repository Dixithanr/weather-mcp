import azure.functions as func
import json
import random
from datetime import datetime, timedelta
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Weather API function processed a request.')

    try:
        # Get city name from query parameters or request body
        city_name = None
        
        # Try to get from query parameters first
        city_name = req.params.get('city')
        
        # If not in query params, try to get from request body
        if not city_name:
            try:
                req_body = req.get_json()
                if req_body:
                    city_name = req_body.get('city')
            except ValueError:
                pass
        
        # If still no city name, return error
        if not city_name:
            return func.HttpResponse(
                json.dumps({
                    "error": "City name is required. Please provide 'city' parameter in query string or request body."
                }),
                status_code=400,
                mimetype="application/json"
            )

        # Generate sample weather data
        weather_data = generate_sample_weather(city_name)
        
        return func.HttpResponse(
            json.dumps(weather_data, indent=2),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error occurred while processing the request."
            }),
            status_code=500,
            mimetype="application/json"
        )

def generate_sample_weather(city_name: str) -> dict:
    """
    Generate sample weather data for a given city.
    This is a mock implementation that returns realistic sample data.
    """
    
    # Sample weather conditions
    conditions = [
        "Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Thunderstorm", 
        "Snowy", "Foggy", "Windy", "Clear", "Overcast"
    ]
    
    # Generate random but realistic weather data
    current_temp = random.randint(-10, 35)  # Celsius
    feels_like = current_temp + random.randint(-3, 3)
    humidity = random.randint(30, 90)
    wind_speed = random.randint(0, 25)  # km/h
    pressure = random.randint(1000, 1030)  # hPa
    visibility = random.randint(5, 15)  # km
    
    # Current time
    current_time = datetime.now()
    
    # Generate forecast for next 5 days
    forecast = []
    for i in range(5):
        forecast_date = current_time + timedelta(days=i)
        forecast.append({
            "date": forecast_date.strftime("%Y-%m-%d"),
            "day": forecast_date.strftime("%A"),
            "high_temp": current_temp + random.randint(-5, 10),
            "low_temp": current_temp + random.randint(-10, 5),
            "condition": random.choice(conditions),
            "precipitation_chance": random.randint(0, 80)
        })
    
    weather_data = {
        "city": city_name.title(),
        "country": "Sample Country",  # You could enhance this with real country data
        "current_weather": {
            "temperature": current_temp,
            "feels_like": feels_like,
            "condition": random.choice(conditions),
            "humidity": f"{humidity}%",
            "wind_speed": f"{wind_speed} km/h",
            "pressure": f"{pressure} hPa",
            "visibility": f"{visibility} km",
            "last_updated": current_time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "forecast": forecast,
        "data_source": "Sample Weather API",
        "note": "This is sample weather data for demonstration purposes"
    }
    
    return weather_data
