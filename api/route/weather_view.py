from flask import request, abort
from flask.views import MethodView
from api.services.weather_access import WeatherAccess
from api.schema.config import BAD_REQUEST_CODE
import threading

REQUIRED_PARAMS = {
        'location': str,
        'rule': str
    }

class WeatherView(MethodView):

    weather_access = WeatherAccess()
    lock = threading.Lock()

    def get(self):

        # checks if we have all the required params and validity of type
        for param, param_type in REQUIRED_PARAMS.items():

            # the param is missing
            if param not in request.args:
                abort(BAD_REQUEST_CODE, f"Missing required parameter: {param}")

            # the param is not in the right type
            if not isinstance(request.args[param], param_type):
                abort(BAD_REQUEST_CODE, f"Invalid type for parameter: {param}. Expected type: {param_type.__name__}")

        with self.lock:
            return self.weather_access.get(request.args.get('location'),
                                    request.args.get('rule'),
                                    request.args.get('operator'))