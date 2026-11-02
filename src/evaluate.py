import os
import json
from typing import Optional
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)
from src.config import FIGURES_DIR, METRICS_DIR

def evaluate_model(
    model,
    X_test: np.ndarray,
    y_test: np.ndarray,
    class_names: list,
    model_name: str = "Model",
    task_name: str = "8_categories",
    feature_names: Optional[list] = None,
    validation_metrics: Optional[dict] = None
) -> dict:
    """
    Computes comprehensive evaluation metrics and generates high-resolution figures.
    """
    print(f"\n{'='*70}")
    print(f"      EVALUATING: {model_name} (Task: {task_name})")
    print(f"{'='*70}")

    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(METRICS_DIR, exist_ok=True)

    # 1. Predictions
    y_pred = model.predict(X_test)
    
    # In case predictions are one-hot or float probabilities
    if len(y_pred.shape) > 1 and y_pred.shape[1] > 1:
        y_pred = np.argmax(y_pred, axis=1)

    # 2. Key Metrics
    acc = accuracy_score(y_test, y_pred)
    prec_w = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec_w = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1_w = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    prec_m = precision_score(y_test, y_pred, average='macro', zero_division=0)
    rec_m = recall_score(y_test, y_pred, average='macro', zero_division=0)
    f1_m = f1_score(y_test, y_pred, average='macro', zero_division=0)

    print(f"  Accuracy:         {acc*100:.2f}%")
    print(f"  Weighted F1:      {f1_w*100:.2f}% (Precision: {prec_w*100:.2f}%, Recall: {rec_w*100:.2f}%)")
    print(f"  Macro F1:         {f1_m*100:.2f}% (Precision: {prec_m*100:.2f}%, Recall: {rec_m*100:.2f}%)")

    # 3. Classification Report
    target_labels = list(range(len(class_names)))
    clf_report = classification_report(
        y_test, y_pred,
        labels=target_labels,
        target_names=class_names,
        zero_division=0,
        output_dict=True
    )
    class_metrics = pd.DataFrame([
        {
            "class": cls,
            "precision": clf_report[cls]["precision"],
            "recall": clf_report[cls]["recall"],
            "f1_score": clf_report[cls]["f1-score"],
            "support": int(clf_report[cls]["support"])
        }
        for cls in class_names
    ])
    print("\n  Classification Summary by Class:")
    for cls in class_names:
        if cls in clf_report:
            row = clf_report[cls]
            print(f"    - {cls:20s}: Precision={row['precision']:.3f}, Recall={row['recall']:.3f}, F1={row['f1-score']:.3f} (support={row['support']})")

    # ================= PLOT 1: Confusion Matrix =================
    cm = confusion_matrix(y_test, y_pred, labels=target_labels)
    cm_norm = cm.astype('float') / (cm.sum(axis=1)[:, np.newaxis] + 1e-9)

    cm_df = pd.DataFrame(cm, index=class_names, columns=class_names)
    cm_df.index.name = "Actual"
    cm_df.columns.name = "Predicted"
    cm_path = os.path.join(METRICS_DIR, f"confusion_matrix_{model_name}_{task_name}.csv")
    cm_df.to_csv(cm_path)

    cm_norm_df = pd.DataFrame(cm_norm, index=class_names, columns=class_names)
    cm_norm_df.index.name = "Actual"
    cm_norm_df.columns.name = "Predicted"
    cm_norm_path = os.path.join(METRICS_DIR, f"confusion_matrix_normalized_{model_name}_{task_name}.csv")
    cm_norm_df.to_csv(cm_norm_path)

    class_metrics_path = os.path.join(METRICS_DIR, f"class_metrics_{model_name}_{task_name}.csv")
    class_metrics.to_csv(class_metrics_path, index=False)

    fig, ax = plt.subplots(figsize=(11, 9))
    cax = ax.imshow(cm_norm, cmap='Blues', vmin=0, vmax=1)
    fig.colorbar(cax, ax=ax, shrink=0.8, label="Normalized Accuracy Rate")

    ax.set_xticks(np.arange(len(class_names)))
    ax.set_yticks(np.arange(len(class_names)))
    ax.set_xticklabels(class_names, rotation=45, ha='right', fontsize=9)
    ax.set_yticklabels(class_names, fontsize=9)
    ax.set_ylabel('Ground Truth Label', fontsize=11, weight='bold')
    ax.set_xlabel('Predicted Label', fontsize=11, weight='bold')
    ax.set_title(f"Normalized Confusion Matrix - {model_name} ({task_name})\nAccuracy: {acc*100:.2f}% | Weighted F1: {f1_w*100:.2f}%", fontsize=12, weight='bold')

    # Annotate cells
    for i in range(len(class_names)):
        for j in range(len(class_names)):
            val = cm_norm[i, j]
            raw_cnt = cm[i, j]
            color = "white" if val > 0.5 else "black"
            ax.text(j, i, f"{val:.2f}\n({raw_cnt})", ha="center", va="center", color=color, fontsize=7)

    plt.tight_layout()
    cm_figure_path = os.path.join(FIGURES_DIR, f"eval_cm_{model_name}_{task_name}.png")
    plt.savefig(cm_figure_path, dpi=300)
    plt.close()
    print(f"\n[Saved Plot] Confusion Matrix -> {cm_figure_path}")
    print(f"[Saved Data] Confusion matrix CSVs -> {cm_path}, {cm_norm_path}")

    # ================= PLOT 2: Per-Class Precision, Recall & F1 =================
    class_f1s = [clf_report[cls]['f1-score'] for cls in class_names if cls in clf_report]
    valid_classes = [cls for cls in class_names if cls in clf_report]
    class_precisions = [clf_report[cls]['precision'] for cls in valid_classes]
    class_recalls = [clf_report[cls]['recall'] for cls in valid_classes]

    fig, ax = plt.subplots(figsize=(12, max(6, len(valid_classes) * 0.32)))
    y_pos = np.arange(len(valid_classes))
    bar_height = 0.24
    ax.barh(y_pos - bar_height, class_precisions, height=bar_height, label="Precision", color="#1f77b4")
    ax.barh(y_pos, class_recalls, height=bar_height, label="Recall", color="#ff7f0e")
    ax.barh(y_pos + bar_height, class_f1s, height=bar_height, label="F1 score", color="#2ca02c")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(valid_classes, fontsize=9, weight='semibold')
    ax.invert_yaxis()
    ax.set_xlim(0, 1.05)
    ax.set_title(f"Per-Class Precision, Recall & F1 - {model_name} ({task_name})", fontsize=13, weight='bold')
    ax.set_xlabel("Score (0.0 to 1.0)", fontsize=11, weight='bold')
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    ax.legend(loc="lower right")

    plt.tight_layout()
    f1_path = os.path.join(FIGURES_DIR, f"eval_f1_per_class_{model_name}_{task_name}.png")
    plt.savefig(f1_path, dpi=300)
    plt.close()
    print(f"[Saved Plot] Per-Class F1 Score -> {f1_path}")

    # ================= PLOT 3: Feature Importances (Tree Models) =================
    feat_imp_path = None
    if hasattr(model, 'feature_importances_') and feature_names:
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1][:20]  # Top 20 features
        top_features = [feature_names[i] for i in indices]
        top_importances = importances[indices]

        fig, ax = plt.subplots(figsize=(11, 8))
        y_pos = np.arange(len(top_features))
        colors = plt.cm.plasma(np.linspace(0.2, 0.9, len(top_features)))
        bars = ax.barh(y_pos, top_importances, color=colors, height=0.65)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(top_features, fontsize=9)
        ax.invert_yaxis()
        ax.set_title(f"Top 20 Critical Network Traffic Features - {model_name} ({task_name})", fontsize=13, weight='bold')
        ax.set_xlabel("Feature Importance Value", fontsize=11, weight='bold')
        ax.grid(axis='x', linestyle='--', alpha=0.5)

        for bar in bars:
            w = bar.get_width()
            ax.text(w + (max(top_importances) * 0.01), bar.get_y() + bar.get_height() / 2., f"{w:.4f}",
                    va='center', fontsize=8)

        plt.tight_layout()
        feat_imp_path = os.path.join(FIGURES_DIR, f"eval_feat_importance_{model_name}_{task_name}.png")
        plt.savefig(feat_imp_path, dpi=300)
        plt.close()
        print(f"[Saved Plot] Feature Importances -> {feat_imp_path}")

    # 4. Save Metrics Summary
    metrics_summary = {
        "model_name": model_name,
        "task_name": task_name,
        "test_samples": int(len(y_test)),
        "accuracy": round(float(acc), 4),
        "weighted_precision": round(float(prec_w), 4),
        "weighted_recall": round(float(rec_w), 4),
        "weighted_f1": round(float(f1_w), 4),
        "macro_precision": round(float(prec_m), 4),
        "macro_recall": round(float(rec_m), 4),
        "macro_f1": round(float(f1_m), 4),
        "classification_report": clf_report,
        "confusion_matrix_csv": os.path.relpath(cm_path),
        "normalized_confusion_matrix_csv": os.path.relpath(cm_norm_path),
        "class_metrics_csv": os.path.relpath(class_metrics_path),
        **(validation_metrics or {})
    }

    json_path = os.path.join(METRICS_DIR, f"eval_metrics_{model_name}_{task_name}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(metrics_summary, f, indent=4)
    print(f"[Saved Metrics] JSON -> {json_path}")
    print(f"{'='*70}\n")

    return metrics_summary

def plot_model_comparison(results_list: list, task_name: str = "8_categories"):
    """
    Generates a comparative leaderboard plot comparing Accuracy, Weighted F1, and Macro F1 across all trained models.
    """
    if not results_list:
        return None

    models = [r['model_name'] for r in results_list]
    x = np.arange(len(models))
    metric_series = [
        ("Accuracy", "accuracy", "#1f77b4"),
        ("Weighted precision", "weighted_precision", "#9467bd"),
        ("Weighted recall", "weighted_recall", "#8c564b"),
        ("Weighted F1", "weighted_f1", "#2ca02c"),
        ("Macro precision", "macro_precision", "#e377c2"),
        ("Macro recall", "macro_recall", "#17becf"),
        ("Macro F1", "macro_f1", "#ff7f0e")
    ]
    width = 0.12

    fig, ax = plt.subplots(figsize=(14, 7))
    for metric_index, (label, key, color) in enumerate(metric_series):
        values = [r[key] * 100 for r in results_list]
        offset = (metric_index - (len(metric_series) - 1) / 2) * width
        ax.bar(x + offset, values, width, label=f"{label} (%)", color=color)

    ax.set_ylabel('Score (%)', fontsize=12, weight='bold')
    ax.set_xlabel('Machine Learning Algorithm', fontsize=12, weight='bold')
    ax.set_title(f"Model Tournament Leaderboard - CICIoT2023 ({task_name})", fontsize=14, weight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=11, weight='semibold')
    ax.set_ylim(0, 105)
    ax.legend(loc='lower right', frameon=True)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    chart_path = os.path.join(FIGURES_DIR, f"eval_tournament_leaderboard_{task_name}.png")
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"\n[Tournament Plot Saved] Model Leaderboard -> {chart_path}")
    return chart_path
