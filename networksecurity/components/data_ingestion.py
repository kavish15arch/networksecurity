import os
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pymongo
from typing import List
from dotenv import load_dotenv
load_dotenv()

MONGODB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise e
        
    def collect_as_dataframe(self):# this func is made to read values from mongo db as a data frame
        try:
            database_name=self.data_ingestion_config.database_name

            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGODB_URL)
            collection=self.mongo_client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))

            if '_id' in df.columns.to_list():# Mongo db adds _id to every feature to remove it we did this
                df.drop(columns=['_id'],axis=1)

                df = df.replace({'na': np.nan})
                return df
        except Exception as e:
            raise e
    def storing_mongo_data_locally(self,dataframe:pd.DataFrame):#created to store the mongo db file to in system itself 
        try:
         feature_file_path=self.data_ingestion_config.feature_store_file_path
         dir_path=os.path.dirname(feature_file_path)
         os.makedirs(dir_path,exist_ok=True)
         dataframe.to_csv(feature_file_path, index=False,header=True)
         return dataframe
        except Exception as e:
            raise e
        
    def training_and_test_split(self, dataframe:pd.DataFrame):
        try:
         train_set , test_set=train_test_split(dataframe,test_size=0.2)
         dir_path=os.path.dirname(self.data_ingestion_config.train_data_file_path)
         os.makedirs(dir_path, exist_ok=True)

         train_set.to_csv(self.data_ingestion_config.train_data_file_path,index=False,header=True)

         test_set.to_csv(self.data_ingestion_config.test_data_file_path,index=False,header=True)
        except Exception as e:
            raise e


        
    def initiate_data_ingestion(self):
        try:
            dataframe=self.collect_as_dataframe()
            dataframe=self.collect_as_dataframe()
            self.training_and_test_split(dataframe)
            dataingestionartifact=DataIngestionArtifact(train_file=self.data_ingestion_config.train_data_file_path,test_file=self.data_ingestion_config.test_data_file_path)
            return dataingestionartifact
        except Exception as e:
            raise e


