from Prediction_Application.logger import logging
from Prediction_Application.exception import ApplicationException
from Prediction_Application.entity.config_entity import DataTransformationConfig
from Prediction_Application.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from Prediction_Application.constant import *
from Prediction_Application.util.util import read_yaml_file, save_data,save_object
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import os,sys
import pandas as pd
import numpy as np
import re



class Feature_Engineering(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        """
        This class applies necessary Feature Engneering for Rental Bike Share Data
        """
        logging.info(f"\n{'*'*20} Feature Engneering Started {'*'*20}\n\n")
        
        
    def wind_clean(self,x):
        pat = pat = "[\d]+"
        if x=="Calm":
            num = 0
        elif x!= " " and "°" in x:
            num= re.findall(pat,x)[1]
        elif "°" not in x:
            num= re.findall(pat,x)[0]
        return num

    def desc_filter(self,x):
        """
        Function to return a string with words mentioned in conditions list below.
        """
        conditions = ["Clear", "Cloudy","Broken","Few","Scattered","Haze","Fog","Drizzle",
                      "Snowfall","Light","Rain","Thunderstorm","Heavy"]
        desc = []
        if x != np.nan:    
            for i in str(x).split():
                if i in conditions:
                    desc.append(i)
            return " ".join(desc)

    def data_clean(self,data):
        try:
            # Renaming columns
            data = data.rename(columns={"temperature(in celcius)":"temp",
                        "relative_temperature(in celcius)":"r_temp",
                        "wind_speed(in kmph)":"wind",
                        "humidity(in %)":"humidity"})
            
            # Cleaning the columns for model building
            data["temp"] = data["temp"].apply(lambda x: x.strip("°C"))
            data["r_temp"] = data["r_temp"].apply(lambda x: x.strip("°C"))
            data["humidity"] = data["humidity"].apply(lambda x: x.strip("%"))
            data["wind"] = data["wind"].apply(self.wind_clean)
            data["description"] = data["description"].apply(self.desc_filter)
            
            # Converting Datatype of required columns
            for feature in data.columns:
                if data[feature].dtypes == 'O' and feature not in ["date","season","description"]:
                    data[feature] = data[feature].astype("float")
                    
            data["casual"] = data["casual"].astype("int64")
            data["member"] = data["member"].astype("int64")
            
            data["date"] = pd.to_datetime(data["date"])
            data.sort_values(by=['date', "hour"], ascending=True, inplace=True)
            
            # Removing the duplicate rows from dataset
            data = data[~data.duplicated(subset=["date","month",
            "hour","season","weekday","is_holiday","working_day"],keep="last")].reset_index(drop=True)
            return data
        except Exception as e:
            raise ApplicationException(e,sys) from e
        
        
    def create_weather_situation(self,x):
        """
        Function to clean weather description column and label encode it.
        """
        if ("Few" in x) or ("Clear" in x) or ("Drizzle" in x) :
            return int(1)
        elif ("Broken" in x) or ("Haze" in x) or ("Cloudy" in x):
            return int(2)
        elif ("Light Rain" in x) or ("Snowfall" in x) or ("Scattered" in x):
            return int(3)
        elif ("Heavy" in x) or ("Thunderstorm" in x) or ("Fog" in x):
            return int(4)
    
    def create_covid_period(self,x):
        """
        Function to check whether given year is covid year or not.
        """
        if (x == 2020) or (x == 2021):
            return 1
        else:
            return 0

        
    def fit(self,X,y=None):
        return self
    
    def transform(self,X,y=None):
        try:
            X = self.data_clean(X)

            # Label Encoding the 'season' column
            season_dict = {"winter":1, "spring":2, "summer":3, "fall":4}
            X["season"] = X["season"].map(season_dict)

            # Label Encoding the 'weather description' and creating new column 'weather_sit' from it
            weather_sit = X["description"].apply(self.create_weather_situation)
            is_covid = X["year"].apply(self.create_covid_period)
            # Dropping the 'description' column
            X.drop(columns = ["casual","member","r_temp","description"],inplace = True)

            # Merging the above two new column to the passed Dataset
            generated_feature = np.c_[X,weather_sit,is_covid]
            return generated_feature

        except Exception as e:
            raise ApplicationException(e,sys) from e



class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig,
                    data_ingestion_artifact: DataIngestionArtifact,
                    data_validation_artifact: DataValidationArtifact):
        try:
            logging.info(f"\n{'*'*20} Data Transformation log started {'*'*20}\n\n")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact

        except Exception as e:
            raise ApplicationException(e,sys) from e

    def get_feature_engineering_object(self):
        try:
            feature_engineering = Pipeline(steps = [("fe",Feature_Engineering())])
            return feature_engineering
        except Exception as e:
            raise ApplicationException(e,sys) from e

    def get_data_transformer_object(self):
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path

            dataset_schema = read_yaml_file(file_path=schema_file_path)

            date_columns = dataset_schema[DATE_COLUMN_KEY]
            numerical_columns = dataset_schema[NUMERICAL_COLUMN_KEY] 
            categorical_columns = dataset_schema[CATEGORICAL_COLUMN_KEY]

            all_columns = date_columns+numerical_columns+categorical_columns

            num_pipeline = Pipeline(steps =[("impute", SimpleImputer(strategy="median")),
                                            ("scaler",StandardScaler())])

            cat_pipeline = Pipeline(steps = [("impute", SimpleImputer(strategy="most_frequent")),
                                             ])

            preprocessing = ColumnTransformer([('cat_pipeline',cat_pipeline, categorical_columns),
                                               ('num_pipeline',num_pipeline,numerical_columns)])

            return preprocessing
        except Exception as e:
            raise ApplicationException(e,sys) from e    
    
    
    def initiate_data_transformation(self):
        try:
            logging.info(f"Obtaining training and test file path.")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            logging.info(f"Loading training and test data as pandas dataframe.")
            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)

            # Reading schema file for columns details
            schema_file_path = self.data_validation_artifact.schema_file_path
            schema = read_yaml_file(file_path=schema_file_path)

            # Extracting target column name
            target_column_name = schema[TARGET_COLUMN_KEY]

            

            logging.info(f"Obtaining feature engineering object.")
            fe_obj = self.get_feature_engineering_object()

            date_columns = schema[DATE_COLUMN_KEY]
            numerical_columns = schema[NUMERICAL_COLUMN_KEY] 
            categorical_columns = schema[CATEGORICAL_COLUMN_KEY]

            all_columns = date_columns+categorical_columns+numerical_columns
            col = ['date','year','month','hour','season','weekday','is_holiday','working_day','total_count',
                    'temp','wind','humidity','weather_sit','is_covid']

            logging.info(f"Applying feature engineering object on training dataframe and testing dataframe")
            feature_eng_train_arr = fe_obj.fit_transform(train_df)
            feature_eng_test_arr = fe_obj.transform(test_df)

            # Converting featured engineered array into dataframe
            feature_eng_train_df = pd.DataFrame(feature_eng_train_arr,columns=col)
            feature_eng_test_df = pd.DataFrame(feature_eng_test_arr,columns=col)

            logging.info(f"Splitting input and target feature from training and testing dataframe.")
            input_feature_train_df = feature_eng_train_df.drop(columns = target_column_name,axis = 1)
            target_feature_train_df = feature_eng_train_df[target_column_name]

            input_feature_test_df = feature_eng_test_df.drop(columns = target_column_name,axis = 1)
            target_feature_test_df = feature_eng_test_df[target_column_name]

            # Taking out date, year, month, hour columns from train and test data
            date_col_train_df = feature_eng_train_df.loc[:,date_columns]
            date_col_test_df = feature_eng_test_df.loc[:,date_columns]

            logging.info(f"Obtaining preprocessing object.")
            preprocessing_obj = self.get_data_transformer_object()

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")
            train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            test_arr = preprocessing_obj.transform(input_feature_test_df)

            transformed_train_df = pd.DataFrame(np.c_[date_col_train_df,train_arr,np.array(target_feature_train_df)],columns=all_columns+[target_column_name])
            transformed_test_df = pd.DataFrame(np.c_[date_col_test_df,test_arr,np.array(target_feature_test_df)],columns=all_columns+[target_column_name])

            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            transformed_train_file_path = os.path.join(transformed_train_dir,"transformed_train.csv")
            transformed_test_file_path = os.path.join(transformed_test_dir,"transformed_test.csv")

            save_data(file_path = transformed_train_file_path, data = transformed_train_df)
            save_data(file_path = transformed_test_file_path, data = transformed_test_df)

            logging.info("Saving Feature Engineering Object")
            feature_engineering_object_file_path = self.data_transformation_config.feature_engineering_object_file_path
            save_object(file_path = feature_engineering_object_file_path,obj = fe_obj)
            save_object(file_path=os.path.join(ROOT_DIR,PIKLE_FOLDER_NAME_KEY,
                                 os.path.basename(feature_engineering_object_file_path)),obj=fe_obj)

            logging.info("Saving Preprocessing Object")
            preprocessing_object_file_path = self.data_transformation_config.preprocessed_object_file_path
            save_object(file_path = preprocessing_object_file_path, obj = preprocessing_obj)
            save_object(file_path=os.path.join(ROOT_DIR,PIKLE_FOLDER_NAME_KEY,
                                 os.path.basename(preprocessing_object_file_path)),obj=preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(is_transformed=True,
            message="Data transformation successfull.",
            transformed_train_file_path = transformed_train_file_path,
            transformed_test_file_path = transformed_test_file_path,
            preprocessed_object_file_path = preprocessing_object_file_path,
            feature_engineering_object_file_path = feature_engineering_object_file_path)

            logging.info(f"Data Transformation Artifact: {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise ApplicationException(e,sys) from e

    def __del__(self):
        logging.info(f"\n{'*'*20} Data Transformation log completed {'*'*20}\n\n")