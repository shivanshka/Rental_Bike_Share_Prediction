from wsgiref import simple_server
from flask import Flask, render_template,request, Response
from flask_cors import CORS, cross_origin
from Prediction_Application.pipeline.prediction_pipeline import Prediction
from Prediction_Application.pipeline.training_pipeline import Model_Training
from Prediction_Application.logger import logging
import os

app = Flask(__name__)
CORS(app)

@app.route("/", methods =["GET","POST"])
@cross_origin()
def home():
    return render_template("Home.html")

@app.route("/bulk_page", methods =["GET"])
@cross_origin()
def bulk_page():
    return render_template("Bulk-Prediction.html")

@app.route("/single_page", methods =["GET"])
@cross_origin()
def single_page():
    return render_template("Single-Prediction.html")

@app.route("/contact", methods =["GET"])
@cross_origin()
def contact():
    return render_template("Contact.html")

@app.route("/bulk_predict", methods=['POST'])
@cross_origin()
def bulk_predict():
    try:
        if request.json is not None:
            path = request.json['filepath']
            pred = Prediction(path)  # object initialization
            path = pred.initiate_bulk_prediction()  # initiating the prediction pipeline
            return Response("Prediction File created at !!!" + str(path))
        
        elif request.form is not None:
            path = request.form['filepath']
            pred = Prediction(path)  # object initialization
            path = pred.initiate_bulk_prediction()  # initiating the prediction pipeline
            return Response("Prediction File created at !!!" + str(path))
        else:
            print('Nothing Matched')
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)


@app.route("/single_predict", methods=['POST'])
@cross_origin()
def single_predict():
    try:
        if request.json is not None:
            data = request.json['filepath']

            pred = Prediction()  # object initialization
            pred_val = pred.initiate_single_prediction(data)  # calling the prediction_validation function
            return Response("Prediction File created at !!!" + str(pred_val))

        elif request.form is not None:
            data = request.form['filepath']

            pred = Prediction()  # object initialization
            pred_val = pred.initiate_single_prediction(data)  # calling the prediction_validation function
            return Response("Prediction File created at !!!" + str(pred_val))
            
        else:
            print('Nothing Matched')
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)


@app.route("/train", methods=['GET', 'POST'])
@cross_origin()
def trainRouteClient():
    try:
        # if request.json['folderPath'] is not None:
        folder_path = "Training_Batch_Files"
        # path = request.json['folderPath']
        if folder_path is not None:
            path = folder_path
            train_Obj = Model_Training(path)  # object initialization
            train_Obj.initiate_model_training()  # training the model for the files in the table
            
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)
    return Response("Training successful!!")

port = int(os.getenv("PORT", 6000))
if __name__=="__main__":
    host = 'localhost'
    httpd = simple_server.make_server(host, port, app)
    print("Serving on %s:%d" % (host, port))
    httpd.serve_forever()