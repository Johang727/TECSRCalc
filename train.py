import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import datetime

print("Merging CSV files together...")

dataFolder = "data/"

dfList = []

flareon:int = 136

testSize:float = 0.3

for fn in os.listdir(dataFolder):
    if fn.endswith(".csv"):
        fp = os.path.join(dataFolder, fn)
        df = pd.read_csv(fp, sep=";")
        dfList.append(df)

masterDF = pd.concat(dfList, ignore_index=True)

print(f"Length: {len(masterDF)}")

print("\nTraining started...")

x = masterDF[["Date", "DPM", "APM"]]
y = masterDF["SR"]

xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=testSize, random_state=flareon)

print("Training set size:", len(xTrain))
print("Testing set size:", len(xTest))

model = RandomForestRegressor(n_estimators=100, random_state=flareon)

model.fit(xTrain, yTrain)


yPred = model.predict(xTest)

mse = mean_squared_error(yTest, yPred)
r2 = r2_score(yTest, yPred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R-squared: {r2:.2f}")

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


metrics = {
    'model': model,
    'mse': mse,
    'r2': r2,
    'size': len(xTrain),
    'testSize': len(xTest),
    'timestamp': timestamp
}

print("Saving model...")
joblib.dump(metrics, "model.pkl")
print("Saved as \"model.pkl\"")