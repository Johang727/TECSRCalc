from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS
import datetime
import numpy as np
import re, os, sys

# Create the Flask application instance
app = Flask(__name__, static_folder='docs', template_folder='docs')

# yea imma be honest, ai made this func. nobody understands regex
def is_allowed_origin(origin):
    if not origin:
        return False
    if origin == "https://tecsrcalc.pages.dev":
        return True
    if re.match(r'https:\/\/[a-zA-Z0-9-]+\.tecsrcalc\.pages\.dev', origin):
        return True
    return False



CORS(app, origins=is_allowed_origin, supports_credentials=True) # type: ignore


# Load the trained model when the application starts
# This is more efficient than loading it for every request
MODEL_PATH:str = 'model.pkl'


try:
    # fetch and store variables from the packaged model
    print("Attempting to load model...")
    model_mets = joblib.load(MODEL_PATH)

    RFmodel = model_mets['models'][0]

    LRmodel = model_mets['models'][1]

    GBmodel = model_mets['models'][2]

    x = model_mets['dataX']

    print("Model loaded successfully!")
except FileNotFoundError:
    print(f"Error: Model file \"{MODEL_PATH}\" not found!")
    model = None
    sys.exit(0)

DPM_MIN = x["DPM"].min()

# ------- #

# webysite

@app.route('/')
def health_check():
    return jsonify({
        "status":"Running"
    })

@app.route('/predict', methods=['POST'])
def predict():
    # Check if the model was loaded successfully
    if not RFmodel and not LRmodel and not GBmodel:
        return jsonify({'error': 'One of the models is missing!'}), 500
    # From what I understand 500 errors are server-side; 400 are client-side
    # TODO, have it redirect to a new page with contact information

    # Get the data sent from the web page
    data = request.get_json(force=True)
    dpm = data.get('dpm')
    apm = data.get('apm')
    modelChoice = data.get('modelSelect')

    # Basic input validation
    if dpm is None or apm is None:
        return jsonify({'error': 'Missing DPM or APM values.'}), 400
    try:
        dpm = float(dpm)
        apm = float(apm)
        excel_start = datetime.date(1900, 1, 1)
        today = datetime.date.today()
        dateInt = (today - excel_start).days + 2
    except ValueError:
        return jsonify({'error': 'Invalid input. Please provide numbers.'}), 400

    # Create a pandas DataFrame for the prediction
    # The model expects the data in this format
    inData = pd.DataFrame([[dateInt, dpm, apm]], columns=['Date','DPM', 'APM'])

    if modelChoice == "Auto":
        if (dpm >= 155 or apm >= 140) or (dpm <= 35 or apm <= 10):
            useLR = True
            modelChoice = "Linear"
        else:
            modelChoice = "RandomForest"

    if modelChoice == "RandomForest":
        modelUsed = "Random Forest"
        # to add an uncertainty after the SR
        tp = [tree.predict(inData) for tree in RFmodel.estimators_]
        calc = f"{round(np.mean(tp))} ± {round(np.std(tp))}"
    elif modelChoice == "Linear":
        modelUsed = "Linear"
        calc = round(LRmodel.predict(inData)[0])
    elif modelChoice == "GradientBoosting":
        modelUsed = "Gradient Boosting"
        calc = 0 # TODO: actually make it work
    else:
        calc = 0
        modelUsed = "Error!"


    return jsonify({
        'sr': calc,
        'model':modelUsed
        })

@app.route('/metrics')
def getMetrics():
    try:
        with open("README.md", "r") as readme:
            rd = readme.read()
    except FileNotFoundError:
        return "README.md not found!", 404
    
    secStart = "<!--START_SECTION:metrics-->"
    secEnd = "<!--END_SECTION:metrics-->"

    match = re.search(f"{secStart}(.*?){secEnd}", rd, re.DOTALL)

    if match:
        section = match.group(1).strip()
        return section, 200, {"Content-Type": "text/plain"}
    else:
        return "Metrics not found!", 404



if __name__ == '__main__':
    # only runs when run locally
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")

