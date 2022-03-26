from flask import Flask, jsonify, request
import pickle
import pandas as pd

with open("models/cluster_kmeans_model.pkl", "rb") as cluster_model_file:
    clustering = pickle.load(cluster_model_file)


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def halo():
    p1 = request.values.get('global_active_power')
    p2 = request.values.get('global_reactive_power')
    p3 = request.values.get('voltage')
    p4 = request.values.get('global_intensity')
    p5 = request.values.get('sub_metering_1')
    p6 = request.values.get('sub_metering_2')
    p7 = request.values.get('sub_metering_3')
    if ((p1 != None) & (p2 != None) & (p3 != None) & (p4 != None) & (p5 != None) & (p6 != None) & (p7 != None)):
        p1, p2, p3, p4, p5, p6, p7 = int(p1), int(p2), int(
            p3), int(p4), int(p5), int(p6), int(p7)
    else:
        p1, p2, p3, p4, p5, p6, p7 = 0, 0, 0, 0, 0, 0, 0
    p8 = ((p1*1000/60) - p5 - p6 - p7)
    col = ['Global_active_power', 'Global_reactive_power', 'Voltage',
           'Global_intensity', 'Sub_metering_1', 'Sub_metering_2',
           'Sub_metering_3', 'Other_active_metering']
    predicted = clustering.predict(pd.DataFrame(
        [[p1, p2, p3, p4, p5, p6, p7, p8]], columns=col))
    res = {
        'res': str(predicted),
        'info': "okeoke",
        'check': f"params {p1}, params {p2}, params {p3}, params {p4}, params {p5}, params {p6}, params {p7}, params {p8}"
    }
    return res


@app.route("/hello")
def hello():
    return "<h1> Hello, World! </h1>"


# app.run(host= , debug=False)
