from flask import Flask, render_template, request, jsonify
import joblib, os, sys, datetime
import pandas as pd
from flask_cors import CORS
import numpy as np
from werkzeug.middleware.proxy_fix import ProxyFix

# Create the Flask application instance
app = Flask(__name__, static_folder="docs", template_folder="docs")


CORS(app, origins=["https://tecsrcalc.pages.dev", "https://tecsrcalc.org"])

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

# Load the trained model when the application starts
# This is more efficient than loading it for every request
MODEL_PATH:str = "model.pkl"


try:
    # fetch and store variables from the packaged model
    print("Attempting to load model...")
    model_mets = joblib.load(MODEL_PATH)

    RFmodel = model_mets["models"][0]

    LRmodel = model_mets["models"][1]

    GBmodel = model_mets["models"][2]

    RFGB_ensemble = model_mets["models"][3]

    AllModel = model_mets["models"][4]

    x = model_mets["dataX"]
    y = model_mets["dataY"]

    r2 = model_mets["r2"]
    rmse = model_mets["rmse"]
    mape = model_mets["mape"]

    size = model_mets["size"]
    test_size = model_mets["testSize"]

    timestamp = model_mets["timestamp"]

    areas_error:dict = model_mets["areas_error"]

    print("Model loaded successfully!")
except FileNotFoundError:
    print(f"Error: Model file \"{MODEL_PATH}\" not found!")
    model = None
    sys.exit(0)

DPM_MIN = x["DPM"].min()
DPM_MAX = x["DPM"].max()

APM_MIN = x["APM"].min()
APM_MAX = x["APM"].max()

SR_MIN = y.min()
SR_MAX = y.max()


# ------- #

# webysite

@app.route("/")
def health_check():
    return jsonify({
        "status":"Running"
    })

@app.route("/predict", methods=["POST"])
def predict():
    # Check if the model was loaded successfully
    if not RFmodel and not LRmodel and not GBmodel and not AllModel:
        return jsonify({"error": "One of the models is missing!"}), 500
    # From what I understand 500 errors are server-side; 400 are client-side
    # TODO, have it redirect to a new page with contact information

    # Get the data sent from the web page
    data = request.get_json(force=True)
    dpm = data.get("DPM")
    apm = data.get("APM")
    modelChoice = data.get("MODEL_SELECTION")

    print(f"[DEBUG] Calculation Request Recieved: DPM = {dpm}; APM = {apm}; Model = {modelChoice}")

    # basic input validation
    if dpm is None or apm is None:
        return jsonify({"error": "Missing DPM or APM values."}), 400
    try:
        dpm = float(dpm)
        apm = float(apm)
        app = apm/dpm
        excel_start = datetime.date(1900, 1, 1)
        today = datetime.date.today()
        dateInt = (today - excel_start).days + 2
    except ValueError:
        print("[ERROR] Something triggered a ValueError.")
        return jsonify({"error": "Invalid input. Please provide numbers."}), 400

    # Create a pandas DataFrame for the prediction
    # The model expects the data in this format
    inData = pd.DataFrame([[dateInt, dpm, apm, app]], columns=["Date","DPM", "APM", "APP"])

    if modelChoice == "Auto":
        if (dpm >= DPM_MAX or apm >= APM_MAX) or (dpm <= DPM_MIN or apm <= APM_MIN):
            modelChoice = "Linear"
        else:
            modelChoice = "RF_GB_Ensemble"


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
        calc = round(GBmodel.predict(inData)[0])
    elif modelChoice == "RF_GB_Ensemble":
        modelUsed = "Random Forest + Gradient Boosting"
        calc = round(RFGB_ensemble.predict(inData)[0])
    elif modelChoice == "All":
        modelUsed = "All"
        calc = round(AllModel.predict(inData)[0])
    else:
        calc = 0
        modelUsed = "Error!"
        print("[ERROR] Model invalid!")

    print(f"[DEBUG] {modelUsed} calculated an SR of {calc} with the user's data!")
    return jsonify({
        "sr": calc,
        "model":modelUsed,
        "app":apm/dpm
        })


@app.route("/simple_metrics")
def get_simple_metrics():
    excel_start = datetime.date(1900, 1, 1)
    today = datetime.date.today()
    date = (today - excel_start).days + 2

    b_err = str(areas_error.get("Beginner_all", "No data."))
    i_err = str(areas_error.get("Intermediate_all", "No data."))
    a_err = str(areas_error.get("Advanced_all", "No data."))
    e_err = str(areas_error.get("Expert_all", "No data."))
    m_err = str(areas_error.get("Master_all", "No data."))

    return jsonify({
        "date": int(date),
        "b_err": b_err,
        "i_err": i_err,
        "a_err": a_err,
        "e_err": e_err,
        "m_err": m_err,
        "lower": int(SR_MIN),
        "upper": int(SR_MAX)
    })

if __name__ == "__main__":
    # only runs when run locally
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")

