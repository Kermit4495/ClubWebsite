# scikit-learn01.ipynb

An introductory notebook on `scikit-learn`, focused on the data preprocessing stage of a machine learning workflow.

## Contents

**Overview**
- Core `scikit-learn` capabilities: preprocessing, supervised/unsupervised learning, model evaluation, and model selection.
- The `BaseEstimator` object hierarchy (`TransformerMixin`, `ClassifierMixin`, `RegressorMixin`, `ClusterMixin`, etc.).

**I. Data Preprocessing**
1. **Data Split** — using `train_test_split` from `sklearn.model_selection` to create train/test sets (`test_size`, `random_state`), for both supervised and unsupervised settings.
2. **Transformation** — the `fit` / `transform` / `fit_transform` pattern for `TransformerMixin` objects, and why transformers must be fit only on training data.
   - a) Missing value imputation with `SimpleImputer`
   - b) Feature scaling with `StandardScaler` / `MinMaxScaler`, and which model types require scaling
   - c) Dimensionality reduction with `PCA` and `Isomap`
   - d) Categorical encoding with `OneHotEncoder` / `OrdinalEncoder`
3. **Save** — persisting processed data (`X_train_processed`, `X_test_processed`, `y_train`, `y_test`) with `to_csv()` and fitted transformers with `pickle`, organized by model when preprocessing differs across models.

## Requirements

- Python 3
- `scikit-learn`
- `pandas`

## Usage

Open the notebook with Jupyter:

```bash
jupyter notebook scikit-learn01.ipynb
```

## Related files

- `scikit-learn01.pdf` — PDF export of this notebook.
- `data-split.pdf` — supplementary reference on data splitting.
