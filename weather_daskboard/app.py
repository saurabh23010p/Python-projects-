from flask import Flask, render_template, request
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    image_file = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        
        API_KEY = '1f1ceca488cfd98b4f62bd9899724acd'  
        URL = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'

        
        response = requests.get(URL)
        data = response.json()

        if 'list' not in data:
            error = data.get('message', 'Could not fetch weather data.')
        else:
            dates = []
            temperatures = []

           
            for forecast in data['list']:
                dt = datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
                if dt.hour == 12:
                    dates.append(dt.date())
                    temperatures.append(forecast['main']['temp'])

         
            os.makedirs('static/images', exist_ok=True)
            plt.figure(figsize=(10, 5))
            plt.plot(dates, temperatures, marker='o', color='orange')
            plt.title(f'Temperature Forecast for {city.title()}')
            plt.xlabel('Date')
            plt.ylabel('Temperature (°C)')
            plt.tight_layout()
            image_file = f'static/images/{city}_forecast.png'
            plt.savefig(image_file)
            plt.close()

    return render_template('index.html', image_file=image_file, error=error)

if __name__ == '__main__':
    app.run(debug=True)
