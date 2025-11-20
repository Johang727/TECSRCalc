I initially tried this code block:

```python
# stole this from stack overflow

numeric_df = masterDF.select_dtypes(include=np.number)

outlier_mask = (np.abs(stats.zscore(numeric_df)) < 3).all(axis=1)

masterDF = masterDF[outlier_mask][masterDF["APM"] > 0]
```

but the issue was:
- it removed a lot of the high end plays and def not some of the 11k plays that could've been removed.


I did the IQR stuff, yet I feel like it still lacks and could be removing more from 11K.