import joblib
import sys 

metrics:list[str] = [] # this will be the output txt file

MODEL_PATH = 'model.pkl'

try:
    model_mets = joblib.load(MODEL_PATH)

    r2 = model_mets['r2']
    rmse = model_mets['rmse']
    mape = model_mets['mape']


    size = model_mets['size']
    test_size = model_mets['testSize']
    ts = model_mets['timestamp']
    srCounts = model_mets['srCounts']

    x = model_mets['dataX']
    y = model_mets['dataY']


except FileNotFoundError: 
    print(f"Error: Model file \"{MODEL_PATH}\" not found!")
    sys.exit(1)

try:
    with open("README.md", "r", encoding="utf-8") as readme:
        rd = readme.readlines()
except FileNotFoundError:
    print(f"Error: README.md not found!")
    sys.exit(1)

DPM_MIN = x["DPM"].min()
DPM_MAX = x["DPM"].max()

APM_MIN = x["APM"].min()
APM_MAX = x["APM"].max()

SR_MIN = y.min()
SR_MAX = y.max()


#print(rd)

secStart = rd.index("<!--START_SECTION:metrics-->\n")
secEnd = rd.index("<!--END_SECTION:metrics-->\n")

# append the before the start of the section
for line in rd[:secStart+1]:
    metrics.append(line)

# insert the metrics
metrics.append(f"## Models:\n")

metrics.append(f"\n\n*Last Update: {ts}*\n")

metrics.append("### Linear (Auto):\n")

metrics.append(f" - Root Mean Squared Error: {rmse[1]:.2f}\n")
metrics.append(f" - Mean Absolute Percentage Error: {mape[1]*100:.2f}%\n")
metrics.append(f" - R-Squared: {r2[1]:.4f}\n")

metrics.append("\n### Random Forest:\n")

metrics.append(f" - Root Mean Squared Error: {rmse[0]:.2f}\n")
metrics.append(f" - Mean Absolute Percentage Error: {mape[0]*100:.2f}%\n")
metrics.append(f" - R-Squared: {r2[0]:.4f}\n")

metrics.append("\n### Gradient Boosting:\n")

metrics.append(f" - Root Mean Squared Error: {rmse[2]:.2f}\n")
metrics.append(f" - Mean Absolute Percentage Error: {mape[2]*100:.2f}%\n")
metrics.append(f" - R-Squared: {r2[2]:.4f}\n")

metrics.append("\n### Random Forest + Gradient Boosting (Auto):\n")

metrics.append(f" - Root Mean Squared Error: {rmse[3]:.2f}\n")
metrics.append(f" - Mean Absolute Percentage Error: {mape[3]*100:.2f}%\n")
metrics.append(f" - R-Squared: {r2[3]:.4f}\n")


metrics.append("\n### All:\n")

metrics.append(f" - Root Mean Squared Error: {rmse[4]:.2f}\n")
metrics.append(f" - Mean Absolute Percentage Error: {mape[4]*100:.2f}%\n")
metrics.append(f" - R-Squared: {r2[4]:.4f}\n")

metrics.append("\n## Ranges:\n")
metrics.append(f" - DPM: {DPM_MIN} - {DPM_MAX}\n")
metrics.append(f" - APM: {APM_MIN} - {APM_MAX}\n")
metrics.append(f" - SR: {SR_MIN} - {SR_MAX}\n")


metrics.append(f"\n## Data:\n")

all_data:int = size+test_size

metrics.append(f" - Training: {size} Points\n")
metrics.append(f" - Testing: {test_size} Points\n")
metrics.append(f" - All: {all_data} Points\n")


metrics.append("\n<!--END_SECTION:metrics-->\n")

# append everything after the readme
for item in rd[secEnd+1:]:
    metrics.append(item)

with open("README.md", "w", encoding="utf-8") as readme:
    for item in metrics:
        readme.write(f"{item}")

