from ast import expr_context
from Prediction_Application.logger import logging
from Prediction_Application.exception import ApplicationException
from Prediction_Application.entity.config_entity import DataIngestionConfig
from Prediction_Application.entity.artifact_entity import DataIngestionArtifact
#import pandas as pd
#import numpy as np
import os,sys
import zipfile
from six.moves import urllib



class DataIngestion:
    def __init__(self,data_ingestion_config : DataIngestionConfig):
        try:
            logging.info(f"{'*'*20} Data Ingestion log started {'*'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise ApplicationException(e,sys) from e

    def download_data(self):
        """
        Downloads the zipped dataset from the given url and save it to the specified path.
        """
        try:
            # Extracting remote url to download dataset files
            download_url = self.data_ingestion_config.dataset_download_url

            # folder location to download zipped file
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir

            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)
            os.makedirs(tgz_download_dir,exist_ok=True)

            #file_name = os.path.basename(download_url)
            file_name = "rental_bike_data.zip"
            tgz_file_path = os.path.join(tgz_download_dir,file_name)

            logging.info(f"Downloading file from: [{download_url}] into : [{tgz_file_path}]")
            urllib.request.urlretrieve(download_url,tgz_file_path)
            logging.info(f"File: [{tgz_file_path}] has been downloaded successfully")

            return tgz_file_path

        except Exception as e:
            raise ApplicationException(e,sys) from e

    def extract_tgz_file(self,tgz_file_path:str):
        try:
            # Folder location to extract the downloaded zipped dataset files
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
            os.makedirs(raw_data_dir,exist_ok=True)

            logging.info(f"Extracting zipped file : [{tgz_file_path}] into dir: [{raw_data_dir}]")
            # Extarcting the files from zipped file
            zip_ref = zipfile.ZipFile(tgz_file_path)
            zip_ref.extractall(raw_data_dir)
            zip_ref.close()

            logging.info("Extraction completed successfully")

        except Exception as e:
            raise ApplicationException(e,sys) from e

    def data_merge_and_split(self):
        try:
            data_ingestion_artifact = DataIngestionArtifact()
            return data_ingestion_artifact
        except Exception as e:
            raise ApplicationException(e,sys) from e
    
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            tgz_file_path = self.download_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            #return self.data_merge_and_split()
        except Exception as e:
            raise ApplicationException(e,sys) from e
    
    def __del__(self):
        logging.info(f"{'*'*20} Data Ingestion log completed {'*'*20}")

