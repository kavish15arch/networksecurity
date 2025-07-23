import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()

MONGODB_URL=os.getenv('MONGO_DB_URL')
print(MONGODB_URL)

import certifi

ca=certifi.where() # This module is used to certifi at root level which is important for http verification

import pymongo
import pandas as pd
import numpy as np


class NetworkSecurity:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise e
        
    def csv_to_json(self, file_path):
        try:
          data=pd.read_csv(file_path)
          data.reset_index(drop=True , inplace=True)
          record=list(json.loads(data.T.to_json()).values())#.T is means traanspose json.loads converts json into python dictionaries
          return record
        
        except Exception as e:
            raise e
    
    def insert_to_pymongo(self,record, data_base,collections):
        try:
         self.record=record
         self.data_base=data_base
         self.collections=collections

         self.pymongo_client=pymongo.MongoClient(MONGODB_URL)
         self.data_base=self.pymongo_client[self.data_base]
         self.collections=self.data_base[self.collections]
         self.collections.insert_many(self.record)
         return len(self.record)
        
        except Exception as e:
           raise e


if __name__=='__main__':
   filepath='Network_data\phisingData.csv'
   database='KAVISHOP'
   Collections='NetworkData'
   network_obj=NetworkSecurity()
   records=network_obj.csv_to_json(file_path=filepath)
   print(records)
   networkrecords=network_obj.insert_to_pymongo(record=records,data_base=database,collections=Collections)
   print(networkrecords)
