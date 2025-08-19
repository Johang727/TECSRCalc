import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib



dataFolder = "data/"

dfList = []

for fn in os.listdir(dataFolder):
    if fn.endswith(".csv"):
        fp = os.path.join(dataFolder, fn)
        df = pd.read_csv(fp, sep=";")
        dfList.append(df)

masterDF = pd.concat(dfList, ignore_index=True)

print(f"Length: {len(masterDF)}")


x = masterDF[["DPM", "APM"]]
y = masterDF["SR"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

print("Training set size:", len(x_train))
print("Testing set size:", len(x_test))

model = RandomForestRegressor(n_estimators=100, random_state=42)

model.fit(x_train, y_train)


y_pred = model.predict(x_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R-squared: {r2:.2f}")

print("Saving model...")
joblib.dump(model, "model.pkl")
print("Saved as \"model.pkl\"")