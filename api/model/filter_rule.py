from api.schema.config import BAD_REQUEST_CODE,\
    VALID_WEATHER_PARAMETERS, RULE_OPERATORS, INTERNAL_SERVER_ERROR_CODE
from flask import abort

class FilterRule:

    def __init__(self, rule_str):

        self.rule_operator = self.__extract_rule_operator(rule_str)

        # breaks down the rule based upon the operator
        rule_break_down = rule_str.split(self.rule_operator)

        # checks that we only have one split there
        if len(rule_break_down) != 2:
            abort(BAD_REQUEST_CODE, "Invalid rule provided, bad rule format")

        self.weather_parameter = self.__extract_weather_parameter(rule_break_down[0])
        self.comparison_value = self.__extract_comparison_value(rule_break_down[1])
        self.filter_function = self.__create_filter_function()

    def __extract_weather_parameter(self, weather_parameter):
        """
        this extracts the weather parameter
        :param rule_break_down: the part of the rule that should contain the weather part
        :return: the weather value to use
        """

        # checks that the weather type is permitted
        if not (weather_parameter in VALID_WEATHER_PARAMETERS):
            abort(BAD_REQUEST_CODE, "Invalid rule provided, bad weather param")

        return weather_parameter

    def __extract_rule_operator(self, rule_str):
        """
        parses the operator we will work with
        :param rule_str: the rules we are going to parse
        :return: what operator we are going to use
        """

        # TODO check when both operators appear that could be an error
        # checks which operator we are working with
        if RULE_OPERATORS[0] in rule_str:
            return RULE_OPERATORS[0]
        elif RULE_OPERATORS[1] in rule_str:
            return RULE_OPERATORS[1]
        else:
            abort(BAD_REQUEST_CODE,
                  "Invalid rule provided, rule has an incorrect operator")

    def __extract_comparison_value(self, comparison_value):
        """
        extracts the comparison value from the string
        :param comparison_value: the value to compare
        :return: the classes comparison value
        """

        # try converting from string to integer
        try:
            comparison_value = int(comparison_value)
        except:
            abort(BAD_REQUEST_CODE,
                  "Invalid rule provided, bad comparison value")

        return comparison_value

    def __create_filter_function(self):
        """
        creates the comparison function
        :return: the comparison function
        """

        if self.rule_operator == RULE_OPERATORS[0]:

            if self.weather_parameter == VALID_WEATHER_PARAMETERS[0]:
                return lambda x: x[VALID_WEATHER_PARAMETERS[0]] < self.comparison_value
            elif self.weather_parameter == VALID_WEATHER_PARAMETERS[1]:
                return lambda x: x[VALID_WEATHER_PARAMETERS[1]] < self.comparison_value
            elif self.weather_parameter == VALID_WEATHER_PARAMETERS[2]:
                return lambda x: x[VALID_WEATHER_PARAMETERS[2]] < self.comparison_value
            elif self.weather_parameter == VALID_WEATHER_PARAMETERS[3]:
                return lambda x: [VALID_WEATHER_PARAMETERS[3]] < self.comparison_value
            else:
                abort(INTERNAL_SERVER_ERROR_CODE,
                      'Error could not find right filter function')

        elif self.rule_operator == RULE_OPERATORS[1]:

            if self.weather_parameter == VALID_WEATHER_PARAMETERS[0]:
                return lambda x: x[VALID_WEATHER_PARAMETERS[0]] > self.comparison_value
            elif self.weather_parameter == VALID_WEATHER_PARAMETERS[1]:
                return lambda x: x[VALID_WEATHER_PARAMETERS[1]] > self.comparison_value
            elif self.weather_parameter == VALID_WEATHER_PARAMETERS[2]:
                return lambda x: x[VALID_WEATHER_PARAMETERS[2]] > self.comparison_value
            elif self.weather_parameter == VALID_WEATHER_PARAMETERS[3]:
                return lambda x: x[VALID_WEATHER_PARAMETERS[3]] > self.comparison_value
            else:
                abort(INTERNAL_SERVER_ERROR_CODE,
                      'Error could not find right filter function')

        abort(INTERNAL_SERVER_ERROR_CODE,
              'Error could not find right filter function')