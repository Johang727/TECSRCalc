import joblib

metrics = [] # this will be the output txt file

MODEL_PATH = 'model.pkl'

try:
    model_mets = joblib.load(MODEL_PATH)

    mse = model_mets['mse']
    r2 = model_mets['r2']
    size = model_mets['size']
    tSize = model_mets['testSize']
    ts = model_mets['timestamp']
except FileNotFoundError: 
    print(f"Error: Model file \"{MODEL_PATH}\" not found!")

try:
    with open("README.md", "r") as readme:
        rd = readme.readlines()
except FileNotFoundError:
    print(f"Error: README.md not found!")

print(rd)

secStart = rd.index("<!--START_SECTION:metrics-->\n")
secEnd = rd.index("<!--END_SECTION:metrics-->\n")

for i in range(secStart+1, secEnd):
    # remove the previous metrics if they exist
    print(f"removing {rd[secStart+1]}")
    rd.pop(secStart+1)

#print(rd)

# append the before the start of the section
for meow in rd[:secStart+1]:
    metrics.append(meow)

# insert the metrics
metrics.append(f"\n - MSE: **{mse:.2f}**\n")
metrics.append(f" - R2: **{r2:.2f}**\n")
metrics.append(f" - Training Data: **{size}**\n")
metrics.append(f" - Testing Data: **{tSize}**\n")
metrics.append(f" - Timestamp: **{ts}**\n")

metrics.append("\n<!--END_SECTION:metrics-->\n")

# append everything after the readme
for meow in rd[secEnd-1:]:
    metrics.append(meow)

with open("README.md", "w") as readme:
    for meow in metrics:
        readme.write(f"{meow}")