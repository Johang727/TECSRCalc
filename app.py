# This script was created by AI

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
    model_mets = joblib.load(MODEL_PATH)
    model = model_mets['model']
    mse = model_mets['mse']
    r2 = model_mets['r2']
    size = model_mets['size']
    timestamp = model_mets['timestamp']
    print("Trained model loaded successfully.")
except FileNotFoundError:
    print(f"Error: Model file '{MODEL_PATH}' not found. Please run train_model.py first.")
    model = None

@app.route('/')
def home():
    """Serves the main web page (index.html)."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handles the prediction request from the web page."""
    # Check if the model was loaded successfully
    if model is None:
        return jsonify({'error': 'Model not available. Please contact the administrator.'}), 500

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
    predicted_sr = round(prediction[0], 2)

    # Return the prediction as a JSON response
    return jsonify({'predicted_sr': predicted_sr})

@app.route('/metrics')
def metrics():
    """Serves the model performance metrics."""
    if model is None:
        return jsonify({'error': 'Metrics not available.'})
    
    return jsonify({
        'mse': round(mse, 2),
        'r2': round(r2, 2),
        'size': size,
        'timestamp': timestamp
    })

if __name__ == '__main__':
    # Make sure the app runs in development mode
    app.run(debug=True)

