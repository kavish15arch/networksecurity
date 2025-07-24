import yaml
import os
import sys
#import dill
import numpy as np
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path , 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise e    
    
def write_yaml_file(file_path:str , content:object , replace:bool=False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        else:
            os.makedirs(os.path.dirname(file_path ),exist_ok=True)
            with open(file_path , 'w') as file:
                yaml.dump(content, file)
    except Exception as e:
        raise e
    
def save_as_numpy_array(file_path,array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path , 'wb') as file:
            np.save(file , array)
    except Exception as e:
        raise e
    
def save_object(file_path, obj):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    joblib.dump(obj, file_path)
 
    
import joblib
import os

def load_object(file_path):
    if not os.path.exists(file_path):
        raise Exception(f"The file {file_path} does not exist")
    return joblib.load(file_path)

       
    
    

def load_numpy_array_data(file_path):
    try:
        with open(file_path , 'rb') as file:
            return np.load(file) 
    except Exception as e:
        raise e
    
def evaluate_models(x_train , y_train , x_test , y_test, models, params):
    try:
        report={}
        for i in range(len(list(models))):
            model=list(models.values())[i]
            para=params[list(models.keys())[i]]

            gs=GridSearchCV(model , para , cv=3)
            gs.fit(x_train , y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)

            if len(x_train.shape)==1:
                x_train=x_train.reshape(-1,1)
            if len(x_test.shape)==1:
               x_test= x_test.reshape(-1,1)

            print('x_train shape' , x_train.shape)
            print('x_test shape', x_test.shape)

            y_train_pred=model.predict(x_train)
            y_test_pred=model.predict(x_test)

            train_model_score=r2_score(y_train , y_train_pred)
            test_model_score=r2_score(y_test , y_test_pred)

            report[list(models.keys())[i]]= test_model_score

            return report
    
    except Exception as e:
        raise e

