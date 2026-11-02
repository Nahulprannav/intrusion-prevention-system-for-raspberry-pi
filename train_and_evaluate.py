"""
Model Training and Tournament Evaluation Runner for CICIoT2023.
Trains selected tabular models, generates confusion matrices and per-class metrics,
and exports the validation-selected champion model.
"""
import os
import sys
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.train import train_pipeline

def main():
    parser = argparse.ArgumentParser(description="CICIoT2023 Intrusion Detection Training Engine")
    parser.add_argument(
        "--task",
        type=str,
        default="category",
        choices=["category", "multiclass", "binary"],
        help="Classification level: 'category' (8 macro classes), 'multiclass' (34 specific classes), or 'binary' (Attack vs Benign)"
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=["LIGHTGBM", "XGBOOST", "CATBOOST", "RANDOM_FOREST", "EXTRA_TREES", "HIST_GRADIENT_BOOSTING", "PYTORCH_MLP"],
        help="List of models to train and compare in the tournament"
    )
    parser.add_argument(
        "--resample",
        action="store_true",
        help="Force re-sampling from raw CSV files"
    )
    args = parser.parse_args()

    print("="*75)
    print(f"       CICIOT2023 MODEL TRAINING & EVALUATION PIPELINE")
    print(f"       Task Level: {args.task.upper()}")
    print(f"       Selected Models: {', '.join(args.models)}")
    print("="*75)

    results = train_pipeline(
        task=args.task,
        selected_models=args.models,
        force_resample=args.resample
    )

    print("\n[SUCCESS] Model training tournament completed successfully!")
    print("Visual outputs saved in: 'results/figures/'")
    print("Metric summaries saved in: 'results/metrics/'")
    print("Saved champion models in: 'saved_models/'")

if __name__ == "__main__":
    main()
