from flask import Flask, render_template, jsonify, request, send_file
import os, sys
from src.logger import logging
from src.exceptions import CustomException
from src.pipeline.training_pipeline import TrainingPipeline
from src.pipeline.predict_pipeline import PredictionPipeline

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to my application."

@app.route("/train")
def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        
        return "Training completed."
    except Exception as e:
        raise CustomException(e, sys)

@app.route("/predict", methods = ['POST', 'GET'])
def upload():
    try:
        if request.method == 'POST':
            prediction_pipeline = PredictionPipeline(request)
            prediction_file_details = prediction_pipeline.run_pipeline()
            logging.info("Prediction completed. Downloading the prediction file.")
            
            return send_file(prediction_file_details.prediction_file_path,
                             download_name=prediction_file_details.prediction_file_name,
                             as_attachment=True)
        else:
            return render_template('upload_file.html')
    except Exception as e:
        raise CustomException(e, sys)
    
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5000, debug=True)