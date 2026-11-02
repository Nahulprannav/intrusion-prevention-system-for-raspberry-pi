import os
import joblib
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
import lightgbm as lgb
import xgboost as xgb
import catboost as cb

# ================= PyTorch Deep Learning MLP Model =================
class TabularMLP(nn.Module):
    def __init__(self, input_dim: int, num_classes: int, hidden_dims=[256, 128, 64], dropout_rate: float = 0.25):
        super(TabularMLP, self).__init__()
        layers = []
        in_dim = input_dim
        for h_dim in hidden_dims:
            layers.append(nn.Linear(in_dim, h_dim))
            layers.append(nn.BatchNorm1d(h_dim))
            layers.append(nn.SiLU())
            layers.append(nn.Dropout(dropout_rate))
            in_dim = h_dim
        layers.append(nn.Linear(in_dim, num_classes))
        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x)

class PyTorchTabularClassifier:
    """
    Wrapper for PyTorch Tabular Neural Network with Scikit-Learn style fit/predict interface.
    """
    def __init__(self, input_dim: int, num_classes: int, epochs: int = 15, batch_size: int = 256, lr: float = 0.001):
        self.input_dim = input_dim
        self.num_classes = num_classes
        self.epochs = epochs
        self.batch_size = batch_size
        self.lr = lr
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = TabularMLP(input_dim, num_classes).to(self.device)

    def fit(self, X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray = None, y_val: np.ndarray = None):
        self.model.train()
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=self.lr, weight_decay=1e-4)
        
        train_dataset = TensorDataset(torch.tensor(X_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.long))
        train_loader = DataLoader(train_dataset, batch_size=self.batch_size, shuffle=True)
        
        print(f"\n[PyTorch MLP] Training for {self.epochs} epochs on {self.device}...")
        for epoch in range(1, self.epochs + 1):
            total_loss = 0.0
            correct = 0
            total = 0
            for X_batch, y_batch in train_loader:
                X_batch, y_batch = X_batch.to(self.device), y_batch.to(self.device)
                optimizer.zero_grad()
                outputs = self.model(X_batch)
                loss = criterion(outputs, y_batch)
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item() * len(y_batch)
                preds = outputs.argmax(dim=1)
                correct += (preds == y_batch).sum().item()
                total += len(y_batch)
                
            train_acc = correct / total
            avg_loss = total_loss / total
            if epoch % 5 == 0 or epoch == self.epochs:
                print(f"  Epoch [{epoch:02d}/{self.epochs:02d}] - Loss: {avg_loss:.4f} | Accuracy: {train_acc*100:.2f}%")
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        self.model.eval()
        with torch.no_grad():
            tensor_x = torch.tensor(X, dtype=torch.float32).to(self.device)
            logits = self.model(tensor_x)
            preds = logits.argmax(dim=1).cpu().numpy()
        return preds

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        self.model.eval()
        with torch.no_grad():
            tensor_x = torch.tensor(X, dtype=torch.float32).to(self.device)
            probs = torch.softmax(self.model(tensor_x), dim=1).cpu().numpy()
        return probs

# ================= Model Factory =================
def get_model(model_name: str, num_features: int, num_classes: int, random_state: int = 42):
    """
    Instantiates configured ML / DL classifiers with balanced presets.
    """
    model_name = model_name.upper()

    if model_name == "LIGHTGBM" or model_name == "GBM":
        return lgb.LGBMClassifier(
            n_estimators=150,
            learning_rate=0.08,
            num_leaves=63,
            max_depth=8,
            subsample=0.85,
            colsample_bytree=0.85,
            random_state=random_state,
            n_jobs=-1,
            verbosity=-1
        )
    elif model_name == "XGBOOST" or model_name == "XGB":
        return xgb.XGBClassifier(
            n_estimators=120,
            learning_rate=0.1,
            max_depth=6,
            subsample=0.85,
            colsample_bytree=0.85,
            random_state=random_state,
            n_jobs=-1,
            tree_method='hist',
            objective='binary:logistic' if num_classes == 2 else 'multi:softprob',
            eval_metric='logloss' if num_classes == 2 else 'mlogloss'
        )
    elif model_name == "CATBOOST" or model_name == "CAT":
        return cb.CatBoostClassifier(
            iterations=150,
            learning_rate=0.1,
            depth=6,
            random_seed=random_state,
            thread_count=-1,
            verbose=False
        )
    elif model_name == "RANDOM_FOREST" or model_name == "RF":
        return RandomForestClassifier(
            n_estimators=100,
            max_depth=16,
            min_samples_split=4,
            random_state=random_state,
            n_jobs=-1
        )
    elif model_name == "EXTRA_TREES" or model_name == "XT":
        return ExtraTreesClassifier(
            n_estimators=100,
            max_depth=16,
            min_samples_split=4,
            random_state=random_state,
            n_jobs=-1
        )
    elif model_name == "PYTORCH_MLP" or model_name == "FASTAI" or model_name == "NEURAL_NET":
        return PyTorchTabularClassifier(
            input_dim=num_features,
            num_classes=num_classes,
            epochs=15,
            batch_size=256,
            lr=0.002
        )
    else:
        raise ValueError(f"Unknown model name: {model_name}. Supported: LIGHTGBM, XGBOOST, CATBOOST, RANDOM_FOREST, EXTRA_TREES, PYTORCH_MLP")
