import sys
import json
from fooddelivery.predict import make_prediction
from fooddelivery.datamanagement.dataloadersaver import load_dataset

result_checking = ['30 minutes', '65 minutes', '45 minutes', '10 minutes',
       '20 minutes', '120 minutes', '80 minutes']    

def test_make_single_prediction():
    #given
    test_data = load_dataset(filename='Data_Test.xlsx')
    single_test_json = test_data[0:1].to_json(orient='records')

    #when 
    subject = make_prediction(input_data=json.loads(single_test_json))

    #Then
    assert subject is not None
    assert subject['predictions'][0] in result_checking

def test_make_multiple_predictions():
    # Given
    test_data = load_dataset(filename='Data_Test.xlsx')
    original_data_length = len(test_data)
    multiple_test_json = test_data.to_json(orient='records')

    # When
    subject = make_prediction(input_data=json.loads(multiple_test_json))

    # Then
    assert subject is not None
    assert subject['predictions'][0] in result_checking

    # We expect some rows to be filtered out
    assert len(subject.get('predictions')) != original_data_length



