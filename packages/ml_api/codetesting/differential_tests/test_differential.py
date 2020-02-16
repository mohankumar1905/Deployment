import math
import json
import pytest

from fooddelivery.config import config
from fooddelivery.predict import make_prediction
from fooddelivery.datamanagement.dataloadersaver import load_dataset

@pytest.mark.differential
def test_model_prediction_differential():
    """
    This test compares the prediction result similarity of
    the current model with the previous model's results.
    """
    
    test_data = load_dataset(filename=config.TESTING_DATA_FILE)
    multiple_test_json = test_data[99:600].to_json(orient='records')

    # Given
    previous_model_df = load_dataset(filename=config.PREVIOUS_TEST_FILE)
    previous_model_predictions = previous_model_df.predictions.values

    # When
    response = make_prediction(input_data=json.loads(multiple_test_json))
    current_model_predictions = response.get('predictions')

    # Then
    # diff the current model vs. the old model
    assert len(previous_model_predictions) == len(
        current_model_predictions)
    
    same_predictions_count = 0
    # Perform the differential test
    for previous_value, current_value in zip(
            previous_model_predictions, current_model_predictions):

        # convert numpy float64 to Python float.
        if previous_value.item() == current_value.item():
            same_predictions_count+=1

    assert same_predictions_count >= config.SAME_PREDICTION_COUNT
