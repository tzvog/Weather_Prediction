from flask import Flask, jsonify
from api.route.WeatherView import WeatherView

app = Flask(__name__)

def not_found_error(error):
    response = {
        'status': 'error',
        "error": {
            'code': 404,
            'message': error.description
        }
    }
    return jsonify(response), 404

def bad_request_error(error):
    response = {
        'status': 'error',
        "error": {
            'code': 400,
            'message': error.description
        }
    }
    return jsonify(response), 400

def internal_server_error(error):
    response = {
        'status': 'error',
        "error": {
            'code': 500,
            'message': error.description
        }
    }
    return jsonify(response), 500

app.add_url_rule('/weather-conditions', view_func=WeatherView.as_view('weather_conditions'), methods=['GET'])
app.register_error_handler(404, f=not_found_error)
app.register_error_handler(400, f=bad_request_error)
app.register_error_handler(500, f=internal_server_error)

if __name__ == '__main__':
    app.run()
