''' Feature Engineering Script'''

import itertools
import re
import pandas as pd
from category_encoders import OrdinalEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from data_preprocessing import DataPreprocessing


class FeatureExtraction:
    ''' Feature Extraction and Feature Encoding'''
    def __init__(self, data_preprocessing: DataPreprocessing):
        self.processing = data_preprocessing
        self.dataframe = pd.DataFrame()
        self.restaurants_count_dict = {}
        self.location_count_dict = {}
        self.new_restaurants_rating_dict = {}
        self.new_restaurants_votes_dict = {}
        self.new_restaurants_review_dict = {}
        self.cusine_list = []
        self.cusine_column_dict = {}
        self.cities_to_check = ['pune', 'mumbai', 'noida', 'delhi', 'kolkata', 'bangalore', 'gurgoan', 'hyderabad']
        self.ordinal_encoding_columns = ['Cuisines', 'Location', 'Restaurant', 'city']
        self.ordinal_encoder = OrdinalEncoder()
        self.label_encoder = LabelEncoder()
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None

    def one_hot_cusine(self, rows):
        ''' one hot enodinf for items list function'''
        rows = rows.split(", ")
        return_cusine_list = ([0]*len(self.cusine_list))
        for cusine in rows:
            if cusine in self.cusine_list:
                return_cusine_list[self.cusine_column_dict[cusine]] = 1
        return return_cusine_list

    def find_city_in_address(self, address):
        '''Return Cities Present Else Return Banglore'''
        present_city = "bangalore"
        for city in self.cities_to_check:
            if city in address.lower():
                present_city = city
        return present_city

    def restaurants_count(self, training: bool = False):
        '''Number of restaurants available at each location.'''
        if training:
            self.restaurants_count_dict = self.dataframe.groupby(['Location'])['Restaurant'].count()
        self.dataframe['restaraunt_counts'] = self.dataframe['Location'].map(self.restaurants_count_dict)

    def location_count(self, training: bool = False):
        '''Number of location served by each parent restaurants.'''
        if training:
            self.location_count_dict = self.DataFrameame.groupby(['Restaurant'])['Location'].count()
        self.dataframe['location_count'] = self.dataframe['Restaurant'].map(self.location_count_dict)

    def fill_new_restaurant_details(self, training: bool = False):
        ''' Many restaurants have No ratings, reviews and Votes here. # We can handle some them by copying data from parent restaurants.'''
        if training:
            self.new_restaurants_rating_dict = self.dataframe[['Restaurant', 'Rating']][self.dataframe['Rating'] != -99].groupby(['Restaurant'])['Rating'].mean()
            self.new_restaurants_votes_dict = self.dataframe[['Restaurant', 'Votes']][self.dataframe['Votes'] != -99].groupby(['Restaurant'])['Votes'].median()
            self.new_restaurants_review_dict = self.dataframe[['Restaurant', 'Reviews']][self.dataframe['Reviews'] != -99].groupby(['Restaurant'])['Reviews'].median()

        #Handling Ratings
        self.dataframe['Rating'][self.dataframe['Rating'] == -99] = self.dataframe['Restaurant'][self.dataframe['Rating'] == -99].map(self.new_restaurants_rating_dict).fillna(-99)
        #Handling Votes
        self.dataframe['Votes'][self.dataframe['Votes'] == -99] = self.dataframe['Restaurant'][self.dataframe['Votes'] == -99].map(self.new_restaurants_votes_dict).fillna(-99)
        #Handling Reviews
        self.dataframe['Reviews'][self.dataframe['Reviews'] == -99] = self.dataframe['Restaurant'][self.dataframe['Reviews'] == -99].map(self.new_restaurants_review_dict).fillna(-99)

    def cusine_varities(self, training: bool = False):
        '''Find number of Cusine Varites Available'''
        if training:
            self.cusine_list = list(set(list(itertools.chain.from_iterable(self.dataframe['Cuisines'].apply(lambda x: (x.split(", "))).to_list()))))
            for index, column in enumerate(self.cusine_list):
                self.cusine_list[index] = re.sub(r'[^\x00-\x7F]+', ' ', column)
                self.cusine_column_dict[column] = index

        self.dataframe[self.cusine_list] = pd.DataFrame(self.dataframe['Cuisines'].apply(self.one_hot_cusine).values.tolist(), index=self.dataframe.index)
        self.dataframe['Number_of_cusines_available'] = self.dataframe['Cuisines'].apply(lambda x: len(x.split(", ")))

    def encode_categorical_variables(self, training: bool = False):
        ''' Encoding input and target variable'''
        if training:
            self.dataframe[self.ordinal_encoding_columns] = self.ordinal_encoder.fit_transform(self.dataframe[self.ordinal_encoding_columns])
            self.dataframe['Delivery_Time'] = self.label_encoder.fit_transform(self.dataframe['Delivery_Time'])
        else:
            self.dataframe[self.ordinal_encoding_columns] = self.ordinal_encoder.transform(self.dataframe[self.ordinal_encoding_columns])
            self.dataframe['Delivery_Time'] = self.label_encoder.transform(self.dataframe['Delivery_Time'])

    def split_data(self, training: bool = False):
        ''' Split the data into train and test'''
        if training:
            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.dataframe, self.dataframe.Delivery_Time, test_size=0.001, random_state=1994)

        print(self.x_train.shape, self.x_test.shape)


    def feature_ext(self, training: bool = False):
        ''' Features Main Function'''
        self.processing.preprocessing(training)
        print("preprocessing completed")
        self.dataframe = self.processing.dataframe.copy()
        self.dataframe['city'] = self.dataframe['Location'].apply(self.find_city_in_address)
        self.restaurants_count(training)
        self.location_count(training)
        self.fill_new_restaurant_details(training)
        self.cusine_varities(training)
        self.dataframe['rid'] = self.dataframe['Restaurant'].str[3:].astype(int)
        self.encode_categorical_variables(training)
        self.split_data(training)
