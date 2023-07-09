from flask import Flask
from api.route.WeatherView import WeatherView
from api.services.error_handlers import not_found_error, bad_request_error, \
    internal_server_error

app = Flask(__name__)

app.add_url_rule('/weather-conditions',
                 view_func=WeatherView.as_view('weather_conditions'),
                 methods=['GET'])
app.register_error_handler(404, f=not_found_error)
app.register_error_handler(400, f=bad_request_error)
app.register_error_handler(500, f=internal_server_error)

if __name__ == '__main__':
    app.run()
