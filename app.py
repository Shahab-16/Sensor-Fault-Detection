from flask import Flask, render_template, jsonify, request, send_file
from src.exception import CustomException
from src.logger import logging as lg
import os, sys

from src.pipeline.train_pipeline import TrainingPipeline
from src.pipeline.predict_pipeline import PredictionPipeline

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/train")
def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        
        # Return a success message with styling
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Training Complete</title>
            <link rel="stylesheet" href="/static/css/style.css">
        </head>
        <body>
            <div class="container">
                <div class="message success">
                    <h2>Training Completed Successfully!</h2>
                </div>
                <a href="/" class="btn home-btn">Back to Home</a>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        error_message = str(e)
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Training Error</title>
            <link rel="stylesheet" href="/static/css/style.css">
        </head>
        <body>
            <div class="container">
                <div class="message error">
                    <h2>Training Failed</h2>
                    <p>{error_message}</p>
                </div>
                <a href="/" class="btn home-btn">Back to Home</a>
            </div>
        </body>
        </html>
        """, 500

@app.route('/predict', methods=['POST', 'GET'])
def upload():
    try:
        if request.method == 'POST':
            prediction_pipeline = PredictionPipeline(request)
            prediction_file_detail = prediction_pipeline.run_pipeline()

            lg.info("prediction completed. Downloading prediction file.")
            return send_file(
                prediction_file_detail.prediction_file_path,
                download_name=prediction_file_detail.prediction_file_name,
                as_attachment=True
            )
        else:
            return render_template('upload_file.html')
    except Exception as e:
        error_message = str(e)
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Prediction Error</title>
            <link rel="stylesheet" href="/static/css/style.css">
        </head>
        <body>
            <div class="container">
                <div class="message error">
                    <h2>Prediction Failed</h2>
                    <p>{error_message}</p>
                </div>
                <a href="/" class="btn home-btn">Back to Home</a>
            </div>
        </body>
        </html>
        """, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)