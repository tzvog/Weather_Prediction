import requests
from api.schema.config import TOKEN, NOT_FOUND_CODE,\
    BAD_REQUEST_CODE, INTERNAL_SERVER_ERROR_CODE, VALID_WEATHER_PARAMETERS, \
    RULE_OPERATORS, VALID_OPERATORS
from flask import abort
from datetime import datetime, timedelta

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

        weather_values_to_search = set()
        rules_sets = []

        rules_list = full_rules_string.split(',')

        # creates objects for our rules
        for rule in rules_list:

            # checks which operator we are working with
            if RULE_OPERATORS[0] in rule:
                rule_operator = RULE_OPERATORS[0]
            elif RULE_OPERATORS[1] in rule:
                rule_operator = RULE_OPERATORS[1]
            else:
                abort(BAD_REQUEST_CODE, "Invalid rule provided, rule has an incorrect operator")

            rule_break_down = rule.split(rule_operator)

            # checks that we only have one split there
            if len(rule_break_down) != 2:
                abort(BAD_REQUEST_CODE, "Invalid rule provided, bad rule format")

            # checks that the weather is permited
            if not rule_break_down[0] in VALID_WEATHER_PARAMETERS:
                abort(BAD_REQUEST_CODE, "Invalid rule provided, bad weather param")

            # adds to the set of values we are going to check
            weather_values_to_search.add(rule_break_down[0])

            # try converting from string to integer
            try:
                comparison_value = int(rule_break_down[1])
            except:
                abort(BAD_REQUEST_CODE, "Invalid rule provided, bad comparison value")

            # adds the rule we are going to work with
            rules_sets.append((rule_break_down[0],
                               rule_operator, comparison_value))

        return ','.join(weather_values_to_search), rules_sets

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
            return abort(BAD_REQUEST_CODE, "Invalid operator provided, please use 'AND' or 'OR'")


    def get(self, location, rule, operator):

        # creates the date needed to filter for
        start_date = datetime.now()
        end_date = start_date + timedelta(hours=HOUR_INTERVAL_ADDITION)

        lat, lon = self.__validate_and_return_lat_and_lon(location)
        fields, list_of_rules = self.__validate_and_create_list_of_functions(rule)
        valid_operator = self.__validate_operator(operator)

        URL = f"https://api.tomorrow.io/v4/timelines?location={lat},{lon}&fields={fields}&startTime={start_date.isoformat()}&endTime={end_date.isoformat()}&timesteps=1h&units=metric&apikey={TOKEN}"
        response = requests.get(url=URL)

        if response.status_code == INTERNAL_SERVER_ERROR_CODE:
            abort(INTERNAL_SERVER_ERROR_CODE, response.text)
        elif response.status_code == BAD_REQUEST_CODE:
            abort(BAD_REQUEST_CODE, response.text)
        elif response.status_code == NOT_FOUND_CODE:
            abort(NOT_FOUND_CODE, response.text)

if __name__ == '__main__':
    # k = WeatherAccess().get('40.75872069597532,-73.98529171943665', "temperature>30", None)
    k = WeatherAccess().get('a,b',
                            "temperature>30", "xcvxcv")
