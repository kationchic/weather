from flask import Flask, render_template, request
import requests
from datetime import datetime
import pytz
import json


app = Flask(__name__)

@app.route('/') #отслеживаем главную страницу
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city'] #получаем название города
    with open('cities.json', 'r', encoding='utf-8') as file:
    	# Загружаем данные из файла
    	datac = json.load(file) 
    #данные по погоде города
    dataw=get_weather(datac[city])
    #рекомендации
    data = get_clothing_recommendation(dataw['main']['temp'], dataw['main']['humidity'])
    return render_template('city_weather.html', data=data, city=city, temp=dataw['main']['temp'])

def get_clothing_recommendation(temp, humidity):
    if temp < -10:
        res= "Тёплая зимняя одежда, шапка, шарф, тёплые сапоги"
    elif temp < 5:
        res= "Тёплый свитер, куртка, шапка"
    elif temp < 10:
        res= "Тёплый свитер"
    elif temp < 20:
        res= "Футболка с длинным рукавом"
    elif temp < 27:
        res= "Футболка, шорты"
    else:
    	return "Оставайтесь дома под кондиционером"

    if humidity>75:
    	res+=", зонт"
    return res


def get_weather(city_data):
    api_key = "4644a7f2ffb88a4820b1030e0a112417"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={city_data['lat']}&lon={city_data['lon']}&appid={api_key}&units=metric&lang=ru"
    try:
    	response = requests.get(url).json()
    except RequestException as e:
	    print(f"Ошибка: {e}") # Любые ошибки requests
    return response


if __name__=="__main__":
	app.run(debug=True)
