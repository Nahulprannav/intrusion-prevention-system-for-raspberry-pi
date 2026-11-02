"""Compare classic tabular models with TabPFN on identical small training subsets."""
import argparse
import importlib.util
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.train import train_pipeline


MODELS = [
    "XGBOOST",
    "LIGHTGBM",
    "CATBOOST",
    "RANDOM_FOREST",
    "EXTRA_TREES",
    "HIST_GRADIENT_BOOSTING",
    "PYTORCH_MLP",
    "FT_TRANSFORMER_FROM_SCRATCH",
    "TABPFN"
]
TASKS = ("category", "binary")
TRAIN_SAMPLE_SIZE = 1000


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-tabpfn",
        action="store_true",
        help="Compare the non-foundation baselines without loading pretrained weights"
    )
    args = parser.parse_args()

    models = [model for model in MODELS if not args.skip_tabpfn or model != "TABPFN"]
    if "TABPFN" in models and importlib.util.find_spec("tabpfn") is None:
        raise SystemExit(
            "TabPFN is optional. Install it with "
            "'python -m pip install -r requirements-tabular-foundation.txt'."
        )

    for task in TASKS:
        print(
            f"\n### Shared-data model comparison: {task}, "
            f"{TRAIN_SAMPLE_SIZE} stratified training rows",
            flush=True
        )
        results = train_pipeline(
            task=task,
            selected_models=models,
            max_train_samples=TRAIN_SAMPLE_SIZE,
            experiment_suffix=f"shared_{TRAIN_SAMPLE_SIZE}",
            save_champion=False
        )
        completed = {result["model_name"].upper() for result in results}
        missing = [model for model in models if model not in completed]
        if missing:
            raise SystemExit(
                f"{task} comparison incomplete. Models without test results: "
                f"{', '.join(missing)}. Check the logged error; TabPFN model "
                "weights may require license acceptance and a first-use download."
            )

    print("\n[SUCCESS] All shared-subset comparisons completed.")
    print("See results/reports/evaluation_report.md for tables and charts.")


if __name__ == "__main__":
    main()
