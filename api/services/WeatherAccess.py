import requests
from api.schema.config import TOKEN, NOT_FOUND_CODE, BAD_REQUEST_CODE, INTERNAL_SERVER_ERROR_CODE
from flask import abort
from datetime import datetime, timedelta

DATE_INTERVAL_ADDITION = 3

# BASE_URL = 'https://api.tomorrow.io/v4/timelines?location=40.75872069597532,-73.98529171943665&fields=temperature&timesteps=1h&units=metric&apikey='

# BASE_URL = 'https://api.tomorrow.io/v4/timelines?location=40.75872069597532,-73.98529171943665&fields=temperature,windSpeed&&timesteps=1h&units=metric&apikey='


class WeatherAccess:

    def get(self):

        start_date = datetime.now()
        end_date = start_date + timedelta(days=DATE_INTERVAL_ADDITION)
        lat = str(40.75872069597532)
        lon = str(-73.98529171943665)
        fields = ','.join(['temperature', 'windSpeed'])

        URL = f"https://api.tomorrow.io/v4/timelines?location={lat},{lon}&fields={fields}&startTime={start_date.isoformat()}&endTime={end_date.isoformat()}&timesteps=1h&units=metric&apikey={TOKEN}"
        response = requests.get(url=URL)

        if response.status_code == INTERNAL_SERVER_ERROR_CODE:
            abort(INTERNAL_SERVER_ERROR_CODE, "an internal server error has happened")
        elif response.status_code == BAD_REQUEST_CODE:
            abort(BAD_REQUEST_CODE, "this was a bad request")
        elif response.status_code == NOT_FOUND_CODE:
            abort(NOT_FOUND_CODE, "the data requested was not found")

if __name__ == '__main__':
    k = WeatherAccess().get()