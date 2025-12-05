I initially tried this code block:

```python
# stole this from stack overflow

numeric_df = masterDF.select_dtypes(include=np.number)

outlier_mask = (np.abs(stats.zscore(numeric_df)) < 3).all(axis=1)

masterDF = masterDF[outlier_mask][masterDF["APM"] > 0]
```

but the issue was:
- it removed a lot of the high end plays and def not some of the 11k plays that could've been removed.


I did the IQR stuff, yet I feel like it still lacks and could be removing more from 11K. Although variation is quite high regardless.


------

GridSearchCV arc:

Essentially, I just put a ton of broad numbers for Random Forest (see previous commits) then the range for a more specific one:
    This resulted in a higher accuracy and lower error, so WW

Trying the same for Gradient Boosting, letting it run overnight since it's a LOT of combos, even for the simple one.
    GBs are more complex, taking upwards of 10 seconds or more per test when compared to the RFs

I don't think I can really adjust anything for linear.. it's just linear :p

All of them together:
 - I dunno, might do better for extrapolation, but I think it's better to combine the two forests?
 - Decided to combine the two forests for auto, rather than all 3



Bots:



Lv8: 5183 SR

DPM: 50.8 49.7 49.3 49.5 | AVG: 49.8
APM: 32.8 23.9 28.5 30.3 | AVG: 28.9

Lv9: 6496 SR

DPM: 64.7 61.5 63.0 62.7 | 63
APM: 35.8 32.8 34.8 32.3 | 33.9

Lv10: 9605 SR

DPM: 91.1 92.9 92.0 92.8 86.6 | 91.1
APM: 50.1 58.3 60.2 51.9 47.1 | 53.5

Lv10+1:

DPM: 90.6 92.8
APM: 76.2 73.0