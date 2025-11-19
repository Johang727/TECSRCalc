import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neural_network import MLPRegressor
import joblib
import datetime
import time
import numpy as np
import sys
from scipy import stats



start = time.time()

print("Merging CSV files together...")


# variables

DATA_FOLDER = "data/SRCalc/"
RANDOM_STATE:int = 136
TEST_SIZE:float = 0.1
TREE_AMOUNT:int = 200
SR_BINS:list[int] = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000]
SR_LABELS:list[str] = ['<1K SR', '1-2K SR', '2-3K SR', '3-4K SR', '4-5K SR', '5-6K SR', '6-7K SR', '7-8K SR', '8-9K SR', '9-10K SR', '10-11K SR', '11-12K SR', '12-13K SR', '13-14K SR', '14-15K SR', '15-16K SR', '16-17K SR', '>17K SR']

dfList:list[pd.DataFrame] = []
mse:list[float] = []
r2:list[float] = []
models:list = []

# take all csvs from folder and combine them
for fn in os.listdir(DATA_FOLDER):
    if fn.endswith(".csv"):
        fp = os.path.join(DATA_FOLDER, fn)
        df = pd.read_csv(fp, sep=";")
        dfList.append(df)
masterDF:pd.DataFrame = pd.concat(dfList, ignore_index=True)

old_instances:int = len(masterDF)

numeric_df = masterDF.select_dtypes(include=np.number)

q1 = numeric_df.quantile(.25); q3 = numeric_df.quantile(.75)
iqr = q3 - q1

lower_bounds = q1 - 2.5 * iqr
upper_bounds = q3 + 2.5 * iqr

iqr_mask = ((numeric_df >= lower_bounds) & (numeric_df <= upper_bounds)).all(axis=1) & (masterDF["APM"] > 0.0)

iqr_mask = iqr_mask
masterDF = masterDF[iqr_mask]

print("Apparently outliers are dropped?")

# data amount
print(f"Instances: {len(masterDF)}")
print(f"Outliers Removed: {len(masterDF) - old_instances}")

# count SR in each section
masterDF['SRBins'] = pd.cut(masterDF['SR'], bins=SR_BINS, labels=SR_LABELS, right=False)
srCounts:dict[str,int] = masterDF['SRBins'].value_counts().sort_index().to_dict()

print(srCounts)


print("\nTraining started...\n")
x = masterDF[["Date", "DPM", "APM"]]
y = masterDF["SR"]

xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=masterDF["SRBins"])


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
models.append(RandomForestRegressor(n_estimators=TREE_AMOUNT, random_state=RANDOM_STATE, n_jobs=-1))
models[0].fit(xTrain, yTrain)
models.append(LinearRegression())
models[1].fit(xTrain, yTrain)
models.append(GradientBoostingRegressor(n_estimators=TREE_AMOUNT, random_state=RANDOM_STATE))
models[2].fit(xTrain, yTrain)

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

# test Gradient Boosting Regressor
yPred = models[2].predict(xTest)
mse.append(mean_squared_error(yTest, yPred))
r2.append(r2_score(yTest, yPred))

print("\n----\nTesting Gradient Boosting\n")
print(f"Mean Squared Error: {mse[2]:.2f}")
print(f"R-squared: {r2[2]:.4f}")



timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

metrics = {
    'models':models,
    'r2':r2,
    'mse':mse,
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

