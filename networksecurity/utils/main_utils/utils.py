import yaml
import os
import sys
#import dill
import numpy as np
import pickle


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
    
def save_object(file_path , obj):
    try:
        os.makedirs(os.path.dirname(file_path) , exist_ok=True)
        with open(file_path  , 'wb') as file:
            pickle.dump(obj , file)
    except Exception as e:
        raise e