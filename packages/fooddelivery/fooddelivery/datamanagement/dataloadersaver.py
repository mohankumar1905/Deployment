import os
import sys
import joblib
import pandas as pd
from imblearn.pipeline import Pipeline
from fooddelivery.config import config
from fooddelivery import __version__ as _version
import logging

_logger = logging.getLogger(__name__)

def load_dataset(*, filename: str) -> pd.DataFrame:
	data = pd.read_excel(f'{config.DATASET_DIRECTORY}/{filename}')
	return data

def save_pipeline(*, pipeline_to_persist) -> None:
	'''Persist the pipeline'''
	save_file_name = f'{config.PIPELINE_SAVE_FILE}{_version}.pkl'
	save_path = f'{config.TRAINED_MODEL_DIRECTORY}/{save_file_name}'
	remove_old_pipelines(files_to_keep=save_file_name)
	joblib.dump(pipeline_to_persist, save_path)
	_logger.info(f'saved_pipeline: {save_file_name}')

def load_pipeline(*, filename:str) -> Pipeline:
	'''Load the persisted pipeline'''
	filepath = f'{config.TRAINED_MODEL_DIRECTORY}/{filename}'
	saved_pipeline = joblib.load(filename=filepath)
	return saved_pipeline

def remove_old_pipelines(*, files_to_keep) -> None:
	"""
    Remove old model pipelines.
    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.
    """

	for filename in os.listdir(config.TRAINED_MODEL_DIRECTORY):
		if ((filename == (files_to_keep)) or (filename.endswith(".py"))):
			# print(os.path.join(directory, filename))
			_logger.info(f"files not going to be deleted: {filename}")
		else:
			_logger.info(f"files going to be deleted: {filename}")
			if os.path.isfile(f'{config.TRAINED_MODEL_DIRECTORY}/{filename}'):
				os.remove(f'{config.TRAINED_MODEL_DIRECTORY}/{filename}')
			else:    ## Show an error ##
				_logger.info(f"Error: {filename} is a folder")