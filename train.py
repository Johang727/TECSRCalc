import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import datetime
import time
import numpy as np

start = time.time()

print("Merging CSV files together...")

dataFolder = "data/"

dfList = []

flareon = 136

testSize = 0.1

treeAmount = 200

for fn in os.listdir(dataFolder):
    if fn.endswith(".csv"):
        fp = os.path.join(dataFolder, fn)
        df = pd.read_csv(fp, sep=";")
        dfList.append(df)

masterDF = pd.concat(dfList, ignore_index=True)

srBins = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000]

srLabels = ['<1K SR', '1-2K SR', '2-3K SR', '3-4K SR', '4-5K SR', '5-6K SR', '6-7K SR', '7-8K SR', '8-9K SR', '9-10K SR', '10-11K SR', '11-12K SR', '12-13K SR', '13-14K SR', '14-15K SR', '15-16K SR', '16-17K SR', '>17K SR']

masterDF['SRBins'] = pd.cut(masterDF['SR'], bins=srBins, labels=srLabels, right=False)

srCounts = masterDF['SRBins'].value_counts().sort_index().to_dict()

print(srCounts)



print(f"Length: {len(masterDF)}")

print(f"Random state of {flareon} used.")

print("\nTraining started...\n")

x = masterDF[["Date", "DPM", "APM"]]
y = masterDF["SR"]

xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=testSize, random_state=flareon)


# Print statistics for the SR column in the training set
print("\nTraining set SR statistics:")
print(f"  Min SR: {np.min(yTrain)}")
print(f"  Max SR: {np.max(yTrain)}")
print(f"  Mean SR: {np.mean(yTrain):.2f}")
print("---")

# Print statistics for the SR column in the testing set
print("Testing set SR statistics:")
print(f"  Min SR: {np.min(yTest)}")
print(f"  Max SR: {np.max(yTest)}")
print(f"  Mean SR: {np.mean(yTest):.2f}\n")


print("Training set size:", len(xTrain))
print("Testing set size:", len(xTest))

rfmodel = RandomForestRegressor(n_estimators=treeAmount, random_state=flareon)

rfmodel.fit(xTrain, yTrain)

lrmodel = LinearRegression()

lrmodel.fit(xTrain, yTrain)

yPred = rfmodel.predict(xTest)


mse0 = mean_squared_error(yTest, yPred)
r20 = r2_score(yTest, yPred)

print("\nTesting Random Forest\n")
print(f"Mean Squared Error: {mse0:.2f}")
print(f"R-squared: {r20:.4f}")

yPred = lrmodel.predict(xTest)

mse1 = mean_squared_error(yTest, yPred)
r21 = r2_score(yTest, yPred)

print("\nTesting Linear\n")
print(f"Mean Squared Error: {mse1:.2f}")
print(f"R-squared: {r21:.4f}")

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


metrics = {
    'RFmodel': rfmodel,
    'RF_mse': mse0,
    'RF_r2': r20,
    'LRmodel': lrmodel,
    'LR_mse': mse1,
    'LR_r2': r21,
    'size': len(xTrain),
    'testSize': len(xTest),
    'timestamp': timestamp,
    'srCounts': srCounts
}

print("Saving model...")
joblib.dump(metrics, "model.pkl")
print("Saved as \"model.pkl\"")

end = time.time()

print(f"Runtime: {end-start:.2f}s")