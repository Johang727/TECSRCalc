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

print("Finished creating graphs!")


