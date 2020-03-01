''' Data Preprocessing Script'''
import re
import numpy as np
import pandas as pd


class DataPreprocessing:
    ''' List of Data Preprocessing Steps
    Data Preparation Pipeline Step No:1'''
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe
        self.rupee_to_integer_median_dict = {}
        self.replace_values = ["Opening Soon", "NEW", "-", "Temporarily Closed"]

    def dataset_info(self):
        ''' Shows Train Dataset info'''
        print("Shape of the dataset: " + str(self.dataframe.shape))
        print("Displaying the dataset")
        print(self.dataframe.head())
        print("Unique Values in the Dataset are: ")
        print(self.dataframe.nunique())
        print("Datatypes and Null Values of each col")
        print(self.dataframe.info(null_counts=True, verbose=True))

    def rupee_to_integer(self, col, training):
        ''' Convert rupee col from string to integer'''
        self.dataframe[col] = self.dataframe[col].apply(lambda x: re.sub("[^0-9]", "", str(x)))
        self.dataframe[col][self.dataframe[col] == ""] = -1
        self.dataframe[col] = self.dataframe[col].astype(int)
        if training:
            self.rupee_to_integer_median_dict[col] = self.dataframe[col].median()
        self.dataframe[col][self.dataframe[col] == -1] = self.rupee_to_integer_median_dict[col]

    def data_correction_unknown(self, col):
        '''repace - with -99 and change datatype'''
        self.dataframe[col][self.dataframe[col] == "-"] = -99
        self.dataframe[col] = self.dataframe[col].astype("int64")

    def handle_missing_values(self):
        '''Handles Missing Values'''
        self.dataframe.select_dtypes(include='O').fillna('Unknown', inplace=True)
        self.dataframe.select_dtypes(include=[np.number]).fillna(-99, inplace=True)

    def preprocessing(self, training: bool = False):
        ''' Entire Preprocessing calls'''
        if training:
            self.dataset_info()
        self.rupee_to_integer('Average_Cost', training)
        self.rupee_to_integer('Minimum_Order', training)
        self.data_correction_unknown('Votes')
        self.data_correction_unknown('Reviews')
        self.dataframe['Rating'][self.dataframe['Rating'].isin(self.replace_values)] = -99
        self.dataframe['Rating'] = self.dataframe['Rating'].astype("float64")
        self.handle_missing_values()
