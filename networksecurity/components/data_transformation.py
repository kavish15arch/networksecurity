import sys, os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constants.training_pipeline import TARGET_COLUMN
from networksecurity.constants.training_pipeline  import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import (DataTransformationArtifact,DatvalidationArtifact)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import save_as_numpy_array , save_object


class DataTransformation:
    def __init__(self, data_validation_artifact:DatvalidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact : DatvalidationArtifact=data_validation_artifact
            self.data_transforamtion_config : DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise e
        
    @staticmethod
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise e
        
    def using_knn_imputer(self):
        imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS) #** is used for tellingn python that we are using key value pairs

        processor=Pipeline([('imputer',imputer)])
        return processor
        
    def initiate_data_transformation(self):
        try:
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file)
            
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)


            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)
            input_feature_train_df = input_feature_train_df.select_dtypes(include=['number'])
            input_feature_test_df = input_feature_test_df.select_dtypes(include=['number'])



            preprocessor=self.using_knn_imputer()
            preprocessing_obj=preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature=preprocessing_obj.transform(input_feature_train_df)
            transformed_input_test_feature=preprocessing_obj.transform(input_feature_test_df)
            
            train_arr=np.c_[transformed_input_train_feature , np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_input_test_feature , np.array(target_feature_test_df)]

            ## saving the numoy arrays
            save_as_numpy_array(self.data_transforamtion_config.transformed_train_file_path , array=train_arr)
            save_as_numpy_array(self.data_transforamtion_config.transformed_test_file_path , array=test_arr)
            save_object(file_path=self.data_transforamtion_config.transformed_object_file_path, obj=preprocessing_obj)

            save_object('final_models/preprocesror.pkl' , preprocessing_obj)


            ## creating the artifacts
            data_transformation_artifacts=DataTransformationArtifact(self.data_transforamtion_config.transformed_object_file_path , self.data_transforamtion_config.transformed_train_file_path,self.data_transforamtion_config.transformed_test_file_path)
            return data_transformation_artifacts      
        except Exception as e:
            raise e
        


        