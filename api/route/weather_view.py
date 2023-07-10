from flask import abort
from flask.views import MethodView
from api.services.weather_access import WeatherAccess

# from flask_inputs import Inputs
# from flask_inputs.validators import JsonSchema
#
# class MyInputValidation(Inputs):
#     json = [JsonSchema(schema={
#         'type': 'object',
#         'properties': {
#             'parameter': {'type': 'string'}
#         },
#         'required': ['parameter']
#     })]

class WeatherView(MethodView):

    weather_access = WeatherAccess()

    def get(self):

        # self.weather_access.get("bad_places", "temperature>30", None)
        return self.weather_access.get('40.75872069597532,-73.98529171943665',
                                    "temperature>30", None)


