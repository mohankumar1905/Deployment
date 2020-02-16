import os

PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TRAINED_MODEL_DIRECTORY = PACKAGE_ROOT + '/train'
DATASET_DIRECTORY = PACKAGE_ROOT + '/datasets'

#filenames
TESTING_DATA_FILE = 'Data_Test.xlsx'
TRAINING_DATA_FILE = 'Data_Train.xlsx'
TARGET = 'Delivery_Time'
PIPELINE_NAME = 'food_delivery_model'
PIPELINE_SAVE_FILE = f'{PIPELINE_NAME}_output_v'


TARGET_TRANSFORM_DICT = {'30 minutes': 3,
 '65 minutes': 5,
 '45 minutes': 4,
 '10 minutes': 0,
 '20 minutes': 2,
 '120 minutes': 1,
 '80 minutes': 6}

TARGET_INVERSE_TRANSFORM_DICT = {3: '30 minutes',
 5: '65 minutes',
 4: '45 minutes',
 0: '10 minutes',
 2: '20 minutes',
 1: '120 minutes',
 6: '80 minutes'}

#Variables

FEATURES = ['Restaurant', 'Location', 'Cuisines', 'Average_Cost', 'Minimum_Order',
       'Rating', 'Votes', 'Reviews']

#Not Null Check Columns - Prediction

CATEGORICAL_NA_NOT_ALLOWED = ['Restaurant', 'Location', 'Cuisines']

VALUES_TO_REPLACE = ["Opening Soon", "NEW", "-", "Temporarily Closed"]
DATA_CORRECTION_VARIABLES = ['Average_Cost', 'Minimum_Order', 'Votes', 'Reviews', 'Rating']
MEDIAN_IMPUTATION_VARIABLES = ['Average_Cost', 'Minimum_Order']
NULL_HANDLING_NUMERICAL_COLUMNS = ['Average_Cost', 'Minimum_Order', 'Votes', 'Reviews', 'Rating']
NULL_HANDLING_CATEGORICAL_COLUMNS = ['Location', 'Cuisines']
RESTAURANT_AGG_COLOUMNS = ['Location', 'Restaurant', 'restaraunt_counts']
LOCATION_AGG_COLOUMNS = ['Restaurant', 'Location', 'location_counts']
INHERITING_INFO_COLUMNS = ['Votes', 'Reviews', 'Rating']
CUSINE_VARIABLE = 'Cuisines'
ORDINAL_ENCODING_COLUMNS = ['Cuisines', 'Location', 'Restaurant', 'city']
LABEL_ENCODING_COLUMN ='Delivery_Time'
CITIES_TO_CHECK = ['pune', 'mumbai', 'noida', 'delhi', 'kolkata', 'bangalore', 'gurgoan', 'hyderabad']

#testing 

SAME_PREDICTION_COUNT = 10
PREVIOUS_TEST_FILE = 'test_data_predictions.xlsx'