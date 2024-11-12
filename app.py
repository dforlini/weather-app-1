from flask import Flask, render_template, request
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv('WEATHERAPI_KEY', 'df359fcb19174712ad5183015241211')  # Your WeatherAPI key

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=4"
            try:
                response = requests.get(url)
                
                # Check if the response is successful and contains JSON
                if response.status_code == 200:
                    data = response.json()
                    if "forecast" in data:
                        weather_data = []
                        for day in data['forecast']['forecastday']:
                            weather_data.append({
                                'date': day.get('date', 'N/A'),
                                'temperature_max': day['day'].get('maxtemp_f', 'N/A'),
                                'temperature_min': day['day'].get('mintemp_f', 'N/A'),
                                'condition': day['day']['condition'].get('text', 'N/A'),
                                'wind_speed': day['day'].get('maxwind_mph', 'N/A'),
                                'wind_direction': day['day'].get('maxwind_dir', 'N/A')
                            })
                    else:
                        error = "City not found. Please check the city name."
                else:
                    error = f"API request failed with status code {response.status_code}. Response text: {response.text}"
            
            except requests.exceptions.RequestException as e:
                error = f"An error occurred: {e}"
    
    return render_template('index.html', weather_data=weather_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)