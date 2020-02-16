"""
This script should only be run in CI.
Never run it locally or you will disrupt the
differential test versioning logic.
"""

import pandas as pd
import json
from fooddelivery.predict import make_prediction
from fooddelivery.datamanagement.dataloadersaver import load_dataset

from api import config


def capture_predictions():
    """Save the test data predictions to a Excel."""

    test_data = load_dataset(filename=config.TESTING_DATA_FILE)

    # we take a slice with no input validation issues
    multiple_test_json = test_data[99:600].to_json(orient='records')

    predictions = make_prediction(input_data=json.loads(multiple_test_json))


    # save predictions for the test dataset
    predictions_df = pd.DataFrame(predictions)

    # hack here to save the file to the fooddelivery model
    # package of the repo, not the installed package
    predictions_df.to_excel(
        f'{config.PACKAGE_ROOT.parent}/fooddelivery/fooddelivery/datasets/{config.PREVIOUS_TEST_FILE}')


if __name__ == '__main__':
    capture_predictions()
