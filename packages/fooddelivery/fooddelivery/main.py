import sys
import os
from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier
import pipeline
from fooddelivery.datamanagement.dataloadersaver import load_dataset, save_pipeline
from fooddelivery.config import config
from fooddelivery import __version__ as _version
import logging
_logger = logging.getLogger(__name__)

def run_training() -> None:
	'''Train the Model'''
	#Read Training Data
	data = load_dataset(filename=config.TRAINING_DATA_FILE)
	data[config.TARGET] = data[config.TARGET].map(config.TARGET_TRANSFORM_DICT)
	#divide train and test
	x_train, x_test, y_train, y_test = train_test_split(
		data[config.FEATURES], data[config.TARGET], test_size=0.2, random_state=1994) #Set the seed.
	print(data.info())
	#Pass the Train Data to Pipeline
	pipeline.food_delivery_pipe.fit(x_train, y_train)

	_logger.info(f'saving model version: {_version}')
	#Save Pipeline
	save_pipeline(pipeline_to_persist=pipeline.food_delivery_pipe)

if __name__ == '__main__':
	run_training()
