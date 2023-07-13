from flask import Flask
from api.route.weather_view import WeatherView

app = Flask(__name__)


@app.errorhandler(Exception)
def error(error):
    response = {
        "status": "error",
        "error": {
            "code": error.code,
            "message": error.description
        }
    }
    return response, error.code

app.add_url_rule('/weather-conditions',
                 view_func=WeatherView.as_view('weather_conditions'),
                 methods=['GET'])

if __name__ == '__main__':
    app.run()
