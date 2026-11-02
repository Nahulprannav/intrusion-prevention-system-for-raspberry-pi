import csv
import glob
import json
import os

from src.config import FIGURES_DIR, METRICS_DIR, RESULTS_DIR


def _percentage(value):
    return f"{value * 100:.2f}%"


def _relative_path(path):
    return os.path.relpath(path, os.path.join(RESULTS_DIR, "reports")).replace(os.sep, "/")


def generate_evaluation_report():
    """Build a Markdown report from the saved test metrics, tables, and plots."""
    report_dir = os.path.join(RESULTS_DIR, "reports")
    os.makedirs(report_dir, exist_ok=True)

    leaderboard_times = {}
    for path in glob.glob(os.path.join(METRICS_DIR, "leaderboard_*.csv")):
        with open(path, newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                task = os.path.basename(path)[len("leaderboard_"):-len(".csv")]
                leaderboard_times[(task, row["Model"])] = row.get("Training_Time_s", "")

    metrics_files = sorted(glob.glob(os.path.join(METRICS_DIR, "eval_metrics_*.json")))
    report = [
        "# Model Evaluation Report",
        "",
        "All reported test scores are measured on the held-out test split after fitting each model on the training split. The saved champion is selected by validation macro F1, not test scores, to avoid letting majority classes dominate model choice.",
        "Precision, recall, and F1 are shown as both weighted and macro averages; per-class results are included below.",
        "Confusion matrices include raw counts and row-normalized rates.",
        ""
    ]

    task_metrics = {}
    for path in metrics_files:
        with open(path, encoding="utf-8") as file:
            metrics = json.load(file)
        task_metrics.setdefault(metrics["task_name"], []).append(metrics)

    if not task_metrics:
        report.append("No evaluation JSON files were found. Run `python train_and_evaluate.py` first.")

    for task, models in sorted(task_metrics.items()):
        models.sort(
            key=lambda result: result.get("validation_macro_f1", result["macro_f1"]),
            reverse=True
        )
        report.extend([
            f"## {task.title()} classification",
            "",
            "| Model | Validation weighted F1 | Validation macro F1 | Accuracy | Weighted precision | Weighted recall | Weighted F1 | Macro precision | Macro recall | Macro F1 | Train time (s) |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"
        ])
        for metrics in models:
            model_name = metrics["model_name"]
            train_time = leaderboard_times.get((task, model_name), "n/a") or "n/a"
            report.append(
                f"| {model_name} | {_percentage(metrics['validation_weighted_f1']) if 'validation_weighted_f1' in metrics else 'n/a'} "
                f"| {_percentage(metrics['validation_macro_f1']) if 'validation_macro_f1' in metrics else 'n/a'} "
                f"| {_percentage(metrics['accuracy'])} "
                f"| {_percentage(metrics['weighted_precision'])} "
                f"| {_percentage(metrics['weighted_recall'])} "
                f"| {_percentage(metrics['weighted_f1'])} "
                f"| {_percentage(metrics['macro_precision'])} "
                f"| {_percentage(metrics['macro_recall'])} "
                f"| {_percentage(metrics['macro_f1'])} | {train_time} |"
            )

        leaderboard_figure = os.path.join(FIGURES_DIR, f"eval_tournament_leaderboard_{task}.png")
        if os.path.isfile(leaderboard_figure):
            report.extend([
                "",
                f"![{task} model comparison]({_relative_path(leaderboard_figure)})"
            ])

        for metrics in models:
            model_name = metrics["model_name"]
            report.extend([
                "",
                f"### {model_name}",
                "",
                f"Test samples: **{metrics.get('test_samples', 'not recorded')}**",
                "",
                "| Class | Precision | Recall | F1 score | Support |",
                "|---|---:|---:|---:|---:|"
            ])
            class_report = metrics["classification_report"]
            for class_name, scores in class_report.items():
                if class_name in {"accuracy", "macro avg", "weighted avg"}:
                    continue
                report.append(
                    f"| {class_name} | {_percentage(scores['precision'])} "
                    f"| {_percentage(scores['recall'])} | {_percentage(scores['f1-score'])} "
                    f"| {int(scores['support'])} |"
                )

            confusion_figure = os.path.join(FIGURES_DIR, f"eval_cm_{model_name}_{task}.png")
            score_figure = os.path.join(FIGURES_DIR, f"eval_f1_per_class_{model_name}_{task}.png")
            if os.path.isfile(confusion_figure):
                report.extend([
                    "",
                    f"![{model_name} normalized confusion matrix]({_relative_path(confusion_figure)})"
                ])
            if os.path.isfile(score_figure):
                report.extend([
                    "",
                    f"![{model_name} per-class precision, recall and F1]({_relative_path(score_figure)})"
                ])

            artifacts = [
                ("Raw confusion matrix CSV", f"confusion_matrix_{model_name}_{task}.csv"),
                ("Normalized confusion matrix CSV", f"confusion_matrix_normalized_{model_name}_{task}.csv"),
                ("Per-class metrics CSV", f"class_metrics_{model_name}_{task}.csv")
            ]
            links = [
                f"[{label}]({_relative_path(os.path.join(METRICS_DIR, filename))})"
                for label, filename in artifacts
                if os.path.isfile(os.path.join(METRICS_DIR, filename))
            ]
            if links:
                report.extend(["", "Data: " + ", ".join(links)])
            report.append("")

    report.extend(["## Dataset visuals", ""])
    for title, filename in [
        ("34-class distribution", "eda_class_distribution_34.png"),
        ("Macro-category distribution", "eda_macro_categories.png"),
        ("Feature correlation", "eda_feature_correlation.png"),
        ("Protocol distribution", "eda_protocol_distribution.png")
    ]:
        image_path = os.path.join(FIGURES_DIR, filename)
        if os.path.isfile(image_path):
            report.extend([f"### {title}", "", f"![{title}]({_relative_path(image_path)})", ""])

    benchmark_csv = os.path.join(METRICS_DIR, "raspberry_pi_edge_benchmark.csv")
    if os.path.isfile(benchmark_csv):
        report.extend([
            "## Raspberry Pi edge benchmark",
            "",
            "These figures describe the machine used to run the benchmark, not necessarily a Raspberry Pi.",
            "",
            f"[Benchmark results CSV]({_relative_path(benchmark_csv)})"
        ])
        for title, filename in [
            ("Accuracy and inference latency", "eval_rpi_latency_vs_accuracy.png"),
            ("Resource footprint", "eval_rpi_resource_footprint.png"),
            ("Feature importance", "eval_rpi_feature_importance_iat.png")
        ]:
            image_path = os.path.join(FIGURES_DIR, filename)
            if os.path.isfile(image_path):
                report.extend(["", f"### {title}", "", f"![{title}]({_relative_path(image_path)})"])

    report.extend([
        "## Dataset and interpretation notes",
        "",
        "- The test scores apply to the cached stratified sample and should not be interpreted as full-dataset or live-network performance.",
        "- Macro averages weight each class equally; weighted averages account for class support.",
        "- A high accuracy with a lower macro F1 can indicate weaker performance on underrepresented classes.",
        "- Edge benchmark latency must be measured on the actual target Raspberry Pi before deployment.",
        ""
    ])

    output_path = os.path.join(report_dir, "evaluation_report.md")
    with open(output_path, "w", encoding="utf-8", newline="\n") as file:
        file.write("\n".join(report))
    print(f"[Report Saved] {output_path}")
    return output_path


if __name__ == "__main__":
    generate_evaluation_report()
