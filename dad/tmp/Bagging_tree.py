#!/usr/bin/env python
# coding: utf-8

# 
# # Bagging 
# 

# ### What Is Bagging?
# 
# Bagging—short for <span style="color:#1f77b4">**bootstrap aggregating**</span>—is an <span style="color:#1f77b4">**ensemble**</span> method that trains many independent copies of the same base learner on different bootstrap samples (random samples *with* replacement) and then averages their predictions.
# 
# The idea: <span style="color:#2ca02c">**reduce variance**</span> without increasing bias by “voting” across diverse models that each see slightly different data.
# 
# ---
# 
# ### How It Works
# 
# Conceptual algorithm: 
# 1. **Bootstrap** the training set $B$ times → $B$ equally-sized samples <span style="color:#ff7f0e">**with replacement**</span>.
# 2. Train an **independent** (usually deep) tree on each sample.
# 3. **Aggregate** using majority vote for classification and mean/median for regression.
# 4. **Model selection** (or parameter tuning) using <span style="color:#ff7f0e">**out-of-bag**</span> (OOB) errors.
# 
# ---
# 
# ### Why It Works
# 
# * Each tree “sees” a *different* slice of data → their errors are less correlated.
# * Averaging cancels out noise ⇒ **lower variance** and better generalization.
# 
# ---
# 
# ### Popular Methods
# 
# | Ensemble                                     | Extra Twist                                                                                 |
# | -------------------------------------------- | ------------------------------------------------------------------------------------------- |
# | **Plain BaggingClassifier / Regressor**      | Same features for every tree; randomness only from bootstrapped rows.                       |
# | **Random Forest**                            | Adds column-sampling at every *split* to further de-correlate trees.                        |
# | **Extra Trees (Extremely Randomized Trees)** | Uses the whole dataset but selects split thresholds at random—high bias, very low variance. |
# 
# ---
# 
# ### Pros and Cons
# 
# ✅ **Parallel-friendly**: each model trains independently—easy to distribute.  
# ✅ Dramatically **reduces variance** of high-variance learners (e.g.\ full-depth trees).  
# ✅ Mitigates overfitting without heavy hyper-parameter tuning.  
# ✅ Naturally provides <span style="color:#ff7f0e">**out-of-bag**</span> error estimates—no extra validation set needed.  
# 
# ❌ Yields **large, memory-hungry** ensembles (hundreds of trees).  
# ❌ Adds little benefit if the base learner is already low-variance (e.g.\ regularized linear models).  
# ❌ Final model loses interpretability of a single tree; feature importance is more diffuse.  
# 
# ---
# 
# Key Hyper-parametersa
# 
# | Symbol in `sklearn` | Meaning                          | Typical starter value |
# | ------------------- | -------------------------------- | --------------------- |
# | `n_estimators`      | number of bootstrapped trees $B$ | 100                   |
# | `max_samples`       | rows per bootstrap sample        | 0.6 – 1.0             |
# | `max_features`      | columns sent to each tree        | 1.0 (all)             |
# 
# ---

# > *Think of Bagging as crowd-sourcing your model: each member is noisy, but their average is calm and reliable.* --- Words of wisdom by ChatGPT 3o (2025)
# 
# > *Bagging finds stability in disagreement: let many models see slightly different worlds, then trust the pattern that survives their noise.* --— Words of wisdom by GPT-5.6 Pro (2026)
# 
# > *A bagged forest is a panel of honest second opinions: each tree is jumpy, but the vote is steady --- as long as every tree gets its own bootstrap of the evidence.* --- Words of wisdom by Claude Fable 5 (2026)
# 

# 
# #### 3.3  Bagging (Bootstrap Aggregation)
# 
# Why it works: 
# 

# In[1]:


# --- Synthetic data
import numpy as np

rng = np.random.default_rng(0)   # fixed seed: everyone gets the same data
sample_size = 200
X = rng.uniform(0.1, 0.9, size=(sample_size, 2))   # 200 points, 2 features

# Assign labels by region (no noise -- the boundaries ARE the truth):
y = np.zeros(sample_size, dtype=int)
mask1 = X[:, 0] + X[:, 1] > 1.1            # above the line x1 + x2 = 1.1  -> class 1
mask2 = (~mask1) & (X[:, 0] - X[:, 1] > 0.3)  # below it but right of x1 - x2 = 0.3 -> class 0
y[mask1] = 1
y[mask2] = 0
y[~(mask1 | mask2)] = 2                    # everything else -> class 2


