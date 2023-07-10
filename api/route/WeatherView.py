from flask import abort
from flask.views import MethodView
from api.services.WeatherAccess import WeatherAccess

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

        self.weather_access.get()

        return "this is me"
