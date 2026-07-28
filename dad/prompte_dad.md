## 1. Situation

We are given a tabular regression dataset with 10 float-valued input features per sample and a single continuous float target. The goal is to train a feed-forward neural network in PyTorch that predicts the target value from the 10 features. Model quality is evaluated using Mean Squared Error (`torch.nn.MSELoss()`) between predictions and true targets on held-out data. We select the best model based on validation MSE observed during training and report its performance on the test set.

## 2. Data description

* `X_train.csv` / `X_test.csv`: 700 samples x 10 features, no header row, no missing values.
* `y_train.csv` / `Y_test.csv`: 700 samples x 1 target value, no header row, no missing values.
* All 10 input features are already standardized (mean approx 0, std approx 1), roughly in the range [-4, 4].
* The target is also on a standardized-looking scale (mean approx 0, std approx 1), range approx [-3, 5.7].
* Because no further scaling is required, features are fed directly into the network. An internal 80/20 train/validation split is carved out of the training data to monitor generalization and perform model selection / early stopping.

## 3. Constraints (Do Not Change)

* Performance on the test data will be evaluated with torch.nn.MSELoss().
* Deliver the code as a Jupyter notebook (.ipynb).
* Implement the model in PyTorch.
* The network must have AT MOST 20 layers in total.
* Store the parameters of your best model in a variable named `best_model_state`.

## 4. Model specification

A small fully-connected feed-forward network:

* Input layer: 10 features
* Hidden layer 1: Linear(10 -> 64) + ReLU + Dropout(0.1)
* Hidden layer 2: Linear(64 -> 32) + ReLU + Dropout(0.1)
* Hidden layer 3: Linear(32 -> 16) + ReLU
* Output layer: Linear(16 -> 1)

This is 4 `Linear` layers total (well under the 20-layer limit), which is enough capacity for a 10-feature tabular regression problem without overfitting a 700-row dataset. ReLU activations are used throughout the hidden layers, with light dropout (0.1) after the first two hidden layers for regularization; the output layer is linear (no activation) since this is unconstrained real-valued regression.

## 5. Training specification

The model is trained with Adam and mild weight decay for regularization, using the required `torch.nn.MSELoss()` as the objective. Rather than fixing the number of epochs up front, training runs for up to 500 epochs but stops early once validation MSE stalls, which avoids overfitting the relatively small 700-row training set. Model selection is done by tracking validation MSE after every epoch and keeping a snapshot of the weights from the best-performing epoch, rather than simply using whatever the final epoch produces.

* Loss function: `torch.nn.MSELoss()` (as required by the evaluation constraint).
* Optimizer: Adam, learning rate 1e-3, weight decay 1e-4 (mild L2 regularization).
* Batch size: 32.
* Number of epochs: up to 500, with early stopping.
* Validation strategy: a random 80/20 hold-out split of the training data (560 train / 140 validation, fixed seed), separate from the true test set. The split is made once before training starts; validation MSE is computed on this fixed 140-row set once per epoch to track generalization.
* Early stopping: training stops if validation MSE does not improve for 30 consecutive epochs (patience=30), signaling the model has stopped generalizing better and further training would just overfit the training split.
* Best model: defined as the epoch with the lowest validation MSE seen so far, not the final epoch reached. Its weights are snapshotted at that epoch and stored in `best_model_state`, then reloaded for final evaluation on the test set.

## 6. Training curve

Record train/validation MSE per epoch and plot both as a line graph.
