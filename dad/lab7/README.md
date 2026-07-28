# Lab 07 — Linear Regression and Mini Project 2

Source: [UC Davis COSMOS Cluster 11 — Lab07](https://ucd-cosmos-data.github.io/lab/lab7/)
(`lab_description.txt` is the saved raw HTML of this page.)

## Mini Project 2: K-Means Clustering of California Housing

### Goal

Divide California into a small number of **real-estate market regions** —
areas that are geographically contiguous and similar in price — using
**K-means clustering** on the California Housing dataset, restricted to
three features: **longitude**, **latitude**, and **median house value**.

The deliverable is a **written report** (no presentation), emphasizing a
clear explanation of why K-means is an appropriate method for this goal.

### Data

```python
import pandas as pd
from sklearn.datasets import fetch_california_housing

data = fetch_california_housing(as_frame=True)
df = data.frame
```

Dataset description:

```python
print(data.DESCR)
```

### Report Requirements

1. **Methodology explanation (K-means)**
   - State the purpose of the method.
   - Describe the data structure it operates on.
   - Formulate the minimization problem.
   - Describe the algorithm used to solve it.
   - Identify the hyperparameters and how they're chosen.
   - Explain why feature scaling is required.
   - You may use Codex to help, but do not copy/paste directly — review it,
     understand it, and write it in your own words.

2. **Results (figure) and interpretation**
   - Produce a final scatter plot: longitude (x-axis), latitude (y-axis),
     points colored by cluster.
   - Report each region's mean price.
   - Interpret the resulting regions.

3. **Code**
   - Include full, runnable code in an appendix.
   - No code chunks in the main body of the report.

4. **(Optional)** Try other clustering methods and compare results.
