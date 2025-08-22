import joblib

metrics:list[str] = [] # this will be the output txt file

MODEL_PATH:str = 'model.pkl'

try:
    model_mets = joblib.load(MODEL_PATH)

    metrics.append(round(model_mets['mse'], 2))
    metrics.append(round(model_mets['r2'], 2))
    metrics.append(model_mets['size'])
    metrics.append(model_mets['testSize'])
    metrics.append(model_mets['timestamp'])
except FileNotFoundError: 
    print(f"Error: Model file \"{MODEL_PATH}\" not found!")

with open("metrics.txt", "w") as outFile:
    for item in metrics:
        print(item)