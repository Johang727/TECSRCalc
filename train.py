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

excelStart = datetime.date(1900, 1, 1)


for fn in os.listdir(dataFolder):
    if fn.endswith(".csv"):
        fp = os.path.join(dataFolder, fn)
        # We now explicitly parse the 'Date' column and handle potential errors
        df = pd.read_csv(fp, sep=";", parse_dates=['Date'])
        # If pandas fails, we'll try to convert it manually with the correct format
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce').fillna(
            pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce'))
        
        # Convert to number of days since Excel's epoch, then add 2
        df['Date'] = (df['Date'].dt.date - excelStart).dt.days + 2

        dfList.append(df)

masterDF = pd.concat(dfList, ignore_index=True)

print(f"Length: {len(masterDF)}")

print("\nTraining started...")

x = masterDF[["Date", "DPM", "APM"]]
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

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


metrics = {
    'model': model,
    'mse': mse,
    'r2': r2,
    'size': len(x_train),
    'timestamp': timestamp
}

print("Saving model...")
joblib.dump(metrics, "model.pkl")
print("Saved as \"model.pkl\"")