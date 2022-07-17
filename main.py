
from flask import Flask, render_template,request, send_file, redirect,url_for,flash
from flask_cors import CORS, cross_origin
from Prediction_Application.pipeline.prediction_pipeline import Prediction
from Prediction_Application.pipeline.training_pipeline import Training_Pipeline
from Prediction_Application.logger import logging
import os
import sys
import shutil

app = Flask(__name__)
CORS(app)
app.secret_key = "any random string"

@app.route("/", methods =["GET"])
@cross_origin()
def home():
    return render_template("result.html")

@app.route("/bulk_predict", methods =["POST"])
@cross_origin()
def bulk_predict():
    try:
        file = request.files.get("files")
        folder = "Prediction_Batch_Files"
        if file is not None:
            flash("File uploaded!!","success")
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        os.mkdir(folder)

        file.save(os.path.join(folder,file.filename))

        pred = Prediction()
        output_file = pred.initiate_bulk_prediction()
        path = os.path.basename(output_file)

        if path is not None:
            flash("Prediction File generated!!","success")
        return send_file(output_file,as_attachment=True)
    except Exception as e:
        flash('Something went wrong', 'danger')
        return redirect(url_for('home'))

@app.route("/single_page", methods =["GET","POST"])
@cross_origin()
def single_page():
    return render_template("Single-Prediction.html")

@app.route("/contact", methods =["GET"])
@cross_origin()
def contact():
    return render_template("Contact.html")



@app.route("/start_train", methods=['GET', 'POST'])
@cross_origin()
def trainRouteClient():
    try:
        train_obj = Training_Pipeline()
        train_obj.run_training_pipeline() # training the model for the files in the table
    except Exception as e:
        return f"Error occured : {e}"


if __name__=="__main__":
    
    port = int(os.getenv("PORT",5003))
    host = '0.0.0.0'
    app.run(host=host,port=port,debug=True)
    
    