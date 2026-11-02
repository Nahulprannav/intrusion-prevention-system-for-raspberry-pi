import os
import time
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import StackingClassifier, VotingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
import lightgbm as lgb

# =====================================================================
# 1. TABULAR FOUNDATION ARCHITECTURE: FT-TRANSFORMER (PyTorch)
# Feature Tokenizer + Multi-Head Self-Attention for Tabular Data
# =====================================================================
class NumericalFeatureTokenizer(nn.Module):
    """
    Transforms numerical features into embedding vectors using linear embeddings + bias.
    """
    def __init__(self, n_features: int, d_token: int):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(n_features, d_token))
        self.bias = nn.Parameter(torch.randn(n_features, d_token))
        nn.init.kaiming_uniform_(self.weight, a=np.sqrt(5))
        nn.init.zeros_(self.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (batch_size, n_features) -> returns (batch_size, n_features, d_token)
        return x.unsqueeze(-1) * self.weight.unsqueeze(0) + self.bias.unsqueeze(0)

class TabularTransformer(nn.Module):
    """
    Tabular Foundation Transformer Model (FT-Transformer style).
    Applies Multi-Head Attention across tabular features.
    """
    def __init__(self, n_features: int, num_classes: int, d_token: int = 32, n_heads: int = 4, n_blocks: int = 2, dropout: float = 0.15):
        super().__init__()
        self.tokenizer = NumericalFeatureTokenizer(n_features, d_token)
        self.cls_token = nn.Parameter(torch.zeros(1, 1, d_token))
        nn.init.normal_(self.cls_token, std=0.02)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_token,
            nhead=n_heads,
            dim_feedforward=d_token * 2,
            dropout=dropout,
            activation='gelu',
            batch_first=True,
            norm_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_blocks)
        self.norm = nn.LayerNorm(d_token)
        self.head = nn.Sequential(
            nn.Linear(d_token, d_token // 2),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_token // 2, num_classes)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size = x.size(0)
        tokens = self.tokenizer(x)  # (batch_size, n_features, d_token)
        cls_tokens = self.cls_token.expand(batch_size, -1, -1)
        tokens = torch.cat([cls_tokens, tokens], dim=1)  # (batch_size, n_features + 1, d_token)
        
        encoded = self.transformer(tokens)
        cls_output = self.norm(encoded[:, 0])  # Take representation of [CLS] token
        logits = self.head(cls_output)
        return logits

class TabularFoundationClassifier(BaseEstimator, ClassifierMixin):
    """
    Scikit-Learn compliant Tabular Foundation Transformer Classifier.
    """
    def __init__(self, n_features: int = 46, num_classes: int = 8, d_token: int = 32, n_heads: int = 4, n_blocks: int = 2, epochs: int = 5, batch_size: int = 256, lr: float = 0.001):
        self.n_features = n_features
        self.num_classes = num_classes
        self.d_token = d_token
        self.n_heads = n_heads
        self.n_blocks = n_blocks
        self.epochs = epochs
        self.batch_size = batch_size
        self.lr = lr
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = TabularTransformer(n_features, num_classes, d_token, n_heads, n_blocks).to(self.device)

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.model.train()
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=self.lr, weight_decay=1e-4)

        dataset = TensorDataset(torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.long))
        loader = DataLoader(dataset, batch_size=self.batch_size, shuffle=True)

        print(f"\n[Tabular Foundation Transformer] Training on {self.device} for {self.epochs} epochs...", flush=True)
        for epoch in range(1, self.epochs + 1):
            total_loss = 0.0
            correct = 0
            total = 0
            for X_b, y_b in loader:
                X_b, y_b = X_b.to(self.device), y_b.to(self.device)
                optimizer.zero_grad()
                out = self.model(X_b)
                loss = criterion(out, y_b)
                loss.backward()
                optimizer.step()

                total_loss += loss.item() * len(y_b)
                correct += (out.argmax(dim=1) == y_b).sum().item()
                total += len(y_b)

            acc = correct / total
            print(f"  Epoch [{epoch:02d}/{self.epochs:02d}] Loss: {total_loss/total:.4f} | Train Acc: {acc*100:.2f}%", flush=True)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        self.model.eval()
        with torch.no_grad():
            t_x = torch.tensor(X, dtype=torch.float32).to(self.device)
            out = self.model(t_x)
            preds = out.argmax(dim=1).cpu().numpy()
        return preds

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        self.model.eval()
        with torch.no_grad():
            t_x = torch.tensor(X, dtype=torch.float32).to(self.device)
            probs = torch.softmax(self.model(t_x), dim=1).cpu().numpy()
        return probs

# =====================================================================
# 2. ENSEMBLES FROM THE IEEE PAPER
# Stacking Ensemble & Voting Ensemble
# =====================================================================
def create_stacking_ensemble(random_state: int = 42) -> StackingClassifier:
    """
    Creates the Stacking Ensemble documented in the paper (Table I: 96.72% accuracy).
    Combines Random Forest, LightGBM, and Decision Tree with a Logistic Regression Meta-Learner.
    Uses n_jobs=1 to guarantee zero multiprocessing deadlocks on Windows sandbox.
    """
    base_estimators = [
        ('rf', RandomForestClassifier(n_estimators=40, max_depth=10, random_state=random_state, n_jobs=1)),
        ('lgb', lgb.LGBMClassifier(n_estimators=40, learning_rate=0.1, max_depth=6, random_state=random_state, verbosity=-1, n_jobs=1)),
        ('dt', DecisionTreeClassifier(max_depth=10, min_samples_split=5, random_state=random_state))
    ]
    meta_learner = LogisticRegression(max_iter=200, random_state=random_state)
    return StackingClassifier(estimators=base_estimators, final_estimator=meta_learner, cv=2, n_jobs=1)

def create_voting_ensemble(random_state: int = 42) -> VotingClassifier:
    """
    Creates the Voting Ensemble documented in the paper (Table I: 95.98% accuracy).
    Combines Random Forest, XGBoost, and LightGBM with soft probability voting.
    """
    estimators = [
        ('rf', RandomForestClassifier(n_estimators=40, max_depth=10, random_state=random_state, n_jobs=1)),
        ('xgb', xgb.XGBClassifier(n_estimators=40, learning_rate=0.1, max_depth=6, random_state=random_state, eval_metric='mlogloss', n_jobs=1)),
        ('lgb', lgb.LGBMClassifier(n_estimators=40, learning_rate=0.1, max_depth=6, random_state=random_state, verbosity=-1, n_jobs=1))
    ]
    return VotingClassifier(estimators=estimators, voting='soft', n_jobs=1)

# =====================================================================
# 3. EDGE-OPTIMIZED DECISION TREE FOR RASPBERRY PI
# Section IV-E & Table II: 0.8ms inference, 2.3MB model size, 45MB RAM
# =====================================================================
def create_raspberry_pi_edge_dt(random_state: int = 42) -> DecisionTreeClassifier:
    """
    Creates the ultra-lightweight Decision Tree optimized for Raspberry Pi deployment.
    """
    return DecisionTreeClassifier(
        criterion='gini',
        max_depth=14,
        min_samples_split=10,
        min_samples_leaf=4,
        random_state=random_state
    )
