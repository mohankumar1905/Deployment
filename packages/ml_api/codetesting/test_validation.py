from fooddelivery.config import config as model_config
from fooddelivery.datamanagement.dataloadersaver import load_dataset

import json

def test_prediction_endpoint_validation_200(flask_test_client):
    # Given
    # Load the test data from the fooddelivery package
    # This is important as it makes it harder for the test
    # data versions to get confused by not spreading it
    # across packages.

    test_data =  load_dataset(filename=model_config.TESTING_DATA_FILE)
    post_json = test_data.to_json(orient='records')
    response = flask_test_client.post('/v1/predict/fooddelivery', json = json.loads(post_json))

    assert response.status_code == 200
    response_json = json.loads(response.data)
   
    # Check correct number of errors removed
    assert len(response_json.get('predictions')) + len(
        response_json.get('errors')) == len(test_data)
