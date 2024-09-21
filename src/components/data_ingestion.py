import sys
import os
import pandas as pd
import numpy as np
from pymongo.mongo_client import MongoClient
from zipfile import Path
from src.constants import *
from src.exceptions import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    artifact_folder: str = os.path.join(artifact_folder)
    
class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.utils = MainUtils()
        
    def export_collection_as_dataframe(self, collection_name, db_name):
        
        try:
            mongo_client = MongoClient(MONGO_DB_URL) # the url is coming from constants init file.
            collection = mongo_client[db_name][collection_name] # building connection to mongo db.
            df = pd.DataFrame(list(collection.find())) # fetching database in pandas dataframe.
            if "_id" in df.columns.tolist(): # removing id column.
                df.drop(columns=["_id"], axis=1, inplace=True)
            df.replace({"na": np.nan}, inplace=True) # replacing null value.
            return df
        except Exception as e:
            raise CustomException(e, sys) # returning system error through exception.py
        
    def export_data_into_feature_store_file_path(self) -> pd.DataFrame:
        try:
            logging.info("Exporting data from mongodb:")
            raw_file_path = self.data_ingestion_config.artifact_folder # creating raw file path
            
            os.makedirs(raw_file_path, exist_ok=True) # making directory for the raw file path, returns no error if directory exists.
            
            sensor_data = self.export_collection_as_dataframe(
                collection_name=MONGO_COLLECTION_NAME,
                db_name=MONGO_DATABASE_NAME
            ) # saving the data from mongo db database.
            
            logging.info(f"Saving the exported data into feature store file path: {raw_file_path}")
            
            feature_store_file_path = os.path.join(raw_file_path, 'wafer_fault.csv') # create path for saving the data into csv file.
            
            sensor_data.to_csv(feature_store_file_path, index=False) # saving into csv file.
            
            return feature_store_file_path # retutrning the data file path.
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_ingestion(self) -> Path:
        logging.info("Entered inited_data_ingestion method of data_injestion class.")
        
        try:
            feature_store_file_path = self.export_data_into_feature_store_file_path()
            
            logging.info("Got the data from mongodb.")
            
            logging.info("Exeted inited_data_ingestion method of data_injestion class.")
            
            return feature_store_file_path
        
        except Exception as e:
            raise CustomException(e, sys) from e
            