import shutil, os, sys, pandas as pd, numpy as np, pickle
from src.logger import logging
from src.exceptions import CustomException
from src.constants import *
from src.utils.main_utils import MainUtils
from flask import request
from dataclasses import dataclass

@dataclass
class PredictionPipelineConfig:
    prediction_output_dirname: str = 'predictions'
    prediction_file_name: str = 'predictions_output.csv'
    model_file_path: str = os.path.join(artifact_folder, ['model.pkl'])
    preprocessor_path: str = os.path.join(artifact_folder, ['preprocessor.pkl'])
    prediction_file_path = os.path.join(prediction_output_dirname, prediction_file_name)
    
class PredictionPipeline:
    
    def __init__(self, request: request):
        self.request = request
        self.utils = MainUtils()
        self.prediction_pipeline_config = PredictionPipelineConfig()
    
    def save_input_files(self) -> str:
        try:
            pred_file_input_dir = 'prediction_artifacts' # output folder name.
            os.makedirs(pred_file_input_dir, exist_ok=True) # create artifact directory for prediction.
            
            input_csv_file = self.request.files['file']  # getting the file uploaded
            pred_file_path = os.path.join(pred_file_input_dir, input_csv_file.filename()) # creating the file path of prediction.
            
            input_csv_file.save(pred_file_path) # saving the uploaded data into csv.
            
            return pred_file_path
        except Exception as e:
            raise CustomException(e, sys)
        
    def predict(self, features):
        try:
            model = self.utils.load_object(self.prediction_pipeline_config.model_file_path) # loading the model trained.
            preprocessor = self.utils.load_object(self.prediction_pipeline_config.preprocessor_path) # loading the preprocessor.
            
            transformed_x = preprocessor.transform(features) # preprocessing the input data.
            preds = model.predict(transformed_x) # predicting the output.
            
            return preds
        except Exception as e:
            raise CustomException(e, sys)
            
    def get_predicted_dataframe(self, input_dataframe_path: pd.DataFrame):
        try:
            prediction_column_name: str = TARGET_COLUMN
            input_dataframe: pd.DataFrame = pd.read_csv(input_dataframe_path) # dataframe to be predicted.
            input_dataframe = input_dataframe.drop(columns="Unnamed: 0") if "Unnamed: 0" in input_dataframe.columns else input_dataframe # removing the unwanted column.
            predictions = self.predict(input_dataframe) # predicted output.
            input_dataframe[prediction_column_name] = [pred for pred in predictions] # adding output to the dataframe.
            target_column_mapping = {0:'bad', 1:'good'} # prediction transformation.
            input_dataframe[prediction_column_name] = input_dataframe[prediction_column_name].map(target_column_mapping) # transforming the prediction.
            os.makedirs(self.prediction_pipeline_config.prediction_output_dirname, exist_ok=True) # creating output directory.
            input_dataframe.to_csv(self.prediction_pipeline_config.prediction_file_path, index=False) # saving output as csv file.
            
            logging.info("Prediction is completed.")
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def run_pipeline(self):
        try:
            input_csv_path = self.save_input_files()
            self.get_predicted_dataframe(input_csv_path) # running the prediction pipeline.
            return self.prediction_pipeline_config
        
        except Exception as e:
            raise CustomException(e, sys)