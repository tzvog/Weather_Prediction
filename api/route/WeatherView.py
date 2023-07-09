from flask.views import MethodView

class WeatherView(MethodView):

    def get(self):
        return "this is me"