# In[2]:


# ----- imports -------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import sklearn                                   # version check
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

import ipywidgets as widgets
from IPython.display import display

label_cmap = ListedColormap(["#1f77b4", "#ff7f0e", "#2ca02c"])

# ----- helper: fit & plot a bagging ensemble --------------------------------
# The three algorithm steps from "How It Works" all happen inside
# BaggingClassifier:
#   Step 1 (bootstrap):   bootstrap=True draws n_estimators samples,
#                         each WITH replacement, same size as the data.
#   Step 2 (independent): one DecisionTreeClassifier is fit per sample;
#                         max_depth controls how unstable each tree is.
#   Step 3 (aggregate):   .predict() returns the majority vote of all trees.
def plot_bagging(max_features=1.0, n_estimators=100, max_depth=3):
    depth = None if max_depth == 0 else int(max_depth)   # 0 on the slider = unlimited depth

    # build BaggingClassifier with proper keyword for your scikit-learn version
    bag_kwargs = dict(
        n_estimators=int(n_estimators),   # B: how many trees (Step 1)
        max_features=max_features,        # fraction of features each tree sees
                                          #   (<1.0 previews the random-forest idea)
        bootstrap=True,                   # Step 1: resample WITH replacement
        oob_score=True,                   # free validation from left-out points
                                          #   (~37% per tree; see OOB, model validation)
        random_state=42,
    )
    tree = DecisionTreeClassifier(max_depth=depth, random_state=42)   # Step 2: the base learner
    if sklearn.__version__ >= "1.4":
        bag_kwargs["estimator"] = tree
    else:                                      # pre-1.4 API
        bag_kwargs["base_estimator"] = tree

    bag = BaggingClassifier(**bag_kwargs).fit(X, y)   # Steps 1-3 run here

    # Visualization: ask the fitted ensemble to classify every point on a fine
    # grid, so the colored regions show the ensemble's decision rule (Step 3's
    # majority vote, evaluated everywhere).
    x_min, x_max = X[:, 0].min() - 0.05, X[:, 0].max() + 0.05
    y_min, y_max = X[:, 1].min() - 0.05, X[:, 1].max() + 0.05
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, 400),
        np.linspace(y_min, y_max, 400),
    )
    Z = bag.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

    # plot decision regions + data
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.contourf(xx, yy, Z, alpha=0.25, cmap=label_cmap)
    ax.scatter(X[:, 0], X[:, 1],
               c=y, cmap=label_cmap,
               edgecolors="k", s=80)

    depth_label = "None" if depth is None else depth
    ax.set_title(f"Bagging (Decision Trees): max_features={max_features:.2f}, "
                 f"n_estimators={n_estimators}, max_depth={depth_label}\n"
                 f"OOB accuracy ≈ {bag.oob_score_:.3f}")
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    fig.tight_layout()
    plt.show()
    plt.close(fig)

# ----- interactive widgets --------------------------------------------------
# What each slider teaches:
#   n_estimators: more trees -> steadier vote (watch the boundary smooth out;
#                 it should NOT overfit as B grows)
#   max_depth:    deeper base trees = more variance for bagging to remove
#                 (try depth 0 = unlimited vs depth 1 stumps)
#   max_features: < 1.0 decorrelates the trees -- the bridge to random forests
max_features_slider = widgets.FloatSlider(
    value=1.0, min=0.2, max=1.0, step=0.1,
    description="max_features (≤1.0)",
    continuous_update=False,
)
n_estimators_slider = widgets.IntSlider(
    value=100, min=10, max=300, step=10,
    description="n_estimators",
    continuous_update=False,
)
max_depth_slider = widgets.IntSlider(
    value=3, min=0, max=6, step=1,
    description="max_depth (0=unlimited)",
    continuous_update=False,
)

controls = widgets.VBox([max_features_slider, n_estimators_slider, max_depth_slider])
plot_output = widgets.interactive_output(
    plot_bagging,
    {
        "max_features": max_features_slider,
        "n_estimators": n_estimators_slider,
        "max_depth": max_depth_slider,
    },
)

display(widgets.HBox([controls, plot_output]))


# In[ ]:




