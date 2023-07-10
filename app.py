from flask import Flask
from api.route.weather_view import WeatherView
from api.services.error_handlers import error

app = Flask(__name__)

app.add_url_rule('/weather-conditions',
                 view_func=WeatherView.as_view('weather_conditions'),
                 methods=['GET'])
app.register_error_handler(404, f=error)
app.register_error_handler(400, f=error)
app.register_error_handler(500, f=error)

if __name__ == '__main__':
    app.run()
