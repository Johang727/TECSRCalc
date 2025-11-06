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

# variables

# constants
RANDOM_STATE:int = 136
TEST_SIZE:float = 0.1
TREE_AMOUNT:int = 200
SR_BINS:list[int] = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000]
SR_LABELS:list[str] = ['<1K SR', '1-2K SR', '2-3K SR', '3-4K SR', '4-5K SR', '5-6K SR', '6-7K SR', '7-8K SR', '8-9K SR', '9-10K SR', '10-11K SR', '11-12K SR', '12-13K SR', '13-14K SR', '14-15K SR', '15-16K SR', '16-17K SR', '>17K SR']

# normal
# the goal is to have it in lists to compact it and make it easier to read.
dfList:list[pd.DataFrame] = []
mse:list[float] = []
r2:list[float] = []
models:list = []

# take all csvs from folder and combine them
for fn in os.listdir(dataFolder):
    if fn.endswith(".csv"):
        fp = os.path.join(dataFolder, fn)
        df = pd.read_csv(fp, sep=";")
        dfList.append(df)
masterDF:pd.DataFrame = pd.concat(dfList, ignore_index=True)

# count SR in each section
masterDF['SRBins'] = pd.cut(masterDF['SR'], bins=SR_BINS, labels=SR_LABELS, right=False)
srCounts:dict[str,int] = masterDF['SRBins'].value_counts().sort_index().to_dict()

# data amount
print(f"Instances: {len(masterDF)}")
print(f"Random state of {RANDOM_STATE} used.")


print("\nTraining started...\n")
x = masterDF[["Date", "DPM", "APM"]]
y = masterDF["SR"]

xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)


# print statistics for the SR column in the training set
print("\nTraining set SR statistics:")
print(f"  Min SR: {np.min(yTrain)}")
print(f"  Max SR: {np.max(yTrain)}")
print(f"  Mean SR: {np.mean(yTrain):.2f}")
print("---")

# print statistics for the SR column in the testing set
print("Testing set SR statistics:")
print(f"  Min SR: {np.min(yTest)}")
print(f"  Max SR: {np.max(yTest)}")
print(f"  Mean SR: {np.mean(yTest):.2f}\n")

# print instance sizes
print("Training set size:", len(xTrain))
print("Testing set size:", len(xTest))

# create models
models.append(RandomForestRegressor(n_estimators=TREE_AMOUNT, random_state=RANDOM_STATE))
models[0].fit(xTrain, yTrain)
models.append(LinearRegression())
models[1].fit(xTrain, yTrain)

# test models

# test random forest
yPred = models[0].predict(xTest)
mse.append(mean_squared_error(yTest, yPred))
r2.append(r2_score(yTest, yPred))

print("\n----\nTesting Random Forest\n")
print(f"Mean Squared Error: {mse[0]:.2f}")
print(f"R-squared: {r2[0]:.4f}")

# test linear 
yPred = models[1].predict(xTest)
mse.append(mean_squared_error(yTest, yPred))
r2.append(r2_score(yTest, yPred))

print("\n----\nTesting Linear\n")
print(f"Mean Squared Error: {mse[1]:.2f}")
print(f"R-squared: {r2[1]:.4f}")


timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

metrics = {
    'RFmodel': models[0],
    'RF_mse': mse[0],
    'RF_r2': r2[0],
    'LRmodel': models[1],
    'LR_mse': mse[1],
    'LR_r2': r2[1],
    'size': len(xTrain),
    'testSize': len(xTest),
    'timestamp': timestamp,
    'srCounts': srCounts,
    'dataX': x,
    'dataY': y
}

print("\n----\nSaving model...")
joblib.dump(metrics, "model.pkl")
print("Saved as \"model.pkl\"")


print("Generating graph..")


end = time.time()
print(f"Runtime: {end-start:.2f}s")

