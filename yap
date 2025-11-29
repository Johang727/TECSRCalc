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