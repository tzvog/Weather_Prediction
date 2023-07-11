import requests
from api.schema.config import TOKEN, NOT_FOUND_CODE,\
    BAD_REQUEST_CODE, INTERNAL_SERVER_ERROR_CODE, VALID_OPERATORS
from flask import abort, jsonify
from datetime import datetime, timedelta
from api.model.filter_rule import FilterRule
from api.services.rule_function_aggregation_factory import aggregate_rules_function
import json

HOUR_INTERVAL_ADDITION = 71

class WeatherAccess:

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

        time_line = self.__create_timeline(list_of_rules,
                                           response.text, valid_operator)

        return jsonify({"status": "success",  "data": {"timeline": time_line}})

    def __validate_and_return_lat_and_lon(self, location_string):
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


    def __validate_and_create_list_of_functions(self, full_rules_string):
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

    def __validate_operator(self, operator):
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

        return operator

    def __create_timeline(self, rule_list, response, operator):
        """
        this function creates a timeline from the response
        :param rule_list: the list of rules to filter by
        :param response: the response we got from the server
        :param operator: the operator to work with
        :return: the timeline in a list
        """

        function_to_operate = aggregate_rules_function(rule_list, operator)
        start_time, end_time, intervals = self.__extract_intervals_data(response)

        # create an initial status
        most_recent_status = {"startTime": start_time,
                              "condition_met": function_to_operate(
                                  intervals[0].get('values', {}))}

        return_val_list = []

        # create a timeline using all intervals
        for interval in intervals:

            values = interval.get('values')

            # we didn't get the values
            if not values:
                abort(INTERNAL_SERVER_ERROR_CODE, 'not all values were found')

            current_condition = function_to_operate(values)

            # the condition has switched
            if current_condition != most_recent_status["condition_met"]:

                most_recent_status["endTime"] = interval["startTime"]

                # flush the current status
                return_val_list.append(most_recent_status)

                # create a new status to be used
                most_recent_status = {"startTime": interval["startTime"],
                                      "condition_met": current_condition}

        # adds the last value only if the change was
        # not registered via the last result
        if not most_recent_status["startTime"] == end_time:
            most_recent_status["endTime"] = end_time
            return_val_list.append(most_recent_status)

        return return_val_list

    def __extract_intervals_data(self, response):
        """
        extracts the interval data from a given response text
        :param response the response in text format
        :return: end_time, start_time, intervals
        """

        # refactor the text and get the reponses from it
        response_in_json_format = json.loads(response)
        timelines = response_in_json_format.get('data', {}).get('timelines', {})

        # validate what we have gotten
        if not timelines:
            abort(NOT_FOUND_CODE, 'data not found')

        start_time = timelines[0].get('startTime')
        end_time = timelines[0].get('endTime')
        intervals = timelines[0].get('intervals')

        # we don't have any intervals and the timing is off
        if not intervals or len(intervals) == 0 or start_time \
                is None or end_time is None:
            abort(NOT_FOUND_CODE, 'data not found')

        return start_time, end_time, intervals



if __name__ == '__main__':
    k = WeatherAccess().get('40.75872069597532,-73.98529171943665', "temperature>0", 'OR')
