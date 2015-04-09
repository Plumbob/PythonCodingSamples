#!flask/bin/python

# Server for the SH challenge
# Requires Python3


import flask
import jsonschema
import router_lib
from SHJsonValidator import SHJsonValidator

app = flask.Flask(__name__)

json_validator = SHJsonValidator()


@app.route('/route', methods=['POST'])
def get_route():
    
    #
    # Verify the payload is valid JSON
    try:
        json_validator.validate_input(flask.request.json)

    except jsonschema.exceptions.ValidationError as exc:
        return flask.json.jsonify({"error": exc.message}), 400
        
    #
    # Decode request payload    
    message    = flask.request.json['message'],
    recipients = flask.request.json['recipients']

    #
    # Process payload
    routes = router_lib.get_routes(recipients=recipients)
    
    #
    # Build response object
    BASE_RESPONSE = {'message': 'SH Rocks'}
    response = BASE_RESPONSE
    response['routes'] = routes

    # Send response    
    response_json = flask.json.jsonify(response)
    return response_json

if __name__ == '__main__':
    # Open server to world
    app.run('0.0.0.0')

    # Keep server in Debug mode
    # app.run(debug=True)
    
