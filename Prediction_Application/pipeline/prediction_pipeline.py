from tkinter import E
from Prediction_Application.components.data_validation import DataValidation
from Prediction_Application.logger import logging
from Prediction_Application.exception import ApplicationException
from Prediction_Application.logger import logging
from Prediction_Application.constant import *
from Prediction_Application.util.util import load_object, read_yaml_file, save_data
import os,sys
import pandas as pd
import numpy as np

class Prediction:

    def __init__(self, path=None):
        logging.info(f"\n{'*'*20} Prediction Pipeline Initiated {'*'*20}\n")
        self.path = path
        self.fe_obj = load_object(file_path=os.path.join(ROOT_DIR,PIKLE_FOLDER_NAME_KEY,"feat_eng.pkl"))
        self.preprocessing_obj = load_object(file_path=os.path.join(ROOT_DIR,PIKLE_FOLDER_NAME_KEY,"preprocessed.pkl"))
        self.model_obj = load_object(file_path=os.path.join(ROOT_DIR,PIKLE_FOLDER_NAME_KEY,"model.pkl"))
        if path is not None:
            logging.info(f"Predicting for filepath : [{self.path}]")

    def initiate_bulk_prediction(self):
        try:
            # Data Validation
            data_validation_status = True
            if data_validation_status:
                data_df = pd.read_csv(self.path)
                col = ['date','year','month','hour','season','weekday','is_holiday','working_day','casual','member','total_count',
                    'temp','r_temp','wind','humidity','weather_sit','is_covid']
                
                featured_eng_data = pd.DataFrame(self.fe_obj.transform(data_df),columns=col)
                
                date_cols = featured_eng_data.loc[:,['date','year','month','hour']]

                cols = ['date','year','month','hour','season','weekday','is_holiday','working_day','weather_sit','is_covid',
                'casual','member','total_count','temp','r_temp','wind','humidity']
                
                transformed_data = pd.DataFrame(np.c_[date_cols,self.preprocessing_obj.transform(featured_eng_data)],columns=cols)
                
                transformed_data.drop(columns=["year","casual","member"], inplace=True)
                transformed_data.set_index("date",inplace=True)

                prediction = self.model_obj.predict(transformed_data)
                data_df["predicted_demand"] = prediction

                output_folder_file_path = os.path.join(ROOT_DIR,"Output Folder","Predicted.csv")
                save_data(file_path=output_folder_file_path,data = data_df)
                return output_folder_file_path

        except Exception as e:
            raise ApplicationException(e,sys) from e 

    def initiate_single_prediction(self,data:dict):
        try:
            df = pd.DataFrame(data)
            prediction = self.model_obj.predict(self.preprocessing_obj.transform(df))
            return prediction
        except Exception as e:
            raise ApplicationException(e,sys) from e