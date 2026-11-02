"""Train and test every supported model for all configured classification tasks."""
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.train import train_pipeline


TASKS = ("category", "multiclass", "binary")
MODELS = (
    "LIGHTGBM",
    "XGBOOST",
    "CATBOOST",
    "RANDOM_FOREST",
    "EXTRA_TREES",
    "HIST_GRADIENT_BOOSTING",
    "PYTORCH_MLP"
)


def main():
    incomplete = []
    for task in TASKS:
        print(f"\n### Full model evaluation: {task}", flush=True)
        results = train_pipeline(task=task, selected_models=list(MODELS))
        completed = {result["model_name"].upper() for result in results}
        missing = [model for model in MODELS if model not in completed]
        if missing:
            incomplete.append((task, missing))
            print(f"[INCOMPLETE] {task}: models without test metrics: {', '.join(missing)}", flush=True)

    if incomplete:
        details = "; ".join(f"{task}: {', '.join(models)}" for task, models in incomplete)
        raise SystemExit(f"Some model runs did not complete successfully: {details}")

    print("\n[SUCCESS] All supported models were trained and evaluated on the held-out test split.")
    print("Detailed report: results/reports/evaluation_report.md")


if __name__ == "__main__":
    main()
