from flask import jsonify

def error(error):
    response = {
        'status': 'error',
        "error": {
            'code': error.code,
            'message': error.description
        }
    }
    return jsonify(response), error.code
