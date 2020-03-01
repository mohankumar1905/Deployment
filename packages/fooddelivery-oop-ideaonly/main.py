'''Modelling'''

import warnings
from imblearn.over_sampling import RandomOverSampler
import pandas as pd
from lightgbm import LGBMClassifier
from feature_extraction import FeatureExtraction
from data_preprocessing import DataPreprocessing
warnings.filterwarnings("ignore")

class ModelManager:
    ''' Modeling'''
    def __init__(self, feature_extraction: FeatureExtraction):
        self.feature_extraction = feature_extraction
        self.model = None
        self.ros = RandomOverSampler(random_state=0)
        self.x_train_oversampled = None
        self.y_train_oversampled = None

    def get_training_variables(self):
        '''return all training variables except target - change according to your need'''
        return [var for var in self.feature_extraction.x_train.columns if var not in ['Delivery_Time']]

    def fit_model(self, training_variables: list()):
        '''Model Fitting'''
        training_variables = self.get_training_variables()
        self.x_train_oversampled, self.y_train_oversampled = self.ros.fit_resample(self.feature_extraction.x_train[training_variables], self.feature_extraction.y_train)
        self.model = LGBMClassifier(n_estimators=3000, random_state=1994, nfold=5, learning_rate=0.03, colsample_bytree=0.2, objective='multiclass')
        self.model.fit(self.x_train_oversampled, self.y_train_oversampled, eval_metric='multi_logloss', verbose=200)

    def run_pipeline(self, training: bool = False):
        '''Make a Pipeline for both training and prediction'''
        self.feature_extraction.feature_ext(training)
        training_variables = self.get_training_variables()
        if training:
            self.fit_model(training_variables)
        pred = self.model.predict(self.feature_extraction.dataframe[training_variables])
        print(pred)
        return pred

if __name__ == '__main__':
    DATAFRAME = pd.read_excel("Data_Train.xlsx")
    DATA_PREPROCESSING = DataPreprocessing(DATAFRAME)
    FEATURE_EXTRACTION = FeatureExtraction(DATA_PREPROCESSING)
    MANAGER = ModelManager(FEATURE_EXTRACTION)
    MANAGER.run_pipeline(training=True)
