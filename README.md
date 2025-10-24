## About
Small project I decided to start to determine estimated SR based off of APM and DPM. 

There is a hidden timestamp value that, essentially, accounts for SR inflation.

Data was collected from streams on twitch.tv and personal games, no personal data in disclosed, just SR, APM, and DPM.

I aim to collect the following data to avoid unrepresentative data:
 - Match ends in Phase 3 (high rank)
 - Match lasts at least 3 minutes (low rank)
    - Lower rating players typically don't make it to Phase 3
 - <2K difference between players

Note: Data contained in old_data or similar files might not reflect this.


<!--START_SECTION:metrics-->
## Statistics:
 - Timestamp: **2025-08-26 02:55:54**

Random Forest Model:
 - MSE: **951846.09**
 - R2: **0.8872**

Linear Model:
 - MSE: **1428654.98**
 - R2: **0.8307**

## Data:
```text
<1K SR				0 points		░░░░░░░░░░░░░░░░░░░░░░░░░
1 - 2K SR			7 points		░░░░░░░░░░░░░░░░░░░░░░░░░
2 - 3K SR			19 points		░░░░░░░░░░░░░░░░░░░░░░░░░
3 - 4K SR			44 points		█░░░░░░░░░░░░░░░░░░░░░░░░
4 - 5K SR			42 points		█░░░░░░░░░░░░░░░░░░░░░░░░
5 - 6K SR			31 points		█░░░░░░░░░░░░░░░░░░░░░░░░
6 - 7K SR			59 points		██░░░░░░░░░░░░░░░░░░░░░░░
7 - 8K SR			49 points		█░░░░░░░░░░░░░░░░░░░░░░░░
8 - 9K SR			125 points		███░░░░░░░░░░░░░░░░░░░░░░
9 - 10K SR			116 points		███░░░░░░░░░░░░░░░░░░░░░░
10 - 11K SR			342 points		████████░░░░░░░░░░░░░░░░░
11 - 12K SR			49 points		█░░░░░░░░░░░░░░░░░░░░░░░░
12 - 13K SR			27 points		█░░░░░░░░░░░░░░░░░░░░░░░░
13 - 14K SR			31 points		█░░░░░░░░░░░░░░░░░░░░░░░░
14 - 15K SR			16 points		░░░░░░░░░░░░░░░░░░░░░░░░░
15 - 16K SR			0 points		░░░░░░░░░░░░░░░░░░░░░░░░░
16 - 17K SR			22 points		░░░░░░░░░░░░░░░░░░░░░░░░░
17K+ SR				17 points		░░░░░░░░░░░░░░░░░░░░░░░░░

Training Data:		896 points		██████████████████████░░░
Testing Data:		100 points		███░░░░░░░░░░░░░░░░░░░░░░
All Data:			996 points		█████████████████████████
```
<!--END_SECTION:metrics-->
