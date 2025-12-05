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


*Last Update: 2025-12-04 20:30:54*
### Linear (Auto):
 - Root Mean Squared Error: 949.43
 - Mean Absolute Percentage Error: 10.34%
 - R-Squared: 0.9108

### Random Forest:
 - Root Mean Squared Error: 851.49
 - Mean Absolute Percentage Error: 7.73%
 - R-Squared: 0.9283

### Gradient Boosting:
 - Root Mean Squared Error: 878.01
 - Mean Absolute Percentage Error: 7.51%
 - R-Squared: 0.9237

### Random Forest + Gradient Boosting (Auto):
 - Root Mean Squared Error: 859.68
 - Mean Absolute Percentage Error: 7.59%
 - R-Squared: 0.9269

### All:
 - Root Mean Squared Error: 831.76
 - Mean Absolute Percentage Error: 8.23%
 - R-Squared: 0.9315

## Ranges:
 - DPM: 29.6 - 162.3
 - APM: 4.4 - 142.4
 - SR: 1944 - 17894

## Data:
 - Training: 980 Points
 - Testing: 109 Points
 - All: 1089 Points

<!--END_SECTION:metrics-->
![SR Counts](graphs/data.png)


| Speed (DPM) vs. SR | Attack (APM) vs. SR | Efficiency (APP) vs. SR |
| :---: | :---: | :---: |
| ![DPM vs SR](graphs/dpm.png) | ![APM vs SR](graphs/apm.png) | ![APP vs SR](graphs/app.png) |