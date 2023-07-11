from api.schema.config import VALID_OPERATORS, INTERNAL_SERVER_ERROR_CODE
from flask import abort

def all_func_wrapper(rule_list):
    return lambda interval: all(
        func.filter_function(interval) for func in rule_list)

def any_func_wrapper(rule_list):
    return lambda interval: any(
        func.filter_function(interval) for func in rule_list)


def create_rules_function(rules_list, valid_operator):
    if valid_operator == VALID_OPERATORS[0]:
        return all_func_wrapper(rules_list)
    elif valid_operator == VALID_OPERATORS[1]:
        return any_func_wrapper(rules_list)

    abort(INTERNAL_SERVER_ERROR_CODE,
          "cannot create function from rules")