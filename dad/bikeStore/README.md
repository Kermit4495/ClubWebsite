# Bike Store Sales in Europe

This folder contains the `bike-store-sales-in-europe.ipynb` notebook (originally a Kaggle notebook) and its dataset, `Sales.csv`, adapted to run locally.

## 1. Dataset

`Sales.csv` (113,036 rows, 18 columns) was downloaded from the Kaggle dataset
["Bike Sales in Europe"](https://www.kaggle.com/datasets/mrmorj/bike-sales-in-europe) and placed directly in this directory (`dad/bikeStore/Sales.csv`) so the notebook can load it without depending on Kaggle's runtime environment.

## 2. Notebook fixes

The notebook was written for Kaggle's hosted environment and failed to run locally. The following changes fix it:

### `read_csv` path (the key fix)

```diff
- Sales=pd.read_csv('/kaggle/input/bike-sales-in-europe/Sales.csv')
+ Sales=pd.read_csv('Sales.csv')
```

The original path (`/kaggle/input/bike-sales-in-europe/Sales.csv`) only exists inside Kaggle's hosted runtime and raised `FileNotFoundError` everywhere else. It's now a relative path, `'Sales.csv'`, pointing at the CSV that lives alongside the notebook in this same directory.

### Positional indexing inside `.apply()`

```diff
- x[0], x[1], x[2]
+ x.iloc[0], x.iloc[1], x.iloc[2]
```

In the `Calculated_Date` construction (`Sales[['Year','Month','Day']].apply(...)`), each `x` is a `Series` keyed by column name, not position. Plain `x[0]` relies on pandas' deprecated fallback to positional indexing and now raises a `FutureWarning`/error on modern pandas. Switched to explicit `.iloc[0]`/`.iloc[1]`/`.iloc[2]`.

### Undefined `wedges` in the pie chart legend

```diff
- Sales['Product_Category'].value_counts().plot(kind='pie', ...)
- ...
- plt.legend(wedges, Cat, ...)
+ ax = Sales['Product_Category'].value_counts().plot(kind='pie', ...)
+ ...
+ wedges = ax.patches
+ plt.legend(wedges, Cat, ...)
```

`wedges` was referenced in `plt.legend()` but never defined, causing a `NameError`. The plot's `Axes` is now captured (`ax = ...`) and `wedges = ax.patches` is derived from it before building the legend.

### `Sales.corr()` on non-numeric columns

```diff
- Corr=Sales.corr()
+ Corr=Sales.corr(numeric_only=True)
```

Newer pandas no longer silently drops non-numeric columns in `.corr()`; `numeric_only=True` restores the old behavior instead of erroring on the dataset's string columns.

### Removed a broken, unrelated Plotly cell

A trailing cell called `px.choropleth(df, locations="state", ...)` referenced a `df` and `state`/`value` columns that don't exist anywhere in this notebook (leftover from a different dataset), raising `NameError: name 'df' is not defined`. The cell was emptied out since it isn't part of this analysis.

### Environment/metadata noise

Re-running the notebook locally also updated execution timestamps, `execution_count` numbers, and the recorded Python version (`3.12.13` → `3.14.6`) in the cell metadata. These are incidental to re-execution and not functional changes.
