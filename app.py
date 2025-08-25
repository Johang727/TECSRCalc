from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS
import datetime
import numpy as np

# Create the Flask application instance
app = Flask(__name__, static_folder='docs', template_folder='docs')
CORS(app, origins="https://johang727.github.io")

# Load the trained model when the application starts
# This is more efficient than loading it for every request
MODEL_PATH:str = 'model.pkl'


try:
    # fetch and store variables from the packaged model
    print("Attempting to load model...")
    model_mets = joblib.load(MODEL_PATH)

    RFmodel = model_mets['RFmodel']
    RF_mse = model_mets['RF_mse']
    RF_r2 = model_mets['RF_r2']

    LRmodel = model_mets['LRmodel']
    LR_mse = model_mets['LR_mse']
    LR_r2 = model_mets['LR_r2']

    size = model_mets['size']
    timestamp = model_mets['timestamp']
    srCounts = model_mets['srCounts']
    print("Model loaded successfully!")
except FileNotFoundError:
    print(f"Error: Model file \"{MODEL_PATH}\" not found!")
    model = None

@app.route('/')
def home():
    # sets the home page
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Handles prediction, renamed calculation later, since I liked that name better after testing
    # Check if the model was loaded successfully
    if RFmodel is None and LRmodel:
        return jsonify({'error': 'Model file not found!'}), 500
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

    useLR = False

    # Switch models to one that's better at extrapolating
    if modelChoice == "Linear":
        useLR = True
    elif modelChoice == "RandomForest":
        useLR = False
    else:
        if (dpm >= 155 or apm >= 140) or (dpm <= 35 or apm <= 10):
            useLR = True
        else:
            useLR = False

    if useLR:
        modelUsed = "Linear"
        calc = round(LRmodel.predict(inData)[0])
    else:
        modelUsed = "Random Forest"
        # to add an uncertainty after the SR
        tp = [tree.predict(inData) for tree in RFmodel.estimators_]
        calc = f"{round(np.mean(tp))} ± {round(np.std(tp))}"


    return jsonify({
        'sr': calc,
        'model':modelUsed
        })

@app.route('/metrics')
def metrics():
    if RFmodel is None and LRmodel:
        return jsonify({'error': 'Model file not found!'}), 500
    
    return jsonify({
        'RF_mse': round(RF_mse, 2),
        'RF_r2': round(RF_r2, 2),
        'LR_mse': round(LR_mse, 2),
        'LR_r2': round(LR_r2, 2),
        'size': size,
        'timestamp': timestamp,
        'srCounts': srCounts
    })

if __name__ == '__main__':
    # only runs when run locally
    app.run(debug=True)

