import joblib
import sys 

metrics = [] # this will be the output txt file

MODEL_PATH = 'model.pkl'

try:
    model_mets = joblib.load(MODEL_PATH)

    RF_mse = model_mets['RF_mse']
    RF_r2 = model_mets['RF_r2']
    LR_mse = model_mets['LR_mse'],
    LR_r2 = model_mets['LR_r2']
    size = model_mets['size']
    tSize = model_mets['testSize']
    ts = model_mets['timestamp']
    srCounts = model_mets['srCounts']
except FileNotFoundError: 
    print(f"Error: Model file \"{MODEL_PATH}\" not found!")
    sys.exit(1)

try:
    with open("README.md", "r") as readme:
        rd = readme.readlines()
except FileNotFoundError:
    print(f"Error: README.md not found!")
    sys.exit(1)

#print(rd)

secStart = rd.index("<!--START_SECTION:metrics-->\n")
secEnd = rd.index("<!--END_SECTION:metrics-->\n")

for i in range(secStart+1, secEnd):
    # remove the previous metrics if they exist
    #print(f"removing {rd[secStart+1]}")
    rd.pop(secStart+1)

#print(rd)

# append the before the start of the section
for meow in rd[:secStart+1]:
    metrics.append(meow)

# insert the metrics
metrics.append(f"## Statistics:\n")

metrics.append(f" - Timestamp: **{ts}**\n")

metrics.append("\nRandom Forest Model:")

metrics.append(f"\n - MSE: **{RF_mse:.2f}**\n")
metrics.append(f" - R2: **{RF_r2:.4f}**\n")

metrics.append("\nLinear Model:")

metrics.append(f"\n - MSE: **{LR_mse[0]:.2f}**\n")
metrics.append(f" - R2: **{LR_r2:.4f}**\n")


metrics.append(f"\n## Data:\n")


metrics.append(f" - <1K SR: **{srCounts.get('<1K SR')}**\n")
metrics.append(f" - 1 - 2K SR: **{srCounts.get('1-2K SR')}**\n")
metrics.append(f" - 2 - 3K SR: **{srCounts.get('2-3K SR')}**\n")
metrics.append(f" - 3 - 4K SR: **{srCounts.get('3-4K SR')}**\n")
metrics.append(f" - 4 - 5K SR: **{srCounts.get('4-5K SR')}**\n")
metrics.append(f" - 5 - 6K SR: **{srCounts.get('5-6K SR')}**\n")
metrics.append(f" - 6 - 7K SR: **{srCounts.get('6-7K SR')}**\n")
metrics.append(f" - 7 - 8K SR: **{srCounts.get('7-8K SR')}**\n")
metrics.append(f" - 8 - 9K SR: **{srCounts.get('8-9K SR')}**\n")
metrics.append(f" - 9 - 10K SR: **{srCounts.get('9-10K SR')}**\n")
metrics.append(f" - 10 - 11K SR: **{srCounts.get('10-11K SR')}**\n")
metrics.append(f" - 11 - 12K SR: **{srCounts.get('11-12K SR')}**\n")
metrics.append(f" - 12 - 13K SR: **{srCounts.get('12-13K SR')}**\n")
metrics.append(f" - 13 - 14K SR: **{srCounts.get('13-14K SR')}**\n")
metrics.append(f" - 14 - 15K SR: **{srCounts.get('14-15K SR')}**\n")
metrics.append(f" - 15 - 16K SR: **{srCounts.get('15-16K SR')}**\n")
metrics.append(f" - 16 - 17K SR: **{srCounts.get('16-17K SR')}**\n")
metrics.append(f" - 17K+ SR: **{srCounts.get('>17K SR')}**\n")

metrics.append(f" - \n")

metrics.append(f" - Training Data: **{size}**\n")
metrics.append(f" - Testing Data: **{tSize}**\n")
metrics.append(f" - All Data: **{size+tSize}**\n")


metrics.append("\n<!--END_SECTION:metrics-->\n")

# append everything after the readme
for meow in rd[secEnd-1:]:
    metrics.append(meow)

with open("README.md", "w") as readme:
    for meow in metrics:
        readme.write(f"{meow}")