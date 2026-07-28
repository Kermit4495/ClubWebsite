# Hidden-Layer Neural Networks (MLP)

Notes based on `mlp_notes.pdf`, with a worked example and a guide to constructing
a model that predicts a continuous `y` value (see `lab11/regression_model.ipynb`
for the full implementation).

## 1. Problem setup

Data: `{(x_i, y_i)}` where `x_i ∈ R^p` and `y_i` is quantitative (regression) or
categorical (classification).

**Goal:** build a network that minimizes a loss function `L(y, ŷ)`.

For simplicity, consider a single hidden layer of dimension `d`:

```
x --W(1), b(1)--> (+) --φ--> z --W(2), b(2)--> (+) --φ--> ŷ
```

**Hyperparameters** (chosen before training):
- input / output dimensions
- number of hidden layers and their dimensions
- activation function `φ`
- learning rate `η`
- optimizer (GD, SGD, Adam, ...)

**Parameters** (learned during training): `W(1), b(1), W(2), b(2)`.

**Problem formulation:**

```
minimize_{W(1), b(1), W(2), b(2)}  L(y, ŷ)
```

## 2. Training algorithm

### Step 0 — Initialize
Initialize `W(1), b(1), W(2), b(2)` (e.g. random small values).

### Step 1 — Forward pass
```
z  = φ(W(1) x + b(1))
ŷ  = φ(W(2) z + b(2))
```

### Step 2 — Loss
- Regression → **MSE loss**: `L(y, ŷ) = (y - ŷ)²`
- Classification → **Cross-entropy loss**

### Step 3 — Backpropagation
Using the chain rule:

```
∂L/∂W(2) = ∂L/∂ŷ · z · φ'(W(2) z + b(2))
∂L/∂b(2) = ∂L/∂ŷ · φ'(W(2) z + b(2))

∂L/∂W(1) = ∂L/∂ŷ · W(2) φ'(W(2) z + b(2)) · x · φ'(W(1) x + b(1))
∂L/∂b(1) = ∂L/∂ŷ · W(2) φ'(W(2) z + b(2)) · φ'(W(1) x + b(1))
```

### Step 4 — Optimize (vanilla gradient descent)
```
W(1) ← W(1) - η ∂L/∂W(1)
b(1) ← b(1) - η ∂L/∂b(1)
W(2) ← W(2) - η ∂L/∂W(2)
b(2) ← b(2) - η ∂L/∂b(2)
```

Repeat steps 1–4 for each epoch until convergence.

## 3. Worked numeric example

Setup: `x = 5, y = 2`, init `W(1) = 1, b(1) = 0, W(2) = 1, b(2) = 0`,
activation = ReLU, `η = 0.01`, loss = MSE, optimizer = GD.

**Epoch 1**
- Forward: `z = φ(1·5+0) = 5`, `ŷ = φ(1·5+0) = 5`
- Loss: `L = (5-2)² = 9`
- Gradients: `∂L/∂ŷ = 2(ŷ-y) = 6`
  - `∂L/∂W(2) = 6 × 5 × 1 = 30`
  - `∂L/∂b(2) = 6 × 1 = 6`
  - `∂L/∂W(1) = 6 × (1×1) × (5×1) = 30 × 5 = 150`
  - `∂L/∂b(1) = 6 × 1 × 1 = 30`
- Update:
  - `W(1) = 1 - 0.01×150 = -0.5`
  - `b(1) = 0 - 0.01×30  = -0.3`
  - `W(2) = 1 - 0.01×30  =  0.7`
  - `b(2) = 0 - 0.01×6   = -0.06`

**Epoch 2**
- Forward: `W(1)x+b(1) = -0.5×5-0.3 = -2.8 → ReLU → z = 0`
- `W(2)z+b(2) = 0.7×0-0.06 = -0.06 → ReLU → ŷ = 0`
- Loss: `L = (0-2)² = 4` (down from 9 — the model improved after one GD step)

This confirms the mechanics: forward pass → loss → backprop → parameter update
reduces the loss over successive epochs.

## 4. From the toy example to a real model

The notes use `p = 1` hidden layer of dimension 1 for hand-derivable math. A
practical model generalizes this in a few ways, all still following the exact
same forward → loss → backprop → optimize loop (autograd just automates step 3):

| Notes (toy) | Practical model |
|---|---|
| 1 hidden layer, dim 1 | Multiple hidden layers, wider dims (e.g. 64 → 32 → 16) |
| Vanilla GD, full-batch | Adam optimizer, mini-batches |
| No regularization | Dropout, weight decay (L2) |
| Manual gradient derivation | Autograd (e.g. `loss.backward()` in PyTorch) |
| No validation | Train/validation split, early stopping, best-model checkpointing |

## 5. Constructing a model to predict `y`

Given a tabular regression dataset (`X` = features, `y` = continuous target),
build the model as follows (see `lab11/regression_model.ipynb` for the full
runnable version):

1. **Load & split data.** Read `X_train`, `y_train`, `X_test`, `y_test`.
   Carve out an internal validation split (e.g. 80/20) from training data for
   model selection, since test data can't be used for that.

2. **Define the architecture** — a stack of `Linear → activation` blocks,
   ending in a single linear output unit (no activation, since `y` is
   unconstrained real-valued):

   ```python
   import torch.nn as nn

   class RegressionNet(nn.Module):
       def __init__(self, in_features, hidden=(64, 32, 16), dropout=0.1):
           super().__init__()
           h1, h2, h3 = hidden
           self.net = nn.Sequential(
               nn.Linear(in_features, h1), nn.ReLU(), nn.Dropout(dropout),
               nn.Linear(h1, h2),          nn.ReLU(), nn.Dropout(dropout),
               nn.Linear(h2, h3),          nn.ReLU(),
               nn.Linear(h3, 1),
           )

       def forward(self, x):
           return self.net(x)
   ```

   This is the same `x → W(1)x+b(1) → φ → z → W(2)z+b(2) → φ → ŷ` diagram
   from the notes, chained across more layers.

3. **Choose loss & optimizer.**
   - Loss: `nn.MSELoss()` — matches "regression → MSE loss" from the notes.
   - Optimizer: `torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)`
     — a smarter, adaptive version of the vanilla GD update rule in step 4.

4. **Train the loop** (forward → loss → backward → step, per the notes'
   4-step algorithm), tracking validation loss each epoch:

   ```python
   for epoch in range(N_EPOCHS):
       model.train()
       for xb, yb in train_loader:
           optimizer.zero_grad()
           loss = criterion(model(xb), yb)   # step 1 + 2
           loss.backward()                   # step 3 (autograd)
           optimizer.step()                  # step 4

       model.eval()
       with torch.no_grad():
           val_loss = criterion(model(X_val), y_val).item()
       # track best val_loss, apply early stopping
   ```

5. **Model selection.** Save the parameters from the epoch with the lowest
   validation loss (early stopping with patience) rather than the final epoch,
   to avoid overfitting.

6. **Final evaluation.** Load the best checkpoint and compute MSE on the
   held-out test set — this is the reported generalization performance.

### Predicting `y` for new inputs

Once trained, prediction is just the **forward pass** (step 1) with the
learned parameters — no loss or backprop needed:

```python
model.eval()
with torch.no_grad():
    y_pred = model(x_new)
```
