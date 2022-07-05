
from Prediction_Application.logger import logging
from Prediction_Application.exception import ApplicationException
from Prediction_Application.components.data_ingestion import DataIngestion
from Prediction_Application.components.data_validation import DataValidation
from Prediction_Application.components.data_transformation import DataTransformation
from Prediction_Application.config.configuration import Configuration
from Prediction_Application.entity.config_entity import DataIngestionConfig
from Prediction_Application.entity.artifact_entity import DataIngestionArtifact,DataTransformationArtifact,DataValidationArtifact
import os,sys




class Training_Pipeline:

    def __init__(self,config: Configuration=Configuration())->None:
        try:
            self.config = config
        except Exception as e:
            raise ApplicationException(e,sys) from e

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise ApplicationException(e,sys) from e

    def run_training_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise ApplicationException(e,sys) from e

