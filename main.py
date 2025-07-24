from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig , DataValidationConfig , DataTransformationConfig , ModelTrainerConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

if __name__ == "__main__":
    try:
        print("Starting main.py...")
        trainingpipelineconfig = TrainingPipelineConfig()
        print("Training config created.")
        
        a = DataIngestionConfig(trainingpipelineconfig)
        print("DataIngestionConfig created.")
        
        data_ingestion = DataIngestion(a)
        print("DataIngestion instance created.")
        
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        print("Data ingestion completed.")
        
        print(dataingestionartifact)
        datavalidationconfig=DataValidationConfig(trainingpipelineconfig)
        data_validation= DataValidation(dataingestionartifact,datavalidationconfig)
        data_validation_artifact= data_validation.initiate_data_validatin()
        print(data_validation_artifact)

        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        data_transformartion=DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=data_transformation_config)
        data_transformation_artifact=data_transformartion.initiate_data_transformation()
        print(data_transformation_artifact)

        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config , data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        print(model_trainer_artifact)



    except Exception as e:
        print("An error occurred:")
        print(e)
        raise e
