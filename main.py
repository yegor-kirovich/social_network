from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/weather_report')
def main_page():
    return render_template('main/main_page.html', title="Прогноз погоды")


@app.route('/weather_report/<day>-<month>-<year>')
def hello_world(day, month, year):
    return render_template('hello.html')


if __name__ == '__main__':
    app.run()