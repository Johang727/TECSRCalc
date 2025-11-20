import pandas as pd
import os, time, datetime, joblib, sys
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, VotingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import root_mean_squared_error, r2_score, mean_absolute_percentage_error, mean_squared_error
import numpy as np




start = time.time()

print("Merging CSV files together...")

# variables
# --------------------------------

DATA_FOLDER = "data/SRCalc/"
RANDOM_STATE:int = 136
TEST_SIZE:float = 0.1
TREE_AMOUNT:int = 200
SR_BINS:list[int] = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000]
SR_LABELS:list[str] = ['<1K SR', '1-2K SR', '2-3K SR', '3-4K SR', '4-5K SR', '5-6K SR', '6-7K SR', '7-8K SR', '8-9K SR', '9-10K SR', '10-11K SR', '11-12K SR', '12-13K SR', '13-14K SR', '14-15K SR', '15-16K SR', '16-17K SR', '>17K SR']

dfList:list[pd.DataFrame] = []
rmse:list[float] = []
r2:list[float] = []
mape:list[float] = []
models:list = []
predictions:list = []
# --------------------------------


# merging CSVs in data folder
# --------------------------------

for fn in os.listdir(DATA_FOLDER):
    if fn.endswith(".csv"):
        fp = os.path.join(DATA_FOLDER, fn)
        df = pd.read_csv(fp, sep=";")
        dfList.append(df)
masterDF:pd.DataFrame = pd.concat(dfList, ignore_index=True)
# --------------------------------


# dropping outliers 
# TODO: could be better tbh, doesn't seem to remove some extreme variation in 11k games
# --------------------------------

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
# --------------------------------


# data counting 
# --------------------------------

print(f"Instances: {len(masterDF)}")
print(f"Outliers Removed: {len(masterDF) - old_instances}")


# count SR in each section
masterDF['SRBins'] = pd.cut(masterDF['SR'], bins=SR_BINS, labels=SR_LABELS, right=False)
srCounts:dict[str,int] = masterDF['SRBins'].value_counts().sort_index().to_dict()

print(srCounts)
# --------------------------------


# data splitting + prep
# --------------------------------
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
# --------------------------------

# create Random Forest model:
# --------------------------------
if False:
    print("Training many Random Forests to see which is best...")
    # essentially try a ton of things for our random forest and see which is best

    # first run gave me depth:10, features:sqrt, min_samples_split: 2, n_estimators: 50
    # second run which took 20m gave me depth: None, features, sqrt, min_samples: 3, estimators: 79

    # Best Parameters: {'max_depth': None, 'max_features': 'sqrt', 'min_samples_split': 3, 'n_estimators': 79}

    param_grid = {
        'n_estimators': [x for x in range(45, 86, 1)],
        'max_depth': [10, 20, None],
        'min_samples_split': [2,3,4],
        'max_features': ["sqrt"]
    }

    rf = RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1)

    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        scoring="neg_mean_squared_error",
        n_jobs=-1,
        verbose=3
    )

    grid_search.fit(xTrain, yTrain)

    best_params = grid_search.best_params_

    print(f"Best Parameters: {best_params}")

    best_rf = grid_search.best_estimator_

    models.append(best_rf)
else:
    models.append(RandomForestRegressor(n_jobs=-1, 
                                        random_state=RANDOM_STATE, 
                                        max_depth=None,
                                        max_features="sqrt",
                                        min_samples_split=3,
                                        n_estimators=79
                                        ))



# create the Linear:
# --------------------------------

models.append(LinearRegression(n_jobs=-1))
# --------------------------------

# create Gradient Boost model:
# --------------------------------

if False:

    # run 1
    # Best Parameters: {'alpha': 0.5, 'learning_rate': 0.01, 'loss': 'squared_error', 'max_depth': 10, 'max_features': 'sqrt', 'min_impurity_decrease': 1.0, 'min_samples_split': 3, 'n_estimators': 500, 'subsample': 0.8}

    # run 2
    # Best Parameters: {'alpha': 0.5, 'learning_rate': 0.005, 'loss': 'squared_error', 'max_depth': 8, 'max_features': 'sqrt', 'min_impurity_decrease': 2.0, 'min_samples_split': 3, 'n_estimators': 1000, 'subsample': 0.5}

    # run 3
    # Best Parameters: {'learning_rate': 0.006, 'loss': 'squared_error', 'max_depth': 7, 'max_features': 'sqrt', 'min_impurity_decrease': 1.75, 'min_samples_split': 3, 'n_estimators': 900, 'subsample': 0.75}
    # Root Mean Squared Error: 712.57

    param_grid_gb = {
        'learning_rate':[0.0055, 0.006, 0.007],
        'n_estimators': [850, 900, 950],
        'max_depth': [6, 7, 8],
        'min_samples_split': [3],
        'max_features': ["sqrt"],
        'min_impurity_decrease':[1.5, 1.75, 1.9],
        'loss':["squared_error"],
        'subsample':[0.6, 0.75, 0.8],
    }

    gb = GradientBoostingRegressor(random_state=RANDOM_STATE)

    grid_search_gb = GridSearchCV(
        estimator=gb,
        param_grid=param_grid_gb,
        scoring="neg_mean_squared_error",
        n_jobs=-1,
        verbose=3
    )

    try:
        grid_search_gb.fit(xTrain, yTrain)
    except KeyboardInterrupt:
        print("\n--- Search Interrupted (Ctrl+C) | Press again to force.---")
        
        if hasattr(grid_search_gb, 'cv_results_') and len(grid_search_gb.cv_results_['mean_test_score']) > 0:
            
            best_index = grid_search_gb.cv_results_['mean_test_score'].argmax()
            
            best_score_neg_mse = grid_search_gb.cv_results_['mean_test_score'][best_index]
            best_params = grid_search_gb.cv_results_['params'][best_index]
            best_rmse = np.sqrt(-best_score_neg_mse)

            print(f"Best RMSE (so far): {best_rmse:.2f}")
            print(f"Best Parameters: {best_params}")
        else:
            print("No combinations were fully completed, LL")
            sys.exit(1)

    best_params = grid_search_gb.best_params_

    print(f"Best Parameters: {best_params}")

    best_gb = grid_search_gb.best_estimator_


    models.append(best_gb)
else:
    models.append(GradientBoostingRegressor(
        learning_rate=0.006,
        loss="squared_error",
        max_depth=7,
        min_samples_split=3,
        max_features="sqrt",
        min_impurity_decrease=1.75,
        n_estimators=900,
        subsample=0.75,
        random_state=RANDOM_STATE
    ))

# --------------------------------

# create ensemble of the two trees, these are really good at interpolation, not extra.
# --------------------------------

models.append(VotingRegressor(
    estimators=[
        ("rf", models[0]),
        ("gb", models[2])
    ],
    n_jobs=-1
))

# --------------------------------



# fit the models
# --------------------------------
if not False: # this seems dumb, but False is the placeholder for a flag or something to re-search later
        models[0].fit(xTrain, yTrain)
        models[1].fit(xTrain, yTrain)
        models[2].fit(xTrain, yTrain)
        models[3].fit(xTrain, yTrain) # i dunno how imma do this one if i do the searching; something to figure out later.

# test the models performance
# --------------------------------

# test random forest
# --------------------------------

print("\n----\nTesting Random Forest\n")


predictions.append(models[0].predict(xTest))
rmse.append(root_mean_squared_error(yTest, predictions[0]))
r2.append(r2_score(yTest, predictions[0]))
mape.append(mean_absolute_percentage_error(yTest, predictions[0]))

print(f"Root Mean Squared Error: {rmse[0]:.2f}")
print(f"R-squared: {r2[0]:.4f}")
print(f"Mean Absolute Percentage Error: {mape[0]:.2f}")
# --------------------------------

# test linear 
# --------------------------------

print("\n----\nTesting Linear\n")

predictions.append(models[1].predict(xTest))

rmse.append(root_mean_squared_error(yTest, predictions[1]))
r2.append(r2_score(yTest, predictions[1]))
mape.append(mean_absolute_percentage_error(yTest, predictions[1]))

print(f"Root Mean Squared Error: {rmse[1]:.2f}")
print(f"R-squared: {r2[1]:.4f}")
print(f"Mean Absolute Percentage Error: {mape[1]:.2f}")

# test Gradient Boosting Regressor
# --------------------------------

print("\n----\nTesting Gradient Boosting\n")

predictions.append(models[2].predict(xTest))

rmse.append(root_mean_squared_error(yTest, predictions[2]))
r2.append(r2_score(yTest, predictions[2]))
mape.append(mean_absolute_percentage_error(yTest, predictions[2]))


print(f"Root Mean Squared Error: {rmse[2]:.2f}")
print(f"R-squared: {r2[2]:.4f}")
print(f"Mean Absolute Percentage Error: {mape[2]:.2f}")

# --------------------------------

# test All Ensemble
# --------------------------------

print("\n----\nTesting RF + GB\n")

predictions.append(models[3].predict(xTest))

rmse.append(root_mean_squared_error(yTest, predictions[3]))
r2.append(r2_score(yTest, predictions[3]))
mape.append(mean_absolute_percentage_error(yTest, predictions[3]))


print(f"Root Mean Squared Error: {rmse[3]:.2f}")
print(f"R-squared: {r2[3]:.4f}")
print(f"Mean Absolute Percentage Error: {mape[3]:.2f}")

# --------------------------------



timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

metrics = {
    'models':models,
    'r2':r2,
    'rmse':rmse,
    'mape':mape,
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

