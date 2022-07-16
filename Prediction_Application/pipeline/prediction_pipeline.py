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
                data_df['total_count'] = 0
                col = ['date','year','month','hour','season','weekday','is_holiday','working_day','total_count',
                    'temp','wind','humidity','weather_sit','is_covid']
                
                featured_eng_data = pd.DataFrame(self.fe_obj.transform(data_df),columns=col)
                featured_eng_data.drop(columns="total_count", inplace=True)
                
                date_cols = featured_eng_data.loc[:,['date','year','month','hour']]

                cols = ['date','year','month','hour','season','weekday','is_holiday','working_day','weather_sit',
                'is_covid','temp','wind','humidity']
                data_df = data_df[~data_df.duplicated(subset=["date","month","hour"],keep='last')]

                transformed_data = pd.DataFrame(np.c_[date_cols,self.preprocessing_obj.transform(featured_eng_data)],columns=cols)
                
                transformed_data.drop(columns=["year"], inplace=True)
                transformed_data.set_index("date",inplace=True)
                transformed_data=transformed_data.infer_objects()

                prediction = self.model_obj.predict(transformed_data)
                data_df["predicted_demand"] = prediction

                output_folder_file_path = os.path.join(ROOT_DIR,"Output Folder",CURRENT_TIME_STAMP,"Predicted.csv")
                save_data(file_path=output_folder_file_path,data = data_df)
                return output_folder_file_path

        except Exception as e:
            raise ApplicationException(e,sys) from e 

    def initiate_single_prediction(self,data:dict)->int:
        try:
            df = pd.DataFrame([data])
            date_cols = df.loc[:,["date","month","hour"]]
            preprocessed_df = pd.DataFrame(np.c_[date_cols,self.preprocessing_obj.transform(df.drop(columns=["date","month","hour"]))],
            columns=df.columns)
            preprocessed_df.set_index("date",inplace=True)
            preprocessed_df = preprocessed_df.infer_objects()
            prediction = self.model_obj.predict(preprocessed_df)
            return round(prediction[0])
        except Exception as e:
            raise ApplicationException(e,sys) from e

if __name__=="__main__":
    path = r"G:\Shivansh\iNeuron\Internship\Rental Bike Share Prediction\New folder\Testing_data.csv"
    pred = Prediction(path)
    print(pred.initiate_bulk_prediction())