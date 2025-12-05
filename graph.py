import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joblib, sys, os


# set constants
MODEL_PATH:str = "model.pkl"
FEATURES:list[str] = ["Date", "DPM", "APM"]
GRAPH_FOLDER:str = f"{os.path.dirname(__file__)}/graphs/"


# load data
print(f"Attempting to load from {MODEL_PATH}")
model_mets = joblib.load(MODEL_PATH)
x = model_mets["dataX"]; y = model_mets["dataY"]

sr_counts = model_mets['srCounts']

predictions = model_mets["predictions"]
predictions_actual = model_mets["predictions_actual"]

print(predictions_actual)



sr_list:list[int] = [sr_counts.get('<1K SR'), sr_counts.get('1-2K SR'), sr_counts.get('2-3K SR'),
                    sr_counts.get('3-4K SR'), sr_counts.get('4-5K SR'), sr_counts.get('5-6K SR'),
                    sr_counts.get('6-7K SR'), sr_counts.get('7-8K SR'), sr_counts.get('8-9K SR'),
                    sr_counts.get('9-10K SR'), sr_counts.get('10-11K SR'), sr_counts.get('11-12K SR'),
                    sr_counts.get('12-13K SR'), sr_counts.get('13-14K SR'), sr_counts.get('14-15K SR'),
                    sr_counts.get('15-16K SR'), sr_counts.get('16-17K SR'), sr_counts.get('>17K SR')]

sr_percent:list[float] = [round((i/len(x))*100) for i in sr_list]

sr_labels:list[str] = ['<1', '1', '2', '3',
                        '4', '5', '6',
                        '7', '8', '9', '10',
                        '11','12', '13','14',
                        '15','16','+17']

print(sr_list)
print(sr_percent)
print(sr_labels)

# format data
df:pd.DataFrame = pd.DataFrame(x, columns=FEATURES); df["SR"] = y

# create APP data
df["APP"] = df["APM"] / df["DPM"]

print("Data loaded sucessfully\nNow drawing graph...")


print("Creating DPM graph...")
# create dpm graph base
fig, ax = plt.subplots(1, 1)

# make dpm graph
ax.scatter(df["SR"], df["DPM"], color="#FF5733", alpha=0.1)
ax.set_title("DPM vs. SR", fontsize=12)
ax.set_xlabel("Skill Rating (SR)")
ax.set_ylabel("Drops Per Minute (DPM)")
ax.grid(True, linestyle='--', alpha=0.6)

# fitting a line
z = np.polyfit(df["SR"], df["DPM"], 1) # 1 = linear
p = np.poly1d(z)
ax.plot(df["SR"].to_numpy(), p(df["SR"].to_numpy()), "r", linewidth=2)

# save graph
plt.savefig(f"{GRAPH_FOLDER}dpm.png", dpi=600)

# --- #
print("Creating APM graph...")
# create apm graph base
fig, ax = plt.subplots(1, 1)

# make apm graph
ax.scatter(df["SR"], df["APM"], color="#016583", alpha=0.1)
ax.set_title("APM vs. SR", fontsize=12)
ax.set_xlabel("Skill Rating (SR)")
ax.set_ylabel("Attack Per Minute (APM)")
ax.grid(True, linestyle='--', alpha=0.6)

# fitting a line
z = np.polyfit(df["SR"], df["APM"], 1) # 1 = linear
p = np.poly1d(z)
ax.plot(df["SR"].to_numpy(), p(df["SR"].to_numpy()), "r", linewidth=2)

# save graph
plt.savefig(f"{GRAPH_FOLDER}apm.png", dpi=600)

# --- #

print("Creating APP graph...")

# draw graph base
fig, ax = plt.subplots(1, 1)

# make app graph 
ax.scatter(df["SR"], df["APP"], color="#83016B", alpha=0.1)
ax.set_title("APP vs. SR", fontsize=12)
ax.set_xlabel("Skill Rating (SR)")
ax.set_ylabel("Attack Per Piece (APP)")
ax.grid(True, linestyle='--', alpha=0.6)

# app doesn't increase linearly, therefore, use poly line
z = np.polyfit(df["SR"].to_numpy(), df["APP"].to_numpy(), 2) 
p = np.poly1d(z)

# make sure my computer doesn't die
SRrange = np.linspace(df["SR"].min(), df["SR"].max(), 100) 
ax.plot(SRrange, p(SRrange), "r", linewidth=2)

# save app graph
plt.savefig(f"{GRAPH_FOLDER}app.png", dpi=600)

print("Creating SR graph...")

fig, ax = plt.subplots(1, 1)

fig.set_figwidth(8)

ax.bar(sr_labels, sr_list, color="orange")

ax.set_xlabel("SR Categories (in Ks)")
ax.set_ylabel("SR Count")
ax.set_title("SR Data")

plt.savefig(f"{GRAPH_FOLDER}data.png", dpi=600)


# --- #
print("Creating predictions for random forest graph...")
# create prediction graph base
fig, ax = plt.subplots(1, 1)

# make prediction graph
ax.scatter(predictions_actual, predictions[0], color="#016583", alpha=0.1)
ax.set_title("Random Forest Predictions", fontsize=12)
ax.set_xlabel("Actual Values")
ax.set_ylabel("Predicted Values")
ax.grid(True, linestyle='--', alpha=0.6)

# fitting a line
z = np.polyfit(predictions_actual, predictions[0], 1) # 1 = linear
p = np.poly1d(z)
ax.plot(predictions[0], p(predictions[0]), "r", linewidth=2)

# save graph
plt.savefig(f"{GRAPH_FOLDER}rf.png", dpi=600)

# --- #
print("Creating predictions for linear graph...")
# create prediction graph base
fig, ax = plt.subplots(1, 1)

# make prediction graph
ax.scatter(predictions_actual, predictions[1], color="#016583", alpha=0.1)
ax.set_title("Random Forest Predictions", fontsize=12)
ax.set_xlabel("Actual Values")
ax.set_ylabel("Predicted Values")
ax.grid(True, linestyle='--', alpha=0.6)

# fitting a line
z = np.polyfit(predictions_actual, predictions[1], 1) # 1 = linear
p = np.poly1d(z)
ax.plot(predictions[1], p(predictions[1]), "r", linewidth=2)

# save graph
plt.savefig(f"{GRAPH_FOLDER}lr.png", dpi=600)

# --- #
print("Creating predictions for gradient boosting graph...")
# create prediction graph base
fig, ax = plt.subplots(1, 1)

# make prediction graph
ax.scatter(predictions_actual, predictions[2], color="#016583", alpha=0.1)
ax.set_title("Random Forest Predictions", fontsize=12)
ax.set_xlabel("Actual Values")
ax.set_ylabel("Predicted Values")
ax.grid(True, linestyle='--', alpha=0.6)

# fitting a line
z = np.polyfit(predictions_actual, predictions[2], 1) # 1 = linear
p = np.poly1d(z)
ax.plot(predictions[2], p(predictions[2]), "r", linewidth=2)

# save graph
plt.savefig(f"{GRAPH_FOLDER}gb.png", dpi=600)

# --- #
print("Creating predictions for rf+gb graph...")
# create prediction graph base
fig, ax = plt.subplots(1, 1)

# make prediction graph
ax.scatter(predictions_actual, predictions[3], color="#016583", alpha=0.1)
ax.set_title("Random Forest Predictions", fontsize=12)
ax.set_xlabel("Actual Values")
ax.set_ylabel("Predicted Values")
ax.grid(True, linestyle='--', alpha=0.6)

# fitting a line
z = np.polyfit(predictions_actual, predictions[3], 1) # 1 = linear
p = np.poly1d(z)
ax.plot(predictions[3], p(predictions[3]), "r", linewidth=2)

# save graph
plt.savefig(f"{GRAPH_FOLDER}rfgb.png", dpi=600)

# --- #
print("Creating predictions for all graph...")
# create prediction graph base
fig, ax = plt.subplots(1, 1)

# make prediction graph
ax.scatter(predictions_actual, predictions[4], color="#016583", alpha=0.1)
ax.set_title("Random Forest Predictions", fontsize=12)
ax.set_xlabel("Actual Values")
ax.set_ylabel("Predicted Values")
ax.grid(True, linestyle='--', alpha=0.6)

# fitting a line
z = np.polyfit(predictions_actual, predictions[4], 1) # 1 = linear
p = np.poly1d(z)
ax.plot(predictions[4], p(predictions[4]), "r", linewidth=2)

# save graph
plt.savefig(f"{GRAPH_FOLDER}all.png", dpi=600)



print("Finished creating graphs!")


