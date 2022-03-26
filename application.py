from flask import Flask, jsonify, request
import pickle
import numpy as np
import pandas as pd

with open("models/cluster_kmeans_model.pkl", "rb") as cluster_model_file:
    clustering = pickle.load(cluster_model_file)


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def halo():
    p1 = 10.500
    p2 = 0.1
    p3 = 240
    p4 = 10
    p5 = 20  # sub_1
    p6 = 0  # sub_2
    p7 = 12  # sub_3
    p8 = p1*1000/60 - p5 - p6 - p7
    col = ['Global_active_power', 'Global_reactive_power', 'Voltage',
           'Global_intensity', 'Sub_metering_1', 'Sub_metering_2',
           'Sub_metering_3', 'Other_active_metering']
    predicted = clustering.predict(pd.DataFrame(
        [[p1, p2, p3, p4, p5, p6, p7, p8]], columns=col))
    res = {
        'thing1': request.values.get('thing1'),
        'thing2': request.values.get('thing2'),
        'res': str(predicted)
    }
    return res


@app.route("/hello")
def hello():
    return "<h1> Hello, World! </h1>"


app.run(debug=True)
