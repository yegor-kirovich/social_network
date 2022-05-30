from flask import Flask
from flask import render_template
import requests
app = Flask(__name__)

key = "a514058a14b2261ec0739ceadb112c41"


@app.route('/weather_report/<city>')
def main_page(city):
    res = requests.get("http://api.openweathermap.org/data/2.5/find",
                       params={'q': city, 'type': 'like', 'units': 'metric', 'APPID': key})
    print(res.text)
    data = res.json()

    return render_template('main/main_page.html', title="Прогноз погоды")


@app.route('/weather_report/<day>-<month>-<year>')
def hello_world(day, month, year):
    return render_template('hello.html')


if __name__ == '__main__':
    app.run()