from networksecurity.constants.training_pipeline import SAVED_MODEL_DIR ,MODEL_FILE_NAME

import os
import sys


class NetworkModel:
    def __init__(self, preprocessor , model):
        try:
            self.prepprocessor=preprocessor
            self.model=model
        except Exception as e:
            raise e
        
    

    def predict(self, x):
        try:
            x_transform=self.prepprocessor.transform(x)
            y_pred=self.model.predict(x_transform)
            return y_pred
        except Exception as e:
            raise e