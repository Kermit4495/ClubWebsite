# How I Built the Model

## `numpy_mlp.ipynb` — MLP from scratch (NumPy only)

Data: `y = sin(x) + 0.1 * noise`, 200 points, `x` in `[-pi, pi]`.

1. **Linear regression baseline** — plain gradient descent on `y = wx + b`. Underfits the sine curve, as expected.
2. **Simplest MLP (1 hidden layer, `hidden_dim=1`)** — same shape as the lecture-note example: `W1, b1, W2, b2` (4 parameter tensors). Tried three activations:
   - ReLU
   - tanh
   - identity (linear) — shown to collapse back to exactly the linear regression solution, since stacking two linear maps is still linear.
3. **Deeper and wider MLP** — 2 hidden layers of width 50 (`W1,b1,W2,b2,W3,b3`, 6 parameter tensors), ReLU activations. Manual forward pass, manual backprop (chain rule coded by hand), manual GD parameter updates.
4. **Training loop** — fixed 5000 epochs, full-batch gradient descent, no train/val split, no early stopping. The notebook's closing discussion cell explicitly flags this as a limitation and asks how to prevent overfitting (train/val split, stopping condition) — that question hasn't been answered in code yet, i.e. this notebook currently just trains for a fixed epoch count and reports the final loss/fit plot.

## `regression_model.ipynb` — PyTorch feed-forward regression

Data: 700x10 tabular regression samples (standardized features), MSE loss target.

1. **Model**: `RegressionNet`, 4 `nn.Linear` layers (10→64→32→16→1) with ReLU + light Dropout(0.1) on the first two hidden layers — 8 parameter tensors total (4 weights + 4 biases). This is deeper than any network in `numpy_mlp.ipynb`.
2. **Split**: held-out test set provided separately; additionally carved an 80/20 train/val split out of the training data for model selection.
3. **Training**: Adam optimizer (lr=1e-3, weight_decay=1e-4), batch size 32, up to 500 epochs.
4. **Early stopping**: validation MSE tracked every epoch; training halts if it hasn't improved for 30 consecutive epochs (patience=30). Best-epoch weights are checkpointed (`best_model_state`) and reloaded for final test evaluation.
5. **Result**: best validation MSE ~0.123 (epoch 83), final test MSE ~0.052.

## Key difference between the two notebooks

`numpy_mlp.ipynb` trains on the full dataset for a fixed number of epochs with no validation signal, so it can't detect or stop overfitting — it only visualizes the effect via the loss curve. `regression_model.ipynb` adds the missing piece: a validation split plus patience-based early stopping, which is exactly the generalization safeguard the `numpy_mlp.ipynb` discussion section calls out as missing.

## Parameter count vs. the lecture-note (PDF) example

The PDF's toy MLP has 1 hidden layer — 2 weight matrices + 2 bias vectors (`W1, b1, W2, b2`) = 4 parameter tensors. Comparing every model built in this lab against that baseline:

| File | Layers (weight matrices) | Parameter tensors |
| --- | --- | --- |
| PDF example | 2 (input→hidden, hidden→output) | 4 |
| `numpy_mlp.ipynb` §2.1 (simplest MLP) | 2 (same shape as PDF) | 4 |
| `numpy_mlp.ipynb` §2.3 (deeper and wider) | 3 (input→h1, h1→h2, h2→output) | 6 |
| `regression_model.ipynb` (`RegressionNet`) | 4 (10→64, 64→32, 32→16, 16→1) | 8 |

`regression_model.ipynb` is the deepest model built in this lab (4 layers / 8 parameter tensors), sitting beyond `numpy_mlp.ipynb`'s deepest variant (3 layers / 6 parameter tensors), which in turn goes beyond the PDF's single-hidden-layer toy example (2 layers / 4 parameter tensors).
