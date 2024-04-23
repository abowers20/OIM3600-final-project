from flask import Flask, render_template, request
from weather import get_weather_by_coordinates, get_weather_details, get_weather, reverse_geocoding, get_coordinates_for_city, get_5day_forecast
from config import OPENWEATHER_APIKEY

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    """
    Render the index page.

    Returns:
    - HTML: Rendered index.html template.
    """
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    """
    Handle POST request to fetch weather data.

    This function checks if the geolocation toggle is checked.
    If checked, it gets weather data by coordinates and reverse geocoding.
    If not checked, it gets weather data by city name and country code.

    Returns:
    - HTML: Rendered weather.html template with weather details.
    - Error message template if there's an exception.
    """
    try:
        if 'geolocation-toggle' in request.form:
            lat = request.form['city']
            lon = request.form['country']
            api_key = OPENWEATHER_APIKEY
            weather_data = get_weather_by_coordinates(lat, lon, api_key)
            city, country, state = reverse_geocoding(lat, lon, api_key)
        else:
            city_name = request.form['city']
            country_code = request.form['country']
            state_code = request.form.get('state', '')  # Optional state code
            api_key = OPENWEATHER_APIKEY

            # Get coordinates for the city
            coordinates = get_coordinates_for_city(city_name, state_code, country_code, api_key)
            if not coordinates:
                raise Exception("Failed to get coordinates for the city.")

            lat = coordinates.get("latitude")
            lon = coordinates.get("longitude")

            # Get weather data using city name and country code
            weather_data = get_weather(city_name, country_code, state_code, api_key)
            city, country, state = reverse_geocoding(lat, lon, api_key)

        # Check if weather data is None
        if weather_data is None:
            return render_template('error.html', message="Weather data not found.")

        # Extract additional weather details
        weather_details = get_weather_details(weather_data)

        # Check if location details are available
        if city and country:
            location_details = {
                "city": city,
                "country": country,
                "state": state
            }
        else:
            location_details = None

        # Get 5-day forecast
        forecast_data = get_5day_forecast(lat, lon, api_key)

        return render_template('weather.html', weather_details=weather_details, location_details=location_details, forecast_data=forecast_data)

    except Exception as e:
        # Log the exception
        app.logger.exception("An error occurred while fetching weather data: %s", str(e))
        return render_template('error.html', error_message="Failed to retrieve weather information. Please try again later."), 500

if __name__ == '__main__':
    app.run(debug=True)
