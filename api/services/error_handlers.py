from flask import jsonify


def not_found_error(error):
    response = {
        'status': 'error',
        "error": {
            'code': 404,
            'message': error.description
        }
    }
    return jsonify(response), 404


def bad_request_error(error):
    response = {
        'status': 'error',
        "error": {
            'code': 400,
            'message': error.description
        }
    }
    return jsonify(response), 400


def internal_server_error(error):
    response = {
        'status': 'error',
        "error": {
            'code': 500,
            'message': error.description
        }
    }
    return jsonify(response), 500
