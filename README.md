# CICIoT2023 Network Intrusion Detection System (IDS)

An experimental Machine Learning and Deep Learning project for classifying IoT network attacks using the **CICIoT2023** (Canadian Institute for Cybersecurity) benchmark dataset. The IPS module currently generates firewall commands for demonstration; it does not apply them to the host.

---

## Project Results & Performance Overview

The numbers below are held-out test results on the cached sampled dataset (16,598 records per task). The main tournament trains all models on the same training split and chooses the saved champion using **validation macro F1**, never test scores. Full per-class results, confusion matrices, CSVs, validation scores, and charts are available in the [detailed evaluation report](results/reports/evaluation_report.md).

### 1. Macro Threat Categories Tournament (8 Classes)
Target: `DDoS`, `DoS`, `Mirai`, `Recon`, `Spoofing`, `Web_Attack`, `Brute_Force`, `Benign`

| Model | Accuracy | Weighted precision | Weighted recall | Weighted F1 | Macro F1 | Validation macro F1 | Train time (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **XGBoost** | 95.51% | 95.56% | 95.51% | 95.47% | **88.86%** | 88.82% | 6.76 |
| **LightGBM** | 95.44% | 95.47% | 95.44% | 95.40% | 88.53% | **89.18%** | 6.76 |
| **HistGradientBoosting** | **95.53%** | **95.54%** | **95.53%** | **95.51%** | 88.79% | 88.97% | 6.50 |
| **CatBoost** | 94.73% | 94.86% | 94.73% | 94.62% | 86.74% | 86.81% | 7.33 |
| **Random Forest** | 94.29% | 94.42% | 94.29% | 94.14% | 85.48% | 85.33% | 1.64 |
| **Extra Trees** | 81.93% | 83.76% | 81.93% | 79.82% | 69.79% | 68.99% | 1.04 |
| **PyTorch MLP** | 78.76% | 79.09% | 78.76% | 77.74% | 66.30% | 65.80% | 28.02 |

---

### 2. Fine-Grained Attack Tournament (34 Classes)
Target: Full 34 attack types (e.g., `Mirai-greeth_flood`, `DDoS-SlowLoris`, `MITM-ArpSpoofing`, `SqlInjection`, `DictionaryBruteForce`, etc.)

| Model | Accuracy | Weighted precision | Weighted recall | Weighted F1 | Macro F1 | Validation macro F1 | Train time (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **XGBoost** | **93.11%** | **93.00%** | **93.11%** | **93.00%** | **85.66%** | **86.54%** | 17.23 |
| **HistGradientBoosting** | 92.85% | 92.76% | 92.85% | 92.77% | 85.40% | 86.36% | 13.80 |
| **CatBoost** | 91.61% | 91.76% | 91.61% | 91.46% | 84.51% | 84.40% | 53.44 |
| **Random Forest** | 90.64% | 90.93% | 90.64% | 90.03% | 78.66% | 79.11% | 2.44 |
| **Extra Trees** | 78.58% | 80.76% | 78.58% | 77.99% | 69.52% | 70.06% | 0.99 |
| **PyTorch MLP** | 69.79% | 71.75% | 69.79% | 68.02% | 59.09% | 59.26% | 27.31 |
| **LightGBM** | 18.69% | 21.29% | 18.69% | 13.44% | 10.93% | 11.12% | 9.39 |

### Binary Attack vs Benign (2 classes)

| Model | Accuracy | Weighted precision | Weighted recall | Weighted F1 | Macro F1 | Validation macro F1 | Train time (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **XGBoost** | 98.73% | 98.68% | 98.73% | 98.69% | **90.21%** | 90.08% | 0.52 |
| **HistGradientBoosting** | **98.67%** | **98.61%** | **98.67%** | **98.62%** | 89.82% | **90.29%** | 2.25 |
| **LightGBM** | 98.66% | 98.60% | 98.66% | 98.61% | 89.62% | 89.58% | 0.61 |
| **CatBoost** | 98.63% | 98.55% | 98.63% | 98.56% | 89.17% | 89.24% | 2.73 |
| **Random Forest** | 98.43% | 98.34% | 98.43% | 98.30% | 86.84% | 87.04% | 1.16 |
| **Extra Trees** | 97.22% | 97.02% | 97.22% | 96.48% | 69.62% | 70.12% | 0.84 |
| **PyTorch MLP** | 97.14% | 96.66% | 97.14% | 96.66% | 72.64% | 72.11% | 29.81 |

### Model selection and tabular foundation models

The current data supports a task-specific conclusion: **keep boosted trees as the leading family, but do not declare one universal champion**. The saved champions were selected on validation macro F1: LightGBM for categories, XGBoost for the 34-class task, and HistGradientBoosting for binary. Test scores are reported for comparison, not used to select those artifacts. HistGradientBoosting is competitive on categories and binary; XGBoost leads the 34-class test metrics; LightGBM's 34-class result is a clear warning that boosting implementations can behave very differently. The 2-class accuracy is not enough to pick an IPS model: benign-class recall remains much lower than attack recall, so the class-level results and false-negative costs matter.

The repository's FT-Transformer-style model is **trained from scratch**, not a tabular foundation model: it has random initialization and learns weights on this project’s training split. In the existing edge benchmark it reached 87.46% accuracy and 60.77% macro F1 in 272.91 s; edge XGBoost reached 94.73% accuracy and 86.73% macro F1 in 5.04 s. Their measured single-row latencies were 1.132 ms and 0.661 ms, respectively. These are measurements from the development host, not a Raspberry Pi. On this evidence, the scratch transformer is not the deployment or accuracy leader.

**TabPFN is a different and worthwhile research candidate** because it is pretrained and performs in-context prediction rather than fitting a new neural network from random weights for every dataset. This project has 46 numerical features and an 8-class task, within the TabPFNv2 documented limits (up to 10 classes and 500 features). A shared-subset comparison now reports eight non-TabPFN models on the same stratified 1,000 training rows. In that low-data comparison, LightGBM reaches 78.61% macro F1 on categories and 82.02% on binary classification; the scratch FT-Transformer reaches 13.90% and 49.08%, respectively. This is not a direct replacement for the full-training-set tournament. TabPFN's comparison code is ready, but its pretrained checkpoint has not been downloaded or run because the model-weight license must first be accepted by the user. TabPFN is not included in the 34-class run.

**My recommendation:** retain XGBoost as the 34-class baseline; treat LightGBM and HistGradientBoosting as co-leading candidates on simpler tasks, pending repeated-seed validation. Keep the compact decision tree as an edge-size/latency candidate. Do not select TabPFN (or any neural model) by reputation: consider it a winner only if class-specific metrics, inference latency, memory, model size, and licensing beat the right tree baseline for the deployment. The published TabPFNv2 weights use the Prior Labs License with an additional attribution requirement; this repository does not redistribute those weights.

Sources: [TabPFN paper](https://arxiv.org/abs/2207.01848), [official TabPFN model documentation](https://docs.priorlabs.ai/models.md), [TabPFNv2 weights license](https://huggingface.co/Prior-Labs/TabPFN-v2-clf/blob/main/LICENSE.txt).

---

## 🔍 Key Findings & Dataset Insights

1. **Massive Scale & Severe Imbalance**:
   - Total rows: **~7.85 million records** across train, validation, and test sets.
   - Attack prevalence ranges from over **848,000 instances** (`DDoS-ICMP_Flood`) down to just **140 instances** (`Uploading_Attack`) and **249 instances** (`Recon-PingSweep`).
   - *Previous Code Flaw*: Reading naive slices like `nrows=50000` dropped rare attacks completely and omitted 3 classes entirely from test data.
   - *Our Solution*: Chunk-based stratified streaming guarantees 100% representation for rare classes while bounding majority classes, compressing memory from 2.3 GB down to ~16 MB in Parquet format.

2. **Top Discriminator Features**:
   - `Header_Length`: Distinguishes volumetric floods from normal TCP/UDP packets.
   - `Rate` and `Srate`: Source packet transmission rate strongly identifies DDoS and DoS saturation.
   - `Tot sum`, `Tot size`, `AVG`, `Std`: Flow volume metrics separating normal browsing from automated botnet sweeps.
   - Flag counts (`syn_count`, `ack_count`, `fin_count`): Differentiates SYN floods, ACK fragmentation, and port scanning.

---

## 📁 Repository Structure

```
archive (2)/
├── CICIOT23/                                # Download separately; excluded from Git
│   ├── train/train.csv                      # ~5.49M records (1.62 GB)
│   ├── validation/validation.csv            # ~1.18M records (348 MB)
│   └── test/test.csv                        # ~1.18M records (348 MB)
│
├── data_sampled/                            # Cached Stratified Datasets (Parquet)
│   ├── train_stratified.parquet             # 69,611 balanced records (4.8 MB)
│   ├── val_stratified.parquet               # 16,592 balanced records (1.2 MB)
│   └── test_stratified.parquet              # 16,598 balanced records (1.2 MB)
│
├── saved_models/                            # Serialized trained model pipelines
│   ├── champion_category_pipeline.joblib    # Best 8-class model (XGBoost + Scaler + Encoder)
│   ├── champion_multiclass_pipeline.joblib  # Best 34-class model pipeline
│   └── champion_binary_pipeline.joblib      # Best binary model pipeline
│
├── results/
│   ├── figures/                             # Visual Plots (300 DPI)
│   │   ├── eda_class_distribution_34.png
│   │   ├── eda_macro_categories.png
│   │   ├── eda_feature_correlation.png
│   │   ├── eda_protocol_distribution.png
│   │   ├── eval_tournament_leaderboard_category.png
│   │   ├── eval_tournament_leaderboard_multiclass.png
│   │   ├── eval_cm_XGBOOST_category.png
│   │   ├── eval_cm_XGBOOST_multiclass.png
│   │   ├── eval_feat_importance_XGBOOST_category.png
│   │   └── eval_f1_per_class_XGBOOST_category.png
│   ├── metrics/                             # JSON reports, confusion matrices & CSV leaderboards
│       ├── eda_summary.json
│       ├── leaderboard_category.csv
│       ├── leaderboard_multiclass.csv
│       └── eval_metrics_*.json
│   └── reports/                             # Detailed Markdown report with linked charts/tables
│
├── src/                                     # Core Modular Python Engine
│   ├── __init__.py
│   ├── config.py                            # Path configs, mappings, hyperparameters
│   ├── data_loader.py                       # Chunked streaming stratified sampler
│   ├── eda.py                               # Statistical analysis & visualization generator
│   ├── models.py                            # Boosted trees, forests, HistGB, MLP, optional TabPFN
│   ├── train.py                             # Tournament training & champion selection
│   ├── evaluate.py                          # Metric computation & plotting engine
│   ├── reporting.py                         # Consolidated evaluation report generator
│   └── inference.py                         # Real-time packet threat detection engine
│
├── eda_analysis.py                          # Standalone EDA Runner
├── train_and_evaluate.py                    # Standalone Model Training Runner
├── run_inference.py                         # Standalone Live Prediction CLI
├── run_full_evaluation.py                   # Train/test every supported model on all tasks
├── run_tabular_comparison.py                # Compare models on a shared 1,000-row subset
├── run_pipeline.py                          # Master Orchestrator (Runs All Steps End-to-End)
└── CICIoT2023_Intrusion_Detection_Pipeline.ipynb # Interactive Jupyter Notebook
```

---

## 🚀 How to Run

### Environment and data
Install the Python dependencies:
```bash
python -m pip install -r requirements.txt
```

The raw dataset is not included in this repository because its CSV files exceed 2 GB. Place the official files at:
`CICIOT23/train/train.csv`, `CICIOT23/validation/validation.csv`, and `CICIOT23/test/test.csv`.
The smaller stratified Parquet samples and saved model artifacts are included for convenience.

### 1. Run the Entire End-to-End Pipeline
Executes data sampling, EDA, model training, evaluation, and live inference simulation:
```bash
python run_pipeline.py
```

### 2. Run Exploratory Data Analysis Only
Generates all distribution, correlation, and protocol charts:
```bash
python eda_analysis.py
```

### 3. Train and Benchmark Models
Train and test all supported models on 8 Macro Categories:
```bash
python train_and_evaluate.py --task category --models LIGHTGBM XGBOOST CATBOOST RANDOM_FOREST EXTRA_TREES HIST_GRADIENT_BOOSTING PYTORCH_MLP
```

Train and test all supported models on 34 Fine-Grained Classes:
```bash
python train_and_evaluate.py --task multiclass --models LIGHTGBM XGBOOST CATBOOST RANDOM_FOREST EXTRA_TREES HIST_GRADIENT_BOOSTING PYTORCH_MLP
```

Train and test all supported models on Binary Classification (Attack vs Benign):
```bash
python train_and_evaluate.py --task binary --models LIGHTGBM XGBOOST CATBOOST RANDOM_FOREST EXTRA_TREES HIST_GRADIENT_BOOSTING PYTORCH_MLP
```

Run all seven baseline models across all three tasks and fail visibly if any model does not complete:
```bash
python run_full_evaluation.py
```

For the shared-subset TabPFN comparison (category and binary tasks), install its optional dependency and run:
```bash
python -m pip install -r requirements-tabular-foundation.txt
python run_tabular_comparison.py
```
The first TabPFN run downloads its pretrained v2 checkpoint. Review and accept the linked model-weight license before running it; the code does not bundle or redistribute the weights. The 1,000-row cap is used to make the comparison reproducible and practical on CPU; all compared models receive the same sampled training records.

To run the same-data comparison without downloading/using TabPFN weights:
```bash
python run_tabular_comparison.py --skip-tabpfn
```

Each successfully trained model is evaluated against the held-out test split. Evaluation creates overall and per-class precision, recall, and F1 metrics; accuracy; a normalized confusion-matrix image; raw and normalized confusion-matrix CSVs; per-class metric CSVs; and a tournament comparison chart.

Generate or refresh a consolidated Markdown report from the saved evaluation outputs:
```bash
python -m src.reporting
```
The report is saved to [`results/reports/evaluation_report.md`](results/reports/evaluation_report.md). It contains comparison tables, per-class score tables, confusion matrices, and dataset/benchmark visuals. Individual JSON metrics and CSV tables are saved in `results/metrics/`; images are saved in `results/figures/`.

### 4. Run Real-Time Threat Detection on Live Traffic
Inspect 10 sample packets and output threat alerts with confidence scores:
```bash
python run_inference.py --samples 10 --task category
```

Example Output:
```
=====================================================================================
                 REAL-TIME NETWORK INTRUSION DETECTION MONITOR
=====================================================================================
 Sample_ID        Actual_Raw_Label Predicted_Threat Confidence                      Severity_Level
         1 DDoS-SynonymousIP_Flood             DDoS     99.99% CRITICAL (Denial of Service Attack)
         2         DDoS-ICMP_Flood             DDoS     99.99% CRITICAL (Denial of Service Attack)
         3          DDoS-TCP_Flood             DDoS     99.99% CRITICAL (Denial of Service Attack)
         4           DoS-SYN_Flood              DoS     99.95% CRITICAL (Denial of Service Attack)
         5 DDoS-SynonymousIP_Flood             DDoS     99.99% CRITICAL (Denial of Service Attack)
         6 DDoS-SynonymousIP_Flood             DDoS     99.99% CRITICAL (Denial of Service Attack)
         7       DDoS-PSHACK_Flood             DDoS     99.99% CRITICAL (Denial of Service Attack)
         8           DoS-TCP_Flood              DoS     99.97% CRITICAL (Denial of Service Attack)
         9 DDoS-SynonymousIP_Flood             DDoS     99.99% CRITICAL (Denial of Service Attack)
        10        DDoS-RSTFINFlood             DDoS     99.99% CRITICAL (Denial of Service Attack)
=====================================================================================
```

---

## 📓 Running the Jupyter Notebook
Open `CICIoT2023_Intrusion_Detection_Pipeline.ipynb` in VS Code, JupyterLab, or Google Colab to step through the code interactively with inline charts!

## ⚠️ Limitations and recommended next steps

- The stratified sampler takes up to a per-class cap while streaming in file order. For less order-sensitive samples, use reservoir sampling or shuffle source data before sampling, and document the sampling seed and split provenance.
- Validate the final model on the complete, untouched test split (not only the cached sample), report class-level performance, and consider confidence intervals and repeated seeds.
- The current pipeline generates per-class metrics but does not yet include ROC/precision-recall curves, probability calibration, or threshold tuning; add these before selecting operational alert thresholds.
- Benchmark inference on the actual Raspberry Pi hardware and report warm-up, batch size, memory, and repeated latency percentiles. Host-machine timing is not evidence of Pi performance.
- Firewall rules are strings for a simulation, not production enforcement. Before enabling automatic blocking, add strict IP/port validation, a dry-run mode, allowlists, rollback/expiry, audit review, and isolated integration tests.
- Pin dependency versions and add automated tests for preprocessing consistency, all task types, report generation, and serialized model compatibility.
