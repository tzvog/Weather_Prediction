from flask import abort
from flask.views import MethodView

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

    def get(self):
        abort(404, "this is a bad message")
        return "this is me"
