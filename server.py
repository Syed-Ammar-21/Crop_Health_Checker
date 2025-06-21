
# NAME : SYED AMMAR 


from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)



API_KEY = '3ff57dff9da89d2043b3a2a28ebc3f28'  
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# OPTIMAL GROWING CONDITIONS FOR CROPS

OPTIMAL_CONDITIONS = {
    "wheat": {"temp_min": 10, "temp_max": 25, "humidity_min": 50, "humidity_max": 70, "pressure_min": 1000, "pressure_max": 1020},
    "corn": {"temp_min": 18, "temp_max": 30, "humidity_min": 60, "humidity_max": 80, "pressure_min": 1005, "pressure_max": 1025},
    "rice": {"temp_min": 20, "temp_max": 35, "humidity_min": 70, "humidity_max": 90, "pressure_min": 1008, "pressure_max": 1030},
    "cotton": {"temp_min": 21, "temp_max": 32, "humidity_min": 60, "humidity_max": 85, "pressure_min": 1002, "pressure_max": 1025}
}

@app.route('/crop_health', methods=['GET'])
def check_crop_health():
    city = request.args.get('city')
    crop = request.args.get('crop').lower()

    if not city or not crop:
        return jsonify({'error': 'City and crop parameters are required'}), 400
    
    if crop not in OPTIMAL_CONDITIONS:
        return jsonify({'error': f'Invalid crop type: {crop}. Supported crops: wheat, corn, rice, cotton'}), 400

    # FETCH REAL TIME WEATHER DATA

    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 404:
        return jsonify({'error': f'Invalid city name: {city}. Please enter a valid city.'}), 404
    elif response.status_code != 200:
        return jsonify({'error': 'Could not retrieve weather data'}), response.status_code

    weather_data = response.json()
    current_temp = weather_data['main']['temp']
    current_humidity = weather_data['main']['humidity']
    current_pressure = weather_data['main']['pressure']

    # COMPARING
    optimal = OPTIMAL_CONDITIONS[crop]
    temp_status = "Optimal" if optimal["temp_min"] <= current_temp <= optimal["temp_max"] else "Not Optimal"
    humidity_status = "Optimal" if optimal["humidity_min"] <= current_humidity <= optimal["humidity_max"] else "Not Optimal"
    pressure_status = "Optimal" if optimal["pressure_min"] <= current_pressure <= optimal["pressure_max"] else "Not Optimal"

    overall_health = "Healthy" if temp_status == humidity_status == pressure_status == "Optimal" else "Unhealthy"

    result = {
        "city": city,
        "crop": crop,
        "current_temp": current_temp,
        "current_humidity": current_humidity,
        "current_pressure": current_pressure,
        "temp_status": temp_status,
        "humidity_status": humidity_status,
        "pressure_status": pressure_status,
        "overall_health": overall_health
    }
    
    return jsonify(result)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)