from imblearn.pipeline import Pipeline
import pandas as pd
from category_encoders import OrdinalEncoder
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler
from lightgbm import LGBMClassifier
from fooddelivery.datamanagement import preprocessing as pp
from fooddelivery.datamanagement import feature_extraction as fx
from fooddelivery.config import config as cg
import logging
_logger = logging.getLogger(__name__)
pd.options.mode.chained_assignment = None

food_delivery_pipe = Pipeline(
	[('data_correction',  pp.DataCorrection(variables=cg.DATA_CORRECTION_VARIABLES, values_to_replace=cg.VALUES_TO_REPLACE)),
	('median_imputation', pp.CategoricalMedianImputation(variables=cg.MEDIAN_IMPUTATION_VARIABLES)),
	('numerical_null_handling', pp.HandleNumericalMissingValues(variables=cg.NULL_HANDLING_NUMERICAL_COLUMNS)),
	('categorical_null_handling', pp.HandleCategoricalMissingValues(variables=cg.NULL_HANDLING_CATEGORICAL_COLUMNS)),
	('extract_city', fx.FindCityinAddress(cities_to_check=cg.CITIES_TO_CHECK)),
	('restaurants_count', fx.CountAggregator(aggregation_needed_columns=cg.RESTAURANT_AGG_COLOUMNS)),
	('location_count', fx.CountAggregator(aggregation_needed_columns=cg.LOCATION_AGG_COLOUMNS)),
	('inherit_old_restaurant_info', fx.FillNewRestaurantDetails(variables=cg.INHERITING_INFO_COLUMNS)),
	('extract_cusine_varities_info', fx.CusineVarities(variable=cg.CUSINE_VARIABLE)),
	('encoding', fx.EncodeCategoricalVariables(variables=cg.ORDINAL_ENCODING_COLUMNS)),
	('random_over_sampling', RandomOverSampler(random_state=1994)),
	('lightgbm', LGBMClassifier(n_estimators = 3000, random_state = 1994, nfold = 5, learning_rate = 0.03,
 colsample_bytree = 0.2, objective = 'multiclass', verbose=100))
	])