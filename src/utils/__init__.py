import os, sys, pandas as pd, pickle
from typing import Dict, Tuple

from src.constants import *
from src.exceptions import CustomException
from src.logger import logging


class mainutils:
    def __init__(self):
        pass
    
    def read_yaml_file(self, filename:str)->dict:
        try:
            with open (filename, "rb") as yaml_file:
                return yaml.safe_load(yaml_file)
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def read_schema_config_file(self)->dict:
        try:
            schema_config = os.path.join("config", "schema.yaml")
            return schema_config
        except Exception as e:
            raise CustomException(e, sys) from e
    
    @staticmethod
    def save_object(file_path: str, obj: object)->None:
        logging.info("Entered the save_object method of Mainutils class")
        
        try:
            with open (file_path, "rb") as file_obj:
                pickle.dump(obj, file_obj)
            logging.info("Exited the save_object method of Mainutils class")
        except Exception as e:
            raise CustomException(e, sys) from e
    
    @staticmethod
    def load_object(file_path: str)->object:
        logging.info("Entered the load_object method of Mainutils class")
        
        try:
            with open (file_path, "rb") as file_obj:
                obj = pickle.load(file_obj)
            logging.info("Exited the load_object method of Mainutils class")
            return obj
        except Exception as e:
            raise CustomException(e, sys) from e