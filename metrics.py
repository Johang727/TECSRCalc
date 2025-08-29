import joblib
import sys 

metrics:list[str] = [] # this will be the output txt file

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

allData:int = size+tSize

def make_graph(percent: float):
    """
    Make text progress bar.
    Length of the progress bar is 25 characters.

    :param percent: Completion percent of the progress bar.
    :return: The string progress bar representation.

    Taken from https://github.com/anmol098/waka-readme-stats
    """
    barLength:int = 25
    done_block, empty_block = "█", "░"
    percent_quart = round(percent / (100/barLength))
    return f"{done_block * percent_quart}{empty_block * (barLength - percent_quart)}"


srList:list[int] = [srCounts.get('<1K SR'), srCounts.get('1-2K SR'), srCounts.get('2-3K SR'),
                    srCounts.get('3-4K SR'), srCounts.get('4-5K SR'), srCounts.get('5-6K SR'),
                    srCounts.get('6-7K SR'), srCounts.get('7-8K SR'), srCounts.get('8-9K SR'),
                    srCounts.get('9-10K SR'), srCounts.get('10-11K SR'), srCounts.get('11-12K SR'),
                    srCounts.get('12-13K SR'), srCounts.get('13-14K SR'), srCounts.get('14-15K SR'),
                    srCounts.get('15-16K SR'), srCounts.get('16-17K SR'), srCounts.get('>17K SR')]

srPercent:list[float] = [round((x/allData)*100) for x in srList]

srLabelList:list[str] = ['<1K SR\t\t\t\t', '1 - 2K SR\t\t\t', '2 - 3K SR\t\t\t', '3 - 4K SR\t\t\t',
                        '4 - 5K SR\t\t\t', '5 - 6K SR\t\t\t', '6 - 7K SR\t\t\t',
                        '7 - 8K SR\t\t\t', '8 - 9K SR\t\t\t', '9 - 10K SR\t\t\t', '10 - 11K SR\t\t\t',
                        '11 - 12K SR\t\t\t','12 - 13K SR\t\t\t', '13 - 14K SR\t\t\t','14 - 15K SR\t\t\t',
                        '15 - 16K SR\t\t\t','16 - 17K SR\t\t\t','17K+ SR\t\t\t\t']



print(srPercent)

metrics.append("```text\n")


for i in range(len(srList)):
    metrics.append(f"{srLabelList[i]}{srList[i]} points\t\t{make_graph(srPercent[i])}\n")

"""metrics.append(f"<1K SR:\t\t\t\t{srList[0]} points\t\t{make_graph(srPercent[0])}\n")
metrics.append(f"1 - 2K SR:\t\t\t{srCounts.get('1-2K SR')} points\t\t{make_graph(srPercent[1])}\n") # TODO: finish completing these
metrics.append(f"2 - 3K SR:\t\t\t{srCounts.get('2-3K SR')} points\t\t\n")
metrics.append(f"3 - 4K SR:\t\t\t{srCounts.get('3-4K SR')} points\t\t\n")
metrics.append(f"4 - 5K SR:\t\t\t{srCounts.get('4-5K SR')} points\t\t\n")
metrics.append(f"5 - 6K SR:\t\t\t{srCounts.get('5-6K SR')} points\t\t\n")
metrics.append(f"6 - 7K SR:\t\t\t{srCounts.get('6-7K SR')} points\t\t\n")
metrics.append(f"7 - 8K SR:\t\t\t{srCounts.get('7-8K SR')} points\t\t\n")
metrics.append(f"8 - 9K SR:\t\t\t{srCounts.get('8-9K SR')} points\t\t\n")
metrics.append(f"9 - 10K SR:\t\t\t{srCounts.get('9-10K SR')} points\t\t\n")
metrics.append(f"10 - 11K SR:\t\t{srCounts.get('10-11K SR')} points\t\t\n")
metrics.append(f"11 - 12K SR:\t\t{srCounts.get('11-12K SR')} points\t\t\n")
metrics.append(f"12 - 13K SR:\t\t{srCounts.get('12-13K SR')} points\t\t\n")
metrics.append(f"13 - 14K SR:\t\t{srCounts.get('13-14K SR')} points\t\t\n")
metrics.append(f"14 - 15K SR:\t\t{srCounts.get('14-15K SR')} points\t\t\n")
metrics.append(f"15 - 16K SR:\t\t{srCounts.get('15-16K SR')} points\t\t\n")
metrics.append(f"16 - 17K SR:\t\t{srCounts.get('16-17K SR')} points\t\t\n")
metrics.append(f"17K+ SR:\t\t\t{srCounts.get('>17K SR')} points\t\t\n")
"""

metrics.append(f"\n")

metrics.append(f"Training Data:\t\t{size} points\t\t{make_graph((size/allData)*100)}\n")
metrics.append(f"Testing Data:\t\t{tSize} points\t\t{make_graph((tSize/allData)*100)}\n")
metrics.append(f"All Data:\t\t\t{allData} points\t\t{make_graph(100)}\n")

metrics.append("```")

metrics.append("\n<!--END_SECTION:metrics-->\n")

# append everything after the readme
for meow in rd[secEnd-1:]:
    metrics.append(meow)

with open("README.md", "w") as readme:
    for meow in metrics:
        readme.write(f"{meow}")