import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joblib


MODEL_PATH:str = "model.pkl"

FEATURES:list[str] = ["Date", "DPM", "APM"]

print(f"Attempting to load from {MODEL_PATH}")

model_mets = joblib.load(MODEL_PATH)

x = model_mets["dataX"]; y = model_mets["dataY"]

df:pd.DataFrame = pd.DataFrame(x, columns=FEATURES); df["SR"] = y

df["APP"] = df["APM"] / df["DPM"]

print("Dataframe loaded sucessfully\nNow drawing graph...")


fig, ax = plt.subplots(1, 1)

ax.scatter(df["SR"], df["DPM"], color="#FF5733", alpha=0.3)
ax.set_title("DPM vs. SR", fontsize=12)
ax.set_xlabel("Skill Rating (SR)")
ax.set_ylabel("Drops Per Minute (DPM)")
ax.grid(True, linestyle='--', alpha=0.6)

# apparently this fits a line?
z = np.polyfit(df["SR"], df["DPM"], 1) # 1 = linear
p = np.poly1d(z)
ax.plot(df["SR"], p(df["SR"]), "r", linewidth=2)

plt.savefig("dpm.png", dpi=600)



fig, ax = plt.subplots(1, 1)
ax.scatter(df["SR"], df["APM"], color="#016583", alpha=0.3)
ax.set_title("APM vs. SR", fontsize=12)
ax.set_xlabel("Skill Rating (SR)")
ax.set_ylabel("Attack Per Minute (APM)")
ax.grid(True, linestyle='--', alpha=0.6)

# apparently this fits a line?
z = np.polyfit(df["SR"], df["APM"], 1) # 1 = linear
p = np.poly1d(z)
ax.plot(df["SR"], p(df["SR"]), "r", linewidth=2)


plt.savefig("apm.png", dpi=600)



fig, ax = plt.subplots(1, 1)
ax.scatter(df["SR"], df["APP"], color="#83016B", alpha=0.3)
ax.set_title("APP vs. SR", fontsize=12)
ax.set_xlabel("Skill Rating (SR)")
ax.set_ylabel("Attack Per Piece (APM)")
ax.grid(True, linestyle='--', alpha=0.6)

# apparently this fits a line?
z = np.polyfit(df["SR"], df["APP"], 2) # 2 = polynomial
p = np.poly1d(z)

SRrange = np.linspace(df["SR"].min(), df["SR"].max(), 100)

ax.plot(SRrange, p(SRrange), "r", linewidth=2)


plt.savefig("app.png", dpi=600)



