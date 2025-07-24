import os , sys
from networksecurity.entity.artifact_entity import DataTransformationArtifact , ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.utils.main_utils.utils import save_as_numpy_array , save_object , load_object , load_numpy_array_data , evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier)
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise e
    

    def train_model(self,x_train, y_train, x_test , y_test):
        models={
            'Random forest': RandomForestClassifier(),
            'Decision Tree': DecisionTreeClassifier(),
            'gradient boosting':GradientBoostingClassifier(),
            'logistic regression':LogisticRegression(),
            'Adaboost':AdaBoostClassifier()
        }

        params={
            'Decision Tree':{
                'criterion':['gini' 'entropy' 'log_loss'],
                'splitter':['best','random'],
                'max_features':['sqrt','log2']
            },

            'gradient boosting':{
                'loss':['log_loss','exponential'],
                'learning_rate':[0.1, 0.01, 0.001 , 0.5],
                'criterion':['friedman_mse','squared_error']
            },
            'logistic regression':{
                'penalty': ['l1','l2','elasticnet',None]
                
            },
            'Random forest':{
                'criterion':['gini' ,'entropy', 'log_loss'],
                'max_features':['sqrt','log2']

            },
            'Adaboost':{
                'n_estimators':[8,16,32,64,256,128],
                'learning_rate':[0.1, 0.01, 0.001 , 0.5],
                
            }

        }

        model_report=evaluate_models(x_train=x_train , y_train=y_train , x_test=x_test , y_test=y_test , models=models, params=params)
        best_model_score=max(model_report.values())

        best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        best_model=models[best_model_name]

        y_train_pred=best_model.predict(x_train)

        classification_train_metric=get_classification_score(y_true= y_train  , y_pred=y_train_pred)

        y_test_pred=best_model.predict(x_test)

        classification_test_metric=get_classification_score(y_true=y_test , y_pred=y_test_pred)
        
        ## calling preprocessor.pkl wali file
        preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file)
        
        ## making file where model.pkl will be saved
        model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path , exist_ok=True)

        Network_model=NetworkModel(preprocessor=preprocessor , model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path , obj=NetworkModel)

        save_object('final_models/model.pkl',best_model)


        model_trainer_artifact=ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            trained_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric

        )
        return model_trainer_artifact
    
        

        

        
    def initiate_model_trainer(self):
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file
            test_file_path=self.data_transformation_artifact.transformed_test_file

            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)

            x_train , y_train, x_test ,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model_trainer_artifact=self.train_model(x_train , y_train,x_test,y_test)
            return model_trainer_artifact

        except Exception as e:
            raise e
        

        


