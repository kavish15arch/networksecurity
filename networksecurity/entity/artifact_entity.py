from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file :str
    test_file:str


@dataclass
class DatvalidationArtifact:
    validation_status:bool
    valid_train_file_path:str
    invalid_train_file_path:str
    valid_test_file:str
    invalid_test_file:str
    drift_report_file:str

@dataclass
class DataTransformationArtifact:
    transformed_object_file:str
    transformed_train_file:str
    transformed_test_file: str
