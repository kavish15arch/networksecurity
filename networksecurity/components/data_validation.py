from networksecurity.entity.config_entity import DataIngestionConfig , DataValidationConfig
from scipy.stats import ks_2samp
from networksecurity.entity.artifact_entity import DatvalidationArtifact,DataIngestionArtifact
import pandas as pd
import os , sys
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file , write_yaml_file



class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_file=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise e
        
    @staticmethod

    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise e
    

       
    def validate_no_columns(self , dataframe:pd.DataFrame)-> bool:
        no_of_columns=len(self._schema_file)
        if len(dataframe.columns)==no_of_columns:
            return True
        else: 
            return False
        
    def checking_drift_report(self,base_df,current_df,threshold=0.05):
        try:
            report={}
            status=True
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]

                checking=ks_2samp(d1,d2)
                if checking.pvalue >= threshold:
                    is_found=False
                    status=False

                else:
                    is_found=True
                
                report.update({column:{
                    'p_value':float(checking.pvalue),
                    'drift_status':is_found
                }}

                )
                ## making the file  in which report will be written
            drift_report_file=self.data_validation_config.drift_report_file_path
            dir_path=os.path.dirname(drift_report_file)
            os.makedirs(dir_path , exist_ok=True)
            ## Writing the report in the file
            write_yaml_file(file_path=drift_report_file , content=report)
        except Exception as e:
            raise e


        
        



        
    def initiate_data_validatin(self)->DatvalidationArtifact:
       try:
           trained_file_path=self.data_ingestion_artifact.train_file
           test_file_path=self.data_ingestion_artifact.test_file

           ## Validating test and train data
           train_data_frame=DataValidation.read_data(trained_file_path)
           test_data_frame=DataValidation.read_data(test_file_path)

           ## Validating number of columns
           df = self.read_data(trained_file_path)  # Convert file path → DataFrame
           status = self.validate_no_columns(dataframe=df)
           if not  status:
               error_mesasge={'Train data frame does not contain all the columns'}
           status=self.validate_no_columns(dataframe=test_data_frame)
           if not status:
               error_mesasge={'Test data frame does not contain all the columns'}

           ## drift report
           status=self.checking_drift_report(base_df=train_data_frame, current_df=test_data_frame)
           dir_path=os.path.dirname(self.data_validation_config.valid_train_file)
           os.makedirs(dir_path , exist_ok=True)

           train_data_frame.to_csv(self.data_validation_config.valid_train_file, index=False , header=True)
           test_data_frame.to_csv(self.data_validation_config.valid_test_file)


           data_validation_artifact=DatvalidationArtifact(
               validation_status=status,
               valid_train_file_path=self.data_ingestion_artifact.train_file,
               valid_test_file=self.data_ingestion_artifact.test_file,
               invalid_train_file_path=None,
               invalid_test_file=None,
               drift_report_file=self.data_validation_config.drift_report_file_path)

               
           return data_validation_artifact
       except Exception as e:
           raise e

