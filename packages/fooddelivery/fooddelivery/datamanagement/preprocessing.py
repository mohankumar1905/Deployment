import pandas as pd
import numpy as np
import re
from sklearn.base import BaseEstimator, TransformerMixin
import itertools
from fooddelivery.datamanagement.errors import InvalidModelInputError

class DataCorrection(BaseEstimator, TransformerMixin):
    '''Remove -(hyphens) from data after changing datatype and replace the null with -99'''
    def __init__(self, variables=None, values_to_replace=None) -> None:
        ''' Initialize and Convert if not a list'''
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

        if not isinstance(values_to_replace, list):
            self.values_to_replace = [values_to_replace]
        else:
            self.values_to_replace = values_to_replace

    def fit(self, X: pd.DataFrame, y: pd.Series):
        '''Fit statement to accomodate the sklearn pipeline'''
        return self

    def transform(self, X: pd.DataFrame):
        '''Change the Dataype to Numeric'''
        X = X.copy()
        for col in self.variables:
            X[col] = X[col].apply(lambda x: re.sub("[^0-9.]", "", str(x)))
            X[col][X[col].isin(self.values_to_replace)] = -99
            X[col] = pd.to_numeric(X[col])
        return X

class CategoricalMedianImputation(BaseEstimator, TransformerMixin):
    ''' Converts Rupee to Integer'''
    def __init__(self, variables=None) -> None:
        ''' Initialize and Convert if not a list'''
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        '''Fit statement to accomodate the sklearn pipeline'''
        self.median_dict = {}
        for col in self.variables: 
            self.median_dict[col] = X[col].median()
        return self

    def transform(self, X: pd.DataFrame):
        '''Median Impuation'''
        X = X.copy()
        for col in self.variables:
            X[col][X[col] == -99] = self.median_dict[col]
        return X

class HandleNumericalMissingValues(BaseEstimator, TransformerMixin):
    ''' Handles Missing Values of all the Columns'''
    def __init__(self, variables) -> None:
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables
    
    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        '''Fit statement to accomodate the sklearn pipeline'''
        return self

    def transform(self, X: pd.DataFrame):
        '''Fill the median Value of Rupeee'''
        X = X.copy()
        for col in self.variables:
            X[col].fillna(-99, inplace=True)
            return X

class HandleCategoricalMissingValues(BaseEstimator, TransformerMixin):
    ''' Handles Missing Values of all the Columns'''
    def __init__(self, variables) -> None:
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables
    
    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        '''Fit statement to accomodate the sklearn pipeline'''
        return self

    def transform(self, X: pd.DataFrame):
        '''Fill the Unknown Value of Rupeee'''
        X = X.copy()
        for col in self.variables:
            X[col].fillna("Unknown", inplace=True)
        return X


