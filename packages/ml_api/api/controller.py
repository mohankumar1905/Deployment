from flask import Blueprint, request, jsonify
from fooddelivery.predict import make_prediction
from fooddelivery import __version__ as _version
from api.config import get_logger
from api import __version__ as api_version
from api.validation import validate_inputs

_logger = get_logger(logger_name=__name__)

prediction_app = Blueprint('prediction_app', __name__)

@prediction_app.route('/health', methods=['GET'])
def health():
    if request.method == 'GET':
        return 'ok'

@prediction_app.route('/version', methods=['GET'])
def version():
    if request.method == 'GET':
        return jsonify({
            'model_version': _version,
            'api_version': api_version
        })

@prediction_app.route('/v1/predict/fooddelivery', methods = ['POST'])
def predict():
    if request.method == 'POST':
        # Step 1: Extract POST data from request body as JSON
        json_data = request.get_json()
        _logger.debug(f'Inputs: {json_data}')

        #Step 2: Validate the input using marshmallow schema
        input_data, errors = validate_inputs(input_data=json_data)

        # Step 3: Model prediction
        result = make_prediction(input_data=json_data)
        _logger.debug(f'Outputs: {result}')

        # Step 4: Convert numpy ndarray to list
        # This step is not happening because we
        # already did that while converting probability into
        # real values
        prediction = result.get('predictions')
        version = result.get('version')

        # Step 5: Return the response as JSON
        return jsonify({
            'predictions': prediction,
            'errors': errors,
            'version': version
        })