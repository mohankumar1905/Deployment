import pandas as pd
import numpy as np
import re
from sklearn.base import BaseEstimator, TransformerMixin
from category_encoders import OrdinalEncoder
import itertools
from fooddelivery.datamanagement.errors import InvalidModelInputError

class FindCityinAddress(BaseEstimator, TransformerMixin):
    '''    Extract City from Address'''
    def __init__(self, cities_to_check, city_column = 'city', address_column = 'Location') -> None:
        if not isinstance(cities_to_check, list):
            self.cities_to_check = [cities_to_check]
        else:
            self.cities_to_check = cities_to_check
        self.city_column = city_column
        self.address_column = address_column

    def find_city_in_address(self, address):
        '''Return Cities Present, Else Return Banglore'''
        present_city = "bangalore"
        for city in self.cities_to_check:
            if city in address.lower():
                present_city = city
        return present_city
    
    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        '''Fit statement to accomodate the sklearn pipeline'''
        return self

    def transform(self, X: pd.DataFrame):
        '''Fill the median Value of Rupeee'''
        X = X.copy()
        X[self.city_column] = X[self.address_column].apply(self.find_city_in_address)
        return X

class CountAggregator(BaseEstimator, TransformerMixin):
    '''Number of restaurants available at each location.'''
    def __init__(self, aggregation_needed_columns: list):
        self.groupby_column = aggregation_needed_columns[0]
        self.grouping_column = aggregation_needed_columns[1]
        self.dervided_column = aggregation_needed_columns[2]
    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        '''Fit statement to accomodate the sklearn pipeline'''
        self.count_aggregator_dict = {}
        self.count_aggregator_dict = X.groupby([self.groupby_column])[self.grouping_column].count()
        return self
    def transform(self, X: pd.DataFrame):
        X = X.copy()
        X[self.dervided_column] = X[self.groupby_column].map(self.count_aggregator_dict)
        return X

class FillNewRestaurantDetails(BaseEstimator, TransformerMixin):
    ''' Many restaurants have No ratings, reviews and Votes here.
     # We can handle some them by copying data from parent restaurants.'''
    def __init__(self, variables, restaurant_column = 'Restaurant') -> None:
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables
        self.restaurant_column = restaurant_column
    
    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        '''Fit statement to accomodate the sklearn pipeline'''
        self.restaurant_dict = {}
        for column in self.variables:
            self.restaurant_dict[column] = X[X[column] != -99].groupby([self.restaurant_column])[column].mean()
        return self
    def transform(self, X: pd.DataFrame):
        X = X.copy()
        for column in self.variables:
            if len(X[column][X[column]<0]):
                raise InvalidModelInputError(f"Variables contain zero or negative values in the column: {column}")
            X[column][X[column] == -99] = X[self.restaurant_column][X[column] == -99].map(self.restaurant_dict[column])
            X[column].fillna(-99, inplace=True)
        return X

class CusineVarities(BaseEstimator, TransformerMixin):
    ''' Feature Engineering of Cusine Varities Column'''
    def __init__(self, variable, cusine_count_variable = 'Number_of_cusines_available'):
        self.variable = variable
        self.cusine_count_variable = cusine_count_variable

    def one_hot_cusine(self, rows):
        ''' one hot enodinf for items list function'''
        rows = rows.split(", ")
        return_cusine_list = ([0]*len(self.cusine_list))
        for cusine in rows:
            if cusine in self.cusine_list:
                return_cusine_list[self.cusine_column_dict[cusine]] = 1
        return return_cusine_list

    def fit(self, X: pd.DataFrame, y: pd.Series):
        ''' Taking Cusine Column List'''
        self.cusine_column_dict = {}
        self.cusine_list = list(set(list(itertools.chain.from_iterable(X[self.variable].apply(lambda x: (x.split(", "))).to_list()))))
        for index, column in enumerate(self.cusine_list):
            self.cusine_list[index] = re.sub(r'[^\x00-\x7F]+', ' ', column)
            self.cusine_column_dict[column] = index
        return self
    def transform(self, X: pd.DataFrame):
        X  = X.copy()
        X[self.cusine_list] = pd.DataFrame(X[self.variable].apply(self.one_hot_cusine).values.tolist(), index=X.index)
        X[self.cusine_count_variable] = X[self.variable].apply(lambda x: len(x.split(", ")))
        return X


class EncodeCategoricalVariables(BaseEstimator, TransformerMixin):
    ''' Encoding input and target variable'''
    def __init__(self, variables):
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables
        self.ordinal_encoder = OrdinalEncoder()

    def fit(self, X: pd.DataFrame, y: pd.Series):
        '''fit categorical Variables'''
        self.ordinal_encoder.fit(X[self.variables])
        for column in X.columns:
            if X[column].isna().any():
                raise InvalidModelInputError(f"Variables: {column} contains Null values")
        return self
    
    def transform(self, X: pd.DataFrame):
        '''Both Label and Categorical Encoding Transformations'''
        X = X.copy()
        X[self.variables] = self.ordinal_encoder.transform(X[self.variables])
        return X