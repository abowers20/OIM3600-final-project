import requests, pytz
from typing import Dict, List, Optional
from datetime import datetime

def get_weather_by_coordinates(lat: float, lon: float, api_key: str) -> Optional[Dict]:
    """
    Get weather data for specified latitude and longitude using the OpenWeatherMap API.

    Parameters:
    - lat (float): Latitude coordinate.
    - lon (float): Longitude coordinate.
    - api_key (str): API key for accessing the OpenWeatherMap API.

    Returns:
    - Dict or None: Weather data if successful, None otherwise.
    """
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve weather data. Status code:", response.status_code)
        return None

def get_weather(city_name: str, country_code: str, state_code: str, api_key: str) -> Optional[Dict]:
    """
    Get weather data for a specified city, state, and country using the OpenWeatherMap API.

    Parameters:
    - city_name (str): Name of the city.
    - country_code (str): Country code.
    - state_code (str): State code (if available).
    - api_key (str): API key for accessing the OpenWeatherMap API.

    Returns:
    - Dict or None: Weather data if successful, None otherwise.
    """
    if state_code:
        query = f"{city_name},{state_code},{country_code}"
    else:
        query = f"{city_name},{country_code}"

    url = f'http://api.openweathermap.org/data/2.5/weather?q={query}&appid={api_key}&units=imperial'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve weather data. Status code:", response.status_code)
        return None

def get_weather_details(weather_data: Dict) -> Optional[Dict]:
    """
    Get detailed weather information from the weather data.

    Parameters:
    - weather_data (Dict): Weather data obtained from the OpenWeatherMap API.

    Returns:
    - Dict or None: Detailed weather information if successful, None otherwise.
    """
    if weather_data:
        # Extract additional weather information
        feels_like = weather_data.get("main", {}).get("feels_like")
        wind_speed = weather_data.get("wind", {}).get('speed')
        humidity = weather_data.get("main", {}).get("humidity")
        weather_main = weather_data.get("weather", [{}])[0].get("main")
        weather_description = weather_data.get("weather", [{}])[0].get("description")
        temperature = weather_data.get("main", {}).get("temp")
        latitude = weather_data.get("coord", {}).get("lat")
        longitude = weather_data.get("coord", {}).get("lon")

        return {
            "feels_like": feels_like,
            "wind_speed": wind_speed,
            "humidity": humidity,
            "weather_main": weather_main,
            "weather_description": weather_description,
            "temperature": temperature,
            "latitude": latitude,
            "longitude": longitude
        }
    else:
        return None

def get_coordinates_for_city(city_name: str, state_code: str, country_code: str, api_key: str) -> Optional[Dict]:
    """
    Get latitude and longitude for a specified city, state, and country using the OpenWeatherMap API.

    Parameters:
    - city_name (str): Name of the city.
    - state_code (str): State code (if available).
    - country_code (str): Country code.
    - api_key (str): API key for accessing the OpenWeatherMap API.

    Returns:
    - Dict or None: Latitude and longitude if successful, None otherwise.
    """
    if state_code:
        query = f"{city_name},{state_code},{country_code}"
    else:
        query = f"{city_name},{country_code}"

    url = f'http://api.openweathermap.org/data/2.5/weather?q={query}&appid={api_key}&units=imperial'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("coord"):
            latitude = data["coord"]["lat"]
            longitude = data["coord"]["lon"]
            return {"latitude": latitude, "longitude": longitude}
        else:
            print("Coordinates not found in response:", data)
            return None
    else:
        print("Failed to retrieve coordinates. Status code:", response.status_code)
        return None

def reverse_geocoding(latitude, longitude, api_key):
    """
    Reverse geocoding to get location details (city, country, state) from latitude and longitude.

    Parameters:
    - latitude (float): Latitude coordinate.
    - longitude (float): Longitude coordinate.
    - api_key (str): API key for accessing the OpenWeatherMap API.

    Returns:
    - Tuple[str, str, str] or None: A tuple containing city, country, and state.
                                     None if the location data is not found or an error occurs.
    """
    reverse_geocode_url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={latitude}&lon={longitude}&limit=1&appid={api_key}"
   
    try:
        response = requests.get(reverse_geocode_url)

        if response.status_code == 200:
            data = response.json()
            if data:
                if isinstance(data, list):
                    location_data = data[0]  # Get the first element of the list
                else:
                    location_data = data

                city = location_data.get('name', 'City not found')
                country = location_data.get('country', 'Country not found')
                state = location_data.get('state', '')  # Get state if available, otherwise empty string
                return city, country, state
            else:
                return None, None, None  # Return None for all values if data is empty
        else:
            # Handle API error
            print("Reverse geocoding API error:", response.text)
            return None, None, None

    except Exception as e:
        # Handle any exceptions
        print("Reverse geocoding error:", str(e))
        return None, None, None

def get_5day_forecast(lat: float, lon: float, api_key: str) -> Optional[List[Dict]]:
    """
    Get 5-day weather forecast for specified latitude and longitude using the OpenWeatherMap API.
    Converts timestamps from UTC to EST and formats date/time.

    Parameters:
    - lat (float): Latitude coordinate.
    - lon (float): Longitude coordinate.
    - api_key (str): API key for accessing the OpenWeatherMap API.

    Returns:
    - List[Dict] or None: Weather forecast data for the next 5 days if successful, None otherwise.
    """
    url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&cnt={30}&units=imperial'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "list" in data:
            # Extract necessary data: date, temperature, and main weather
            forecast_data = []
            for forecast in data["list"]:
                utc_time = datetime.strptime(forecast["dt_txt"], '%Y-%m-%d %H:%M:%S')
                utc_time = pytz.utc.localize(utc_time)
                est_time = utc_time.astimezone(pytz.timezone('US/Eastern'))
                formatted_time = est_time.strftime('%Y-%m-%d %I:%M %p')
                forecast_data.append({
                    "date": formatted_time,
                    "temperature": forecast["main"]["temp"],
                    "weather_main": forecast["weather"][0]["main"]
                })
            
            return forecast_data
        else:
            print("No forecast data found.")
            return None
    else:
        print("Failed to retrieve forecast data. Status code:", response.status_code)
        return None