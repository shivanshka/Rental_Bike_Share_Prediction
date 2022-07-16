import re
from wsgiref import simple_server
from flask import Flask, render_template,request, Response
from flask_cors import CORS, cross_origin
from Prediction_Application.pipeline.prediction_pipeline import Prediction
from Prediction_Application.pipeline.training_pipeline import Training_Pipeline

#from Prediction_Application.logger import logging
import os,sys

app = Flask(__name__)
CORS(app)

@app.route("/", methods =["GET"])
@cross_origin()
def home():
    return render_template("Home.html")

@app.route("/bulk_page", methods =["GET","POST"])
@cross_origin()
def bulk_page():
    print(request.method)
    if request.method == "GET":
        return render_template("Bulk-Prediction.html")
    if request.method == "POST":
        try:
            path = request.form['filepath']
            pred = Prediction(path)  # object initialization
            path = pred.initiate_bulk_prediction()  # initiating the prediction pipeline
            return Response(str(path))
        
        except ValueError:
            return Response("Error Occurred! %s" % ValueError)
        except KeyError:
            return Response("Error Occurred! %s" % KeyError)
        except Exception as e:
            return Response("Error Occurred! %s" % e)

@app.route("/single_page", methods =["GET","POST"])
@cross_origin()
def single_page():
    if request.method == "GET":
        return render_template("Single-Prediction.html")
    if request.method == "POST":
        pass

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
            data = {'month': request.json['month'],
            'hour': request.form('hour'),
            'season': request.form('season'),
            'weekday': request.form('weekday'),
            'is_holiday': request.form('is_holiday'),
            'working_day': request.form('working_day'),
            'weather_sit': request.form('weather_sit'),
            'is_covid': request.form('is_covid'),
            'temp': request.form('temp'),
            'r_temp': request.form('r_temp'),
            'wind': request.form('wind'),
            'humidity': request.form('humidity')}

            pred = Prediction()  # object initialization
            pred_val = pred.initiate_single_prediction(data)  # calling the prediction_validation function
            return Response("Prediction File created at !!!" + str(pred_val))

        elif request.form is not None:
            data = {'month': int(request.form['month']),
            'hour': int(request.form['hour']),
            'season': request.form('season'),
            'weekday': request.form('weekday'),
            'is_holiday': request.form('is_holiday'),
            'working_day': request.form('working_day'),
            'weather_sit': request.form('weather_sit'),
            'is_covid': request.form('is_covid'),
            'temp': float(request.form('temp')),
            'wind': float(request.form('wind')),
            'humidity': float(request.form('humidity'))}

            pred = Prediction()  # object initialization
            pred_val = pred.initiate_single_prediction(data)  # calling the prediction_validation function
            return Response("Demand for Bikes with given conditions: " + str(pred_val))
            
        else:
            print('Nothing Matched')
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)


@app.route("/start_train", methods=['GET', 'POST'])
@cross_origin()
def trainRouteClient():
    try:
        train_obj = Training_Pipeline()
        train_obj.run_training_pipeline() # training the model for the files in the table
            
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)
    return Response("Training successful!!")

#port = int(os.getenv("PORT",5004))
if __name__=="__main__":
    app.run(debug = True)
    #host = '0.0.0.0'
    #httpd = simple_server.make_server(host, port, app)
    #print("Serving on %s:%d" % (host, port))
    #httpd.serve_forever()
    