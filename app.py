from flask import Flask, jsonify, request
import pickle
import pandas as pd
from flask_cors import CORS

with open("models/cluster_kmeans_model.pkl", "rb") as cluster_model_file:
    clustering = pickle.load(cluster_model_file)


app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*":
                            {
                                "origins": "*"
                            }
                            }
            )


@ app.route("/", methods=['GET', 'POST'])
def halo():
    p1 = request.values.get('global_active_power')
    p2 = request.values.get('global_reactive_power')
    p3 = request.values.get('voltage')
    p4 = request.values.get('global_intensity')
    p5 = request.values.get('sub_metering_1')
    p6 = request.values.get('sub_metering_2')
    p7 = request.values.get('sub_metering_3')

    p1 = float(p1) if p1 != None else 0
    p2 = float(p2) if p2 != None else 0
    p3 = float(p3) if p3 != None else 0
    p4 = float(p4) if p4 != None else 0
    p5 = float(p5) if p5 != None else 0
    p6 = float(p6) if p6 != None else 0
    p7 = float(p7) if p7 != None else 0

    # if ((p1 != None) & (p2 != None) & (p3 != None) & (p4 != None) & (p5 != None) & (p6 != None) & (p7 != None)):
    #     p1, p2, p3, p4, p5, p6, p7 = float(p1), float(p2), float(
    #         p3), float(p4), float(p5), float(p6), float(p7)
    # else:
    #     p1, p2, p3, p4, p5, p6, p7 = 0, 0, 0, 0, 0, 0, 0
    p8 = ((p1*1000/60) - p5 - p6 - p7)
    col = ['Global_active_power', 'Global_reactive_power', 'Voltage',
           'Global_intensity', 'Sub_metering_1', 'Sub_metering_2',
           'Sub_metering_3', 'Other_active_metering']
    predicted = clustering.predict(pd.DataFrame(
        [[p1, p2, p3, p4, p5, p6, p7, p8]], columns=col))
    res = {
        'res': str(predicted),
        # 'info': "okeoke",
        # 'check': f"params {p1}, params {p2}, params {p3}, params {p4}, params {p5}, params {p6}, params {p7}, params {p8}"
    }
    return res


@ app.route("/hello")
def hello():
    return "<h1> Hello, World! </h1>"


@ app.route("/postest", methods=['GET', 'POST'])
def predict():
    p1 = request.form['global_active_power']
    p2 = request.form['global_reactive_power']
    p3 = request.form['voltage']
    p4 = request.form['global_intensity']
    p5 = request.form['sub_metering_1']
    p6 = request.form['sub_metering_2']
    p7 = request.form['sub_metering_3']
    return f"{p1, p2, p3, p4, p5, p6, p7}"


# app.run(host= , debug=False)
