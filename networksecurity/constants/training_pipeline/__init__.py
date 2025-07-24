from datetime import datetime
import os
import sys
import numpy as np


DATA_INGESTION_COLLECTION_NAME : str='NetworkData'
DATA_INGESTION_DATABASE_NAME : str='KAVISHOP'
DATA_INGESTION_DIR_NAME : str='data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR : str='feature_store'
DATA_INGESTION_INGESTED : str='ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float=0.2


TARGET_COLUMN : str='Result'
PIPELINE_NAME : str='NetworkSecurity'
ARTIFACT_DIR :str ='Artifacts'
FILE_NAME: str ='phishingData.csv'

TRAIN_FILE_NAME: str='train.csv'
TEST_FILE_NAME:str='test.csv'

SCHEMA_FILE_PATH=os.path.join('data_schema','schema.yaml')

'''

Constants Related to Data Validation
'''

DATA_VALIDATION_DIR_NAME:str='data_validation'
DATA_VALIDATION_VALID_DIR:str='validated'
DATA_VALIDATION_INVALID_DIR :str='invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR :str='drift_report'
DATA_VALIDATION_DRIFT_REORT_FILE_NAME :str='report.yaml'


'Constants related to data transformation'
DATA_TRANSFORMATION_DIR_NAME: str='data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str='transformed'
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str='transformed_object'
PREPROCESSING_OBJECT_FILE_NAME : str='preprocessor.pkl'


DATA_TRANSFORMATION_IMPUTER_PARAMS : dict={
    'missing_values': np.nan,
    'n_neighbors':3,
    'weights':'uniform'
}

MODEL_TRAINER_DIR_NAME :str ='model_trainer'
MODEL_TRAINER_TRAINED_MODEL_DIR: str ='trained_model'
MODEL_TRAINER_TRAINED_MODEL_NAME: str='model.pkl'
MODEL_TRAINER_EXPECTED_SCORE: float=0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD: float=0.05
SAVED_MODEL_DIR=os.path.join('saved_models')
MODEL_FILE_NAME= os.path.join('model.pkl')