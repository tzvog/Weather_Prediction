import requests
from api.schema.config import TOKEN, NOT_FOUND_CODE,\
    BAD_REQUEST_CODE, INTERNAL_SERVER_ERROR_CODE, VALID_OPERATORS
from flask import abort, jsonify
from datetime import datetime, timedelta
from api.model.filter_rule import FilterRule
from api.services.rule_function_facotory import create_rules_function
import json

HOUR_INTERVAL_ADDITION = 72

class WeatherAccess:

    @staticmethod
    def __validate_and_return_lat_and_lon(location_string):
        """
        validates the string of longitude and latitude received from the request
        :param location_string: the location string required
        :return: the string split into long and latitude
        """
        split_lat_lon = location_string.split(',')

        # not the correct amount of parts
        if len(split_lat_lon) != 2:
            abort(BAD_REQUEST_CODE, "Invalid location provided, bad latitude and longitude format")

        return split_lat_lon[0], split_lat_lon[1]

    @staticmethod
    def __validate_and_create_list_of_functions(full_rules_string):
        """
        validates the rules and creates corresponding functions
        :param full_rules_string: the string with all the rules
        :return: which values to query within the rules and a list of rules
        with its corresponding function
        """

        # values to search when invoking the API
        weather_values_to_search = set()
        filter_rules = []

        rules_list = full_rules_string.split(',')

        # creates objects for our rules
        for rule in rules_list:
            rule_to_add = FilterRule(rule)
            filter_rules.append(rule_to_add)
            weather_values_to_search.add(rule_to_add.weather_parameter)

        return ','.join(weather_values_to_search), filter_rules

    @staticmethod
    def __validate_operator(operator):
        """
        checks that the operator is a valid one and if none
         exists gives it a default
        :param operator: the operator to check
        :return: the valid operator to use
        """

        if operator is None:
            return VALID_OPERATORS[0]

        if operator not in VALID_OPERATORS:
            abort(BAD_REQUEST_CODE, "Invalid operator provided, please use 'AND' or 'OR'")





    def get_timeline_from_text(self, rule_list, response, valid_operator):

        function_to_operate = create_rules_function(rule_list, valid_operator)

        response_in_json_format = json.loads(response)
        timelines = response_in_json_format.get('data', {}).get('timelines', {})

        if not timelines:
            abort(NOT_FOUND_CODE, 'data not found')

        start_time = timelines[0].get('startTime')
        end_time = timelines[0].get('endTime')
        intervals = timelines[0].get('intervals')

        # we don't have any intervals and the timing is off
        if not intervals or len(intervals) == 0 or start_time\
                is None or end_time is None:
            abort(NOT_FOUND_CODE, 'data not found')

        most_recent = {}
        most_recent["startTime"] = start_time
        most_recent["condition_met"] = function_to_operate(intervals[0].get('values', {}))

        return_val_list = []

        for interval in intervals:

            values = interval.get('values')

            # we didn't get the values
            if not values:
                abort(INTERNAL_SERVER_ERROR_CODE, 'not all values were found')


            current_condtion = function_to_operate(values)

            if current_condtion != most_recent["condition_met"]:

                most_recent["endTime"] = interval["startTime"]

                return_val_list.append(most_recent)

                most_recent = {}
                most_recent["startTime"] = interval["startTime"]
                most_recent["condition_met"] = current_condtion

        most_recent["endTime"] = end_time
        return_val_list.append(most_recent)

        return return_val_list


    def get(self, location, rule, operator):

        # creates the date needed to filter for
        start_date = datetime.now()
        end_date = start_date + timedelta(hours=HOUR_INTERVAL_ADDITION)

        lat, lon = self.__validate_and_return_lat_and_lon(location)
        fields, list_of_rules = self.__validate_and_create_list_of_functions(rule)
        valid_operator = self.__validate_operator(operator)

        URL = f"https://api.tomorrow.io/v4/timelines?location={lat},{lon}&fields={fields}&startTime={start_date.isoformat()}&endTime={end_date.isoformat()}&timesteps=1h&units=metric&apikey={TOKEN}"
        response = requests.get(url=URL)

        # checks if we got an error calling the API
        if response.status_code == INTERNAL_SERVER_ERROR_CODE or \
                response.status_code == BAD_REQUEST_CODE or \
                response.status_code == NOT_FOUND_CODE:
            abort(response.status_code, response.text)

        time_line = self.get_timeline_from_text(list_of_rules, response.text, valid_operator)

        return_val = {
            "status": "success",
            "data":
                {
                    "timeline": time_line
                }
        }

        return jsonify(return_val)

# if __name__ == '__main__':
#     k = WeatherAccess().get('40.75872069597532,-73.98529171943665', "temperature>30", None)
