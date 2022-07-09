from Prediction_Application.exception import ApplicationException
import pymongo
import pandas as pd
import os,sys
from Prediction_Application.constant import *
from Prediction_Application.exception import ApplicationException
from Prediction_Application.logger import logging

class MongoDB:
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(DATABASE_CLIENT_URL_KEY,tls=True,tlsAllowInvalidCertificates=True)

            logging.info("Connection with DB created successfully!!!")                                
            self.db= self.client[DATABASE_NAME_KEY]
            self.collection_name= DATABASE_COLLECTION_NAME_KEY
        except Exception as e:
            raise ApplicationException(e,sys) from e

    def create_and_check_collection(self,coll_name:str = None)->None:
        try:
            
            if coll_name is None:
                # Checking whether the main collection already exist or not, if does then delete it
                if self.collection_name in self.db.list_collection_names():
                    self.db.drop_collection(self.collection_name)

                # Creating new main collection
                self.collection = self.db[self.collection_name]
                
            if coll_name == "Training" or coll_name == "Test":
                # Checking whether the training/test collection already exist or not, if does then delete it
                if coll_name in self.db.list_collection_names():
                    self.db.drop_collection(coll_name)

                self.collection = self.db[coll_name]
                
        except Exception as e:
            raise ApplicationException(e,sys) from e

    def insertall(self,data_dict:dict)-> None:
        try:
            logging.info(f"Inserting data into database:[{DATABASE_NAME_KEY}] in collection: [{self.collection_name}]")
            self.collection.insert_many(data_dict)
            logging.info("Insertion into DB is successful!!! ")
        except Exception as e:
            raise ApplicationException(e,sys) from e

    def fetch_df(self,coll_name:str = None )->pd.DataFrame:
        try:
            if coll_name is None:
                self.collection = self.db[self.collection_name]
                dataframe = pd.DataFrame(self.collection.find())

            if coll_name == "Training" or coll_name == "Test":
                self.collection = self.db[coll_name]
                dataframe = pd.DataFrame(self.collection.find())

            logging.info(f"Data Fetched from collection: [{coll_name}] successfully!!!")

            return dataframe

        except Exception as e:
            raise ApplicationException(e,sys) from e