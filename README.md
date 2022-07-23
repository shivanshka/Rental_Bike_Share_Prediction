# Rental_Bike_Share_Prediction  
application link : http://rental-bike-demand-us.herokuapp.com/

## Project Objective
The objective of this project is to create a solution for user which can help them to predict demand for rental bikes for Capital Bikes in Washington DC so that they can strategically fullfill demand.

## Project Demo Video
link: 

## Project Architecture
We have used layered architecture for carrying out below flow actions:
image.png

## Tools Used
- Jupyter Notebook
- VS Code
- Flask
- Database : MongoDB
- Machine Learning Algorithms: Random Forest and XG Boost
- MLOps
- HTML

## Dataset
We have taken data from 2018 to January 2022 for training, Feb 2022 to Mar 2022 for Testing.

Ride was collected from Capital Bike Share website.
link: http://capitalbikeshare.com/system-data

Weather Data was collected from link: http://www.freemeteo.com

We have derived the final dataset for model training from above two datasets.

## Project Details
There are six packages in the pipeline: Config, Entity, Constant, Exception, Logger, Components and Pipeline

### Config
This package will create all folder structures and provide inputs to the each of the components.

### Entity
This package will defines named tuple for each of the components config and artifacts it generates.

### Constant
This package will contain all predefined constants which can be used accessed from anywhere

### Exception
This package contains the custom exception class for the Prediction Appliaction

### Logger
This package helps in logging all the activity

### Components
This package contains five modules:
1. Data Ingestion: This module downloads the data from the link, unzip it, then stores entire data into Db.
                   From DB it extracts all data into single csv file and split it into training and testing datasets.
2. Data Validation: This module validates whether data files passed are as per defined schema which was agreed upon
                    by client.
3. Data Transformation: This module applies all the Feature Engineering and preprocessing to the data we need to 
                        train our model and save  the pickle object for same.
4. Model Trainer: This module trains the model on transformed data, evalutes it based on R2 accuracy score and 
                  saves the best performing model object for prediction

### Pipeline
This package contains two modules:
1. Training Pipeline: This module will initiate the training pipeline where each of the above mentioned components  
                      will be called sequentially untill model is saved.
2. Prediction Pipeline: This module will help getting prediction from saved trained model.

## Contributors
Shivansh Kaushal