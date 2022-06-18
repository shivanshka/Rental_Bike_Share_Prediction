from flask import Flask, render_template
from flask_cors import CORS, cross_origin

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

if __name__=="__main__":
    app.run(host = "localhost", port = 8001)