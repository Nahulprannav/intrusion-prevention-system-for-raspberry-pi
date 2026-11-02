import os
import time
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from src.config import (
    SAVED_MODELS_DIR, FEATURE_COLUMNS, LABEL_COLUMN,
    METRICS_DIR, FIGURES_DIR
)
from src.data_loader import prepare_or_load_data, transform_targets
from src.models import get_model
from src.evaluate import evaluate_model, plot_model_comparison
from src.reporting import generate_evaluation_report

def train_pipeline(
    task: str = "category",
    selected_models: list = ["LIGHTGBM", "XGBOOST", "CATBOOST", "RANDOM_FOREST", "EXTRA_TREES", "PYTORCH_MLP"],
    force_resample: bool = False
):
    """
    End-to-End Training and Evaluation Pipeline.
    task: 'category' (8 classes), 'multiclass' (34 classes), or 'binary' (2 classes)
    """
    print("\n" + "="*70)
    print(f"      STARTING TRAINING PIPELINE: TASK = {task.upper()}")
    print("="*70)

    # 1. Load Data
    train_df, val_df, test_df = prepare_or_load_data(force_recompute=force_resample)
    
    # 2. Extract Features
    feature_cols = [c for c in FEATURE_COLUMNS if c in train_df.columns]
    X_train_raw = train_df[feature_cols].values
    X_val_raw = val_df[feature_cols].values
    X_test_raw = test_df[feature_cols].values

    # 3. Transform Labels
    y_train_raw = transform_targets(train_df[LABEL_COLUMN], classification_type=task)
    y_val_raw = transform_targets(val_df[LABEL_COLUMN], classification_type=task)
    y_test_raw = transform_targets(test_df[LABEL_COLUMN], classification_type=task)

    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(y_train_raw)
    y_val = label_encoder.transform(y_val_raw)
    y_test = label_encoder.transform(y_test_raw)
    class_names = list(label_encoder.classes_)

    num_classes = len(class_names)
    num_features = len(feature_cols)
    print(f"\n[Setup] Features: {num_features} | Target Classes: {num_classes} -> {class_names}")
    print(f"[Setup] Train records: {len(X_train_raw):,} | Val: {len(X_val_raw):,} | Test: {len(X_test_raw):,}")

    # 4. Feature Normalization
    print("\n[Preprocessing] Fitting StandardScaler on training set...")
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train_raw)
    X_val = scaler.transform(X_val_raw)
    X_test = scaler.transform(X_test_raw)

    # 5. Train Models Tournament
    os.makedirs(SAVED_MODELS_DIR, exist_ok=True)
    tournament_results = []
    trained_models = {}

    for model_name in selected_models:
        print(f"\n>>> Training Model: {model_name} ...")
        t_start = time.time()
        
        try:
            model = get_model(model_name, num_features=num_features, num_classes=num_classes)
            
            # Model-specific fitting
            if model_name.upper() in ["LIGHTGBM", "GBM"]:
                model.fit(
                    X_train, y_train,
                    eval_set=[(X_val, y_val)],
                    callbacks=[]
                )
            elif model_name.upper() in ["XGBOOST", "XGB"]:
                model.fit(
                    X_train, y_train,
                    eval_set=[(X_val, y_val)],
                    verbose=False
                )
            elif model_name.upper() in ["CATBOOST", "CAT"]:
                model.fit(
                    X_train, y_train,
                    eval_set=(X_val, y_val),
                    verbose=False
                )
            elif model_name.upper() in ["PYTORCH_MLP", "FASTAI", "NEURAL_NET"]:
                model.fit(X_train, y_train, X_val, y_val)
            else:
                model.fit(X_train, y_train)

            train_time = round(time.time() - t_start, 2)
            print(f"  Completed training {model_name} in {train_time} seconds.")

            # Evaluate on Test Set
            eval_metrics = evaluate_model(
                model=model,
                X_test=X_test,
                y_test=y_test,
                class_names=class_names,
                model_name=model_name,
                task_name=task,
                feature_names=feature_cols
            )
            eval_metrics['train_time_sec'] = train_time
            tournament_results.append(eval_metrics)
            trained_models[model_name] = model

        except Exception as e:
            print(f"[ERROR] Failed to train {model_name}: {str(e)}")

    # 6. Generate Comparative Leaderboard Chart
    leaderboard_chart = plot_model_comparison(tournament_results, task_name=task)

    # 7. Identify Champion Model & Save Artifacts
    if tournament_results:
        best_entry = max(tournament_results, key=lambda x: x['weighted_f1'])
        best_model_name = best_entry['model_name']
        champion_model = trained_models[best_model_name]

        print("\n" + "="*70)
        print(f"   TOURNAMENT CHAMPION: {best_model_name}")
        print(f"   Accuracy: {best_entry['accuracy']*100:.2f}% | Weighted F1: {best_entry['weighted_f1']*100:.2f}% | Macro F1: {best_entry['macro_f1']*100:.2f}%")
        print("="*70)

        # Save Artifacts
        artifacts = {
            'model': champion_model,
            'scaler': scaler,
            'label_encoder': label_encoder,
            'feature_cols': feature_cols,
            'class_names': class_names,
            'task': task,
            'best_model_name': best_model_name,
            'metrics': best_entry
        }
        artifact_path = os.path.join(SAVED_MODELS_DIR, f"champion_{task}_pipeline.joblib")
        joblib.dump(artifacts, artifact_path)
        print(f"[Artifact Saved] Champion model pipeline -> {artifact_path}")

        # Also save tournament summary table
        leaderboard_df = pd.DataFrame(tournament_results)[[
            'model_name', 'accuracy', 'weighted_precision', 'weighted_recall',
            'weighted_f1', 'macro_precision', 'macro_recall', 'macro_f1',
            'train_time_sec'
        ]]
        leaderboard_df.columns = [
            'Model', 'Accuracy', 'Weighted_Precision', 'Weighted_Recall',
            'Weighted_F1', 'Macro_Precision', 'Macro_Recall', 'Macro_F1',
            'Training_Time_s'
        ]
        leaderboard_csv = os.path.join(METRICS_DIR, f"leaderboard_{task}.csv")
        leaderboard_df.to_csv(leaderboard_csv, index=False)
        print(f"[Leaderboard Saved] -> {leaderboard_csv}")
        print("\nLeaderboard Table:")
        print(leaderboard_df.to_string(index=False))

    generate_evaluation_report()
    return tournament_results
