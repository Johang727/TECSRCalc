from flask import Flask, render_template, request, jsonify
import joblib, os, sys, datetime, secrets, jwt, re
import pandas as pd
from flask_cors import CORS
import numpy as np
from werkzeug.middleware.proxy_fix import ProxyFix
import database as db
from functools import wraps
from dotenv import load_dotenv

# Create the Flask application instance
app = Flask(__name__, static_folder='docs', template_folder='docs')


CORS(app, origins=["https://tecsrcalc.pages.dev", "https://tecsrcalc.org"])

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

# Load the trained model when the application starts
# This is more efficient than loading it for every request
MODEL_PATH:str = 'model.pkl'

load_dotenv()

TOKEN_KEY = os.getenv("TOKEN_KEY", "None")


if TOKEN_KEY == "None":
    print("Check .env! No token key found!")
    sys.exit(1)

try:
    # fetch and store variables from the packaged model
    print("Attempting to load model...")
    model_mets = joblib.load(MODEL_PATH)

    RFmodel = model_mets['models'][0]

    LRmodel = model_mets['models'][1]

    GBmodel = model_mets['models'][2]

    RFGB_ensemble = model_mets['models'][3]

    AllModel = model_mets['models'][4]

    x = model_mets['dataX']
    y = model_mets['dataY']

    r2 = model_mets['r2']
    rmse = model_mets['rmse']
    mape = model_mets['mape']

    size = model_mets['size']
    test_size = model_mets['testSize']

    timestamp = model_mets['timestamp']



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

def tkn_req(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({'message': 'Authorization token is missing!'}), 401

        try:
            token_string = token.split(' ')[1]
        except IndexError:
            token_string = token

        usr_id = db.verify_token(token_string)

        if usr_id == -1:
            return jsonify({'message': 'Token is invalid or expired.'}), 403
        
        return f(usr_id, *args, **kwargs)
    return decorated

def prms_req(min_lvl):
    def decorator(f):
        @wraps(f)
        def decorated_function(usr_id, *args, **kwargs):
            usr_perms = db.get_usr_perms(usr_id)

            if usr_perms < min_lvl:
                return jsonify({
                    "message":"Insufficient permissions.",
                    "required": min_lvl,
                    "current": usr_perms
                }), 403
            
            return f(usr_id, *args, **kwargs)
        return decorated_function
    return decorator


@app.route('/')
def health_check():
    return jsonify({
        "status":"Running"
    })

@app.route('/predict', methods=['POST'])
def predict():
    # Check if the model was loaded successfully
    if not RFmodel and not LRmodel and not GBmodel and not AllModel:
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
        app = apm/dpm
        excel_start = datetime.date(1900, 1, 1)
        today = datetime.date.today()
        dateInt = (today - excel_start).days + 2
    except ValueError:
        return jsonify({'error': 'Invalid input. Please provide numbers.'}), 400

    # Create a pandas DataFrame for the prediction
    # The model expects the data in this format
    inData = pd.DataFrame([[dateInt, dpm, apm, app]], columns=['Date','DPM', 'APM', 'APP'])

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


    return jsonify({
        'sr': calc,
        'model':modelUsed,
        'app':apm/dpm
        })

@app.route('/metrics')
def getMetrics():

    excel_start = datetime.date(1900, 1, 1)
    today = datetime.date.today()
    date = (today - excel_start).days + 2

    final_string:str = ""

    metric_list:list[str] = []
    
    metric_list.append("Linear (Auto):\n")

    metric_list.append(f"\t- Root Mean Squared Error: {rmse[1]:.2f}\n")
    metric_list.append(f"\t- Mean Absolute Percentage Error: {mape[1]*100:.2f}%\n")
    metric_list.append(f"\t- R-Squared: {r2[1]:.4f}\n")

    metric_list.append("\nRandom Forest:\n")

    metric_list.append(f"\t- Root Mean Squared Error: {rmse[0]:.2f}\n")
    metric_list.append(f"\t- Mean Absolute Percentage Error: {mape[0]*100:.2f}%\n")
    metric_list.append(f"\t- R-Squared: {r2[0]:.4f}\n")

    metric_list.append("\nGradient Boosting:\n")

    metric_list.append(f"\t- Root Mean Squared Error: {rmse[2]:.2f}\n")
    metric_list.append(f"\t- Mean Absolute Percentage Error: {mape[2]*100:.2f}%\n")
    metric_list.append(f"\t- R-Squared: {r2[2]:.4f}\n")

    metric_list.append("\nRandom Forest + Gradient Boosting (Auto):\n")

    metric_list.append(f"\t- Root Mean Squared Error: {rmse[3]:.2f}\n")
    metric_list.append(f"\t- Mean Absolute Percentage Error: {mape[3]*100:.2f}%\n")
    metric_list.append(f"\t- R-Squared: {r2[3]:.4f}\n")

    metric_list.append("\nAll:\n")

    metric_list.append(f"\t- Root Mean Squared Error: {rmse[4]:.2f}\n")
    metric_list.append(f"\t- Mean Absolute Percentage Error: {mape[4]*100:.2f}%\n")
    metric_list.append(f"\t- R-Squared: {r2[4]:.4f}\n")


    metric_list.append("\n\nData:\n")
    metric_list.append(f"\t- Training Instances: {size}\n")
    metric_list.append(f"\t- Testing Instances: {test_size}\n")
    metric_list.append(f"\t- Total Instances: {size+test_size}\n")

    metric_list.append("\n\nRanges:\n")
    metric_list.append(f"\t- DPM: {DPM_MIN} - {DPM_MAX}\n")
    metric_list.append(f"\t- APM: {APM_MIN} - {APM_MAX}\n")
    metric_list.append(f"\t- SR: {SR_MIN} - {SR_MAX}\n")

    metric_list.append("\n\nLast Update:\n")
    metric_list.append(f"{timestamp}\n")





    for item in metric_list:
        final_string += item

    return jsonify({
        'metrics': final_string,
        'date':date
        })

@app.route("/login", methods=["POST"])
def handle_login():
    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')

    usr_id = db.verify_login(username, password)


    if usr_id != -1:
        token = db.gen_token(usr_id)
        return jsonify({
            "status": "success",
            "token":token
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Username or password invalid, try again."
        })

@app.route("/register", methods=["POST"])
def handle_registration():
    data = request.get_json(force=True)
    usr = data.get("usr")

    usr = usr.strip()

    if not 3 <= len(usr) <= 20:
        return jsonify({
            "status": "error",
            "message": "Username must be between 3 and 20 characters long."
        })

    if not re.fullmatch(r'^[a-zA-Z0-9_-]+$', usr):
        return jsonify({
            "status": "error",
            "message": "Username can only contain letters, numbers, hyphens, and underscores."
        })
    
    if usr.lower() in ["admin", "root", "api", "tecsrcalc", "guest"]:
        return jsonify({
            "status": "error",
            "message": "Username invalid."
        })
    
    result = db.register_user(usr)

    if result["status"] == "error":
        return jsonify(result), 409
    
    return jsonify(result), 201
    
    



if __name__ == '__main__':
    # only runs when run locally
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")

