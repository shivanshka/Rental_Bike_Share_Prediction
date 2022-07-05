from Prediction_Application.components.data_ingestion import DataIngestion
from Prediction_Application.components.data_validation import DataValidation
from Prediction_Application.components.data_transformation import DataTransformation
import pickle
from Prediction_Application.logger import logging



class Prediction:

    def __init__(self, path=None):
        self.path = path

    def initiate_bulk_prediction(self):
        pass

    def initiate_single_prediction(self,data):
        pass