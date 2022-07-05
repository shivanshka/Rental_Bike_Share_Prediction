import yaml
from Prediction_Application.exception import ApplicationException
import os,sys
import dill
import pandas as pd
import numpy as np
from Prediction_Application.constant import *

def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns the contents as dictionary.

    Params:
    ---------------
    file_path (str) : file path for the yaml file
    """
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise ApplicationException(e,sys) from e
