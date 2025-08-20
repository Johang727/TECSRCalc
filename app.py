from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS
import datetime

# Create the Flask application instance
app = Flask(__name__, static_folder='docs', template_folder='docs')
CORS(app, origins="https://johang727.github.io")

# Load the trained model when the application starts
# This is more efficient than loading it for every request
MODEL_PATH = 'model.pkl'


try:
    # fetch and store variables from the packaged model
    print("Attempting to load model...")
    model_mets = joblib.load(MODEL_PATH)
    model = model_mets['model']
    mse = model_mets['mse']
    r2 = model_mets['r2']
    size = model_mets['size']
    timestamp = model_mets['timestamp']
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
    if model is None:
        return jsonify({'error': 'Model file not found!'}), 500
    # From what I understand 500 errors are server-side; 400 are client-side
    # TODO, have it redirect to a new page with contact information

    # Get the data sent from the web page
    data = request.get_json(force=True)
    dpm = data.get('dpm')
    apm = data.get('apm')

    # Basic input validation
    if dpm is None or apm is None:
        return jsonify({'error': 'Missing DPM or APM values.'}), 400
    try:
        dpm = float(dpm)
        apm = float(apm)
        excel_start = datetime.date(1900, 1, 1)
        today = datetime.date.today()
        date_int = (today - excel_start).days + 2
    except ValueError:
        return jsonify({'error': 'Invalid input. Please provide numbers.'}), 400

    # Create a pandas DataFrame for the prediction
    # The model expects the data in this format
    input_data = pd.DataFrame([[date_int, dpm, apm]], columns=['Date','DPM', 'APM'])

    # Make the prediction
    prediction = model.predict(input_data)
    predicted_sr = round(prediction[0])

    # Return the prediction as a JSON response
    return jsonify({'predicted_sr': predicted_sr})

@app.route('/metrics')
def metrics():
    if model is None:
        return jsonify({'error': 'Model file not found!'}), 500
    
    return jsonify({
        'mse': round(mse, 2),
        'r2': round(r2, 2),
        'size': size,
        'timestamp': timestamp
    })

if __name__ == '__main__':
    # only runs when run locally
    app.run(debug=True)

