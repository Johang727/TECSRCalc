This branch is for testing an account system for easy uploading of images to contribute if you'd like. By default, you will be able to contribute without making an account.

There's not much made rn.

## TEC: SR Calculator
Aims to determine a player's estimated Skill Rating (SR) in Tetris Effect: Connected based on Attack Per Minute (APM) and Drops Per Minute (DPM). 

<details>
<summary>How is data collected?</summary>

- Match ends in Phase 3 (high rank)
- Match lasts 3 minutes or more (low rank)
- Less than 2000 SR difference between players
- Neither player has green SR

*Note: Data contained in old_data or similar files might not reflect this.*
</details>

<details>
<summary>Where did this data come from?</summary>

Streams on twitch.tv, personal matches and friend matches.

*Note: Data contains no usernames nor sources for anonymity. Even I cannot trace it back.*
</details>

<details>
<summary>Why only 2 (technically 3) features?</summary>

Tetris Effect: Connected only directly provides 5 metrics:
- Drops Per Minute (DPM); aka `Speed`
- Attack Per Minute (APM); aka `Attack`
- Zone Attack Per Minute (ZAPM)
    - Zone attack is a weird metric, as much as I'd like to include it, zoning in Phase 1 (the longest and easiest phase to zone in) and then never again can result in an over-inflated value.
    - Furthermore, since `ZAPM` only divides by time spent in zone, a zone can last a few frames, and as long as you scored just one line, you will have a `ZAPM` in the hundreds.
        - See below for some images:
            <details>
            <summary>Image from the Enhance Discord </summary>

            ![alt text](docs/images/image-1.png)
            </details>
    - These situations are rare, but it's not uncommon to see lots of ZAPM fluctuation.
- Score
    - Score determines the phase of the game. Lower rating players typically don't reach Phase 3 (60k points), and higher rating players reach it in a minute or two.
    - The reason this is not relevant is because efficiency is already dictated by APM/DPM.
- Time
    - No matter what rating you are, if you are against an evenly matched opponent, rounds can last 10 minutes or more. (The longest round I've had is 20 minutes, the shortest a few seconds)

If we expand these, we get:
- Attack Efficiency `(APP = APM/DPM)`
    - This was not included because it is directly related to the two main features.
- Score Efficiency `(Score/(DPM*Time))`
    - Very similar to attack efficiency, therefore is not included in the dataset.
    - Zone provides a higher boost in `Attack` than in `Score`, in a mode about trying to topout the other player, `Attack` is really what matters the most.


</details>


<!--START_SECTION:metrics-->
## Models:


*Last Update: 2025-12-05 10:47:58*
### Linear (Auto):
 - Root Mean Squared Error: 859.16
 - Mean Absolute Percentage Error: 8.53%
 - R-Squared: 0.9358

### Random Forest:
 - Root Mean Squared Error: 848.89
 - Mean Absolute Percentage Error: 7.11%
 - R-Squared: 0.9373

### Gradient Boosting:
 - Root Mean Squared Error: 844.09
 - Mean Absolute Percentage Error: 7.04%
 - R-Squared: 0.9380

### Random Forest + Gradient Boosting (Auto):
 - Root Mean Squared Error: 841.56
 - Mean Absolute Percentage Error: 7.00%
 - R-Squared: 0.9384

### All:
 - Root Mean Squared Error: 816.81
 - Mean Absolute Percentage Error: 7.25%
 - R-Squared: 0.9420

## Ranges:
 - DPM: 27.2 - 162.3
 - APM: 2.1 - 142.4
 - SR: 1431 - 17894

## Data:
 - Training: 1022 Points
 - Testing: 114 Points
 - All: 1136 Points

<!--END_SECTION:metrics-->
![SR Counts](graphs/data.png)


| Speed (DPM) vs. SR | Attack (APM) vs. SR | Efficiency (APP) vs. SR |
| :---: | :---: | :---: |
| ![DPM vs SR](graphs/dpm.png) | ![APM vs SR](graphs/apm.png) | ![APP vs SR](graphs/app.png) |

| Linear Predicted vs Real | Random Forest Predicted vs Real | Gradient Boosting Predicted vs Real | RF + GF Predicted vs Real | All Models' Predicted vs Real |
| :---: | :---: | :---: | :---: | :---: |
| ![Linear Predicted vs Real](graphs/lr.png) | | ![Random Forest Predicted vs Real](graphs/rf.png) | | ![Gradient Boosting Predicted vs Real](graphs/gb.png) | | ![RF + GB Predicted vs Real](graphs/rfgb.png) | | ![All Models' Predicted vs Real](graphs/lr.png) | 
