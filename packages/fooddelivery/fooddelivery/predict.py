import sys
import os
import numpy as np
import pandas as pd
from fooddelivery.datamanagement.dataloadersaver import load_pipeline
from fooddelivery.datamanagement.input_data_validation import validate_inputs
from fooddelivery.config import config
from fooddelivery import __version__ as _version
import logging
_logger = logging.getLogger(__name__)
pd.options.mode.chained_assignment = None

pipeline_filename = f'{config.PIPELINE_SAVE_FILE}{_version}.pkl'
food_delivery_pipe = load_pipeline(filename=pipeline_filename)

def make_prediction(*, input_data) -> dict:
	''' Make a Prediction Using Saved Model Pipeline'''
	data = pd.DataFrame(input_data)
	validated_data = validate_inputs(input_data=data)
	prediction = food_delivery_pipe.predict(validated_data[config.FEATURES])
	output = [config.TARGET_INVERSE_TRANSFORM_DICT.get(predicted) for predicted in prediction]
	response = {'predictions': output, 'version': _version}
	_logger.info(
        f'Making predictions with model version: {_version} '
        f'Inputs: {validated_data} '
        f'Predictions: {response}')
	return response

