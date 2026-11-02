# Model Evaluation Report

All reported scores are measured on the held-out test split after fitting each model on the training split.
Precision, recall, and F1 are shown as both weighted and macro averages; per-class results are included below.
Confusion matrices include raw counts and row-normalized rates.

## Binary classification

| Model | Accuracy | Weighted precision | Weighted recall | Weighted F1 | Macro precision | Macro recall | Macro F1 | Train time (s) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| XGBOOST | 98.73% | 98.68% | 98.73% | 98.69% | 93.65% | 87.31% | 90.21% | 0.54 |
| LIGHTGBM | 98.66% | 98.60% | 98.66% | 98.61% | 93.18% | 86.63% | 89.62% | 0.68 |
| CATBOOST | 98.63% | 98.55% | 98.63% | 98.56% | 93.53% | 85.65% | 89.17% | 2.58 |
| RANDOM_FOREST | 98.43% | 98.34% | 98.43% | 98.30% | 94.36% | 81.62% | 86.84% | 1.14 |
| PYTORCH_MLP | 97.11% | 96.61% | 97.11% | 96.60% | 84.62% | 66.42% | 72.01% | 35.7 |
| EXTRA_TREES | 97.22% | 97.02% | 97.22% | 96.48% | 93.29% | 63.11% | 69.62% | 0.66 |

![binary model comparison](../figures/eval_tournament_leaderboard_binary.png)

### XGBOOST

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Attack | 99.07% | 99.62% | 99.35% | 15998 |
| Benign | 88.24% | 75.00% | 81.08% | 600 |

![XGBOOST normalized confusion matrix](../figures/eval_cm_XGBOOST_binary.png)

![XGBOOST per-class precision, recall and F1](../figures/eval_f1_per_class_XGBOOST_binary.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_XGBOOST_binary.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_XGBOOST_binary.csv), [Per-class metrics CSV](../metrics/class_metrics_XGBOOST_binary.csv)


### LIGHTGBM

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Attack | 99.02% | 99.60% | 99.31% | 15998 |
| Benign | 87.35% | 73.67% | 79.93% | 600 |

![LIGHTGBM normalized confusion matrix](../figures/eval_cm_LIGHTGBM_binary.png)

![LIGHTGBM per-class precision, recall and F1](../figures/eval_f1_per_class_LIGHTGBM_binary.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_LIGHTGBM_binary.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_LIGHTGBM_binary.csv), [Per-class metrics CSV](../metrics/class_metrics_LIGHTGBM_binary.csv)


### CATBOOST

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Attack | 98.94% | 99.64% | 99.29% | 15998 |
| Benign | 88.11% | 71.67% | 79.04% | 600 |

![CATBOOST normalized confusion matrix](../figures/eval_cm_CATBOOST_binary.png)

![CATBOOST per-class precision, recall and F1](../figures/eval_f1_per_class_CATBOOST_binary.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_CATBOOST_binary.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_CATBOOST_binary.csv), [Per-class metrics CSV](../metrics/class_metrics_CATBOOST_binary.csv)


### RANDOM_FOREST

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Attack | 98.65% | 99.74% | 99.19% | 15998 |
| Benign | 90.07% | 63.50% | 74.49% | 600 |

![RANDOM_FOREST normalized confusion matrix](../figures/eval_cm_RANDOM_FOREST_binary.png)

![RANDOM_FOREST per-class precision, recall and F1](../figures/eval_f1_per_class_RANDOM_FOREST_binary.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_RANDOM_FOREST_binary.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_RANDOM_FOREST_binary.csv), [Per-class metrics CSV](../metrics/class_metrics_RANDOM_FOREST_binary.csv)


### PYTORCH_MLP

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Attack | 97.55% | 99.51% | 98.52% | 15998 |
| Benign | 71.68% | 33.33% | 45.51% | 600 |

![PYTORCH_MLP normalized confusion matrix](../figures/eval_cm_PYTORCH_MLP_binary.png)

![PYTORCH_MLP per-class precision, recall and F1](../figures/eval_f1_per_class_PYTORCH_MLP_binary.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_PYTORCH_MLP_binary.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_PYTORCH_MLP_binary.csv), [Per-class metrics CSV](../metrics/class_metrics_PYTORCH_MLP_binary.csv)


### EXTRA_TREES

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Attack | 97.31% | 99.88% | 98.58% | 15998 |
| Benign | 89.27% | 26.33% | 40.67% | 600 |

![EXTRA_TREES normalized confusion matrix](../figures/eval_cm_EXTRA_TREES_binary.png)

![EXTRA_TREES per-class precision, recall and F1](../figures/eval_f1_per_class_EXTRA_TREES_binary.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_EXTRA_TREES_binary.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_EXTRA_TREES_binary.csv), [Per-class metrics CSV](../metrics/class_metrics_EXTRA_TREES_binary.csv)

## Category classification

| Model | Accuracy | Weighted precision | Weighted recall | Weighted F1 | Macro precision | Macro recall | Macro F1 | Train time (s) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| XGBOOST | 95.51% | 95.56% | 95.51% | 95.47% | 90.84% | 87.46% | 88.86% | 4.48 |
| LIGHTGBM | 95.44% | 95.47% | 95.44% | 95.40% | 90.14% | 87.33% | 88.53% | 4.41 |
| CATBOOST | 94.73% | 94.86% | 94.73% | 94.62% | 90.71% | 84.48% | 86.74% | 7.9 |
| RANDOM_FOREST | 94.29% | 94.42% | 94.29% | 94.14% | 89.96% | 82.85% | 85.48% | 1.62 |
| EXTRA_TREES | 81.93% | 83.76% | 81.93% | 79.82% | 85.49% | 65.26% | 69.79% | 0.99 |
| PYTORCH_MLP | 78.97% | 79.61% | 78.97% | 78.69% | 72.79% | 66.55% | 66.98% | 35.28 |

![category model comparison](../figures/eval_tournament_leaderboard_category.png)

### XGBOOST

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Benign | 84.42% | 79.50% | 81.89% | 600 |
| Brute_Force | 92.24% | 67.08% | 77.68% | 319 |
| DDoS | 99.96% | 99.97% | 99.97% | 7200 |
| DoS | 99.96% | 99.88% | 99.92% | 2400 |
| Mirai | 100.00% | 99.94% | 99.97% | 1800 |
| Recon | 86.72% | 92.91% | 89.71% | 2453 |
| Spoofing | 89.48% | 84.33% | 86.83% | 1200 |
| Web_Attack | 73.91% | 76.04% | 74.96% | 626 |

![XGBOOST normalized confusion matrix](../figures/eval_cm_XGBOOST_category.png)

![XGBOOST per-class precision, recall and F1](../figures/eval_f1_per_class_XGBOOST_category.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_XGBOOST_category.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_XGBOOST_category.csv), [Per-class metrics CSV](../metrics/class_metrics_XGBOOST_category.csv)


### LIGHTGBM

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Benign | 84.50% | 78.17% | 81.21% | 600 |
| Brute_Force | 87.45% | 67.71% | 76.33% | 319 |
| DDoS | 99.93% | 99.97% | 99.95% | 7200 |
| DoS | 99.96% | 99.83% | 99.90% | 2400 |
| Mirai | 100.00% | 100.00% | 100.00% | 1800 |
| Recon | 87.18% | 92.91% | 89.95% | 2453 |
| Spoofing | 89.34% | 83.83% | 86.50% | 1200 |
| Web_Attack | 72.71% | 76.20% | 74.41% | 626 |

![LIGHTGBM normalized confusion matrix](../figures/eval_cm_LIGHTGBM_category.png)

![LIGHTGBM per-class precision, recall and F1](../figures/eval_f1_per_class_LIGHTGBM_category.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_LIGHTGBM_category.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_LIGHTGBM_category.csv), [Per-class metrics CSV](../metrics/class_metrics_LIGHTGBM_category.csv)


### CATBOOST

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Benign | 81.40% | 75.83% | 78.52% | 600 |
| Brute_Force | 98.31% | 54.55% | 70.16% | 319 |
| DDoS | 99.89% | 99.78% | 99.83% | 7200 |
| DoS | 99.79% | 99.79% | 99.79% | 2400 |
| Mirai | 99.78% | 99.61% | 99.69% | 1800 |
| Recon | 83.15% | 93.11% | 87.85% | 2453 |
| Spoofing | 86.55% | 83.67% | 85.08% | 1200 |
| Web_Attack | 76.86% | 69.49% | 72.99% | 626 |

![CATBOOST normalized confusion matrix](../figures/eval_cm_CATBOOST_category.png)

![CATBOOST per-class precision, recall and F1](../figures/eval_f1_per_class_CATBOOST_category.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_CATBOOST_category.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_CATBOOST_category.csv), [Per-class metrics CSV](../metrics/class_metrics_CATBOOST_category.csv)


### RANDOM_FOREST

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Benign | 83.83% | 70.83% | 76.78% | 600 |
| Brute_Force | 95.51% | 53.29% | 68.41% | 319 |
| DDoS | 99.81% | 99.90% | 99.85% | 7200 |
| DoS | 100.00% | 99.96% | 99.98% | 2400 |
| Mirai | 100.00% | 99.44% | 99.72% | 1800 |
| Recon | 81.11% | 93.64% | 86.93% | 2453 |
| Spoofing | 85.41% | 81.00% | 83.15% | 1200 |
| Web_Attack | 74.04% | 64.70% | 69.05% | 626 |

![RANDOM_FOREST normalized confusion matrix](../figures/eval_cm_RANDOM_FOREST_category.png)

![RANDOM_FOREST per-class precision, recall and F1](../figures/eval_f1_per_class_RANDOM_FOREST_category.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_RANDOM_FOREST_category.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_RANDOM_FOREST_category.csv), [Per-class metrics CSV](../metrics/class_metrics_RANDOM_FOREST_category.csv)


### EXTRA_TREES

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Benign | 79.15% | 52.50% | 63.13% | 600 |
| Brute_Force | 97.53% | 24.76% | 39.50% | 319 |
| DDoS | 82.10% | 98.60% | 89.59% | 7200 |
| DoS | 93.22% | 37.83% | 53.82% | 2400 |
| Mirai | 99.94% | 99.28% | 99.61% | 1800 |
| Recon | 68.49% | 91.89% | 78.48% | 2453 |
| Spoofing | 81.23% | 73.58% | 77.22% | 1200 |
| Web_Attack | 82.23% | 43.61% | 56.99% | 626 |

![EXTRA_TREES normalized confusion matrix](../figures/eval_cm_EXTRA_TREES_category.png)

![EXTRA_TREES per-class precision, recall and F1](../figures/eval_f1_per_class_EXTRA_TREES_category.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_EXTRA_TREES_category.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_EXTRA_TREES_category.csv), [Per-class metrics CSV](../metrics/class_metrics_EXTRA_TREES_category.csv)


### PYTORCH_MLP

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Benign | 64.62% | 45.67% | 53.52% | 600 |
| Brute_Force | 76.84% | 22.88% | 35.27% | 319 |
| DDoS | 86.03% | 89.58% | 87.77% | 7200 |
| DoS | 66.80% | 56.92% | 61.46% | 2400 |
| Mirai | 99.94% | 99.28% | 99.61% | 1800 |
| Recon | 76.28% | 76.44% | 76.36% | 2453 |
| Spoofing | 71.91% | 68.92% | 70.38% | 1200 |
| Web_Attack | 39.88% | 72.68% | 51.50% | 626 |

![PYTORCH_MLP normalized confusion matrix](../figures/eval_cm_PYTORCH_MLP_category.png)

![PYTORCH_MLP per-class precision, recall and F1](../figures/eval_f1_per_class_PYTORCH_MLP_category.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_PYTORCH_MLP_category.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_PYTORCH_MLP_category.csv), [Per-class metrics CSV](../metrics/class_metrics_PYTORCH_MLP_category.csv)

## Multiclass classification

| Model | Accuracy | Weighted precision | Weighted recall | Weighted F1 | Macro precision | Macro recall | Macro F1 | Train time (s) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| XGBOOST | 93.11% | 93.00% | 93.11% | 93.00% | 86.91% | 85.10% | 85.66% | 23.83 |
| CATBOOST | 91.61% | 91.76% | 91.61% | 91.46% | 87.89% | 83.02% | 84.51% | 50.21 |
| RANDOM_FOREST | 90.64% | 90.93% | 90.64% | 90.03% | 88.35% | 77.78% | 78.66% | 2.31 |
| EXTRA_TREES | 78.58% | 80.76% | 78.58% | 77.99% | 77.22% | 68.44% | 69.52% | 1.1 |
| PYTORCH_MLP | 71.30% | 73.25% | 71.30% | 69.44% | 65.24% | 60.90% | 59.90% | 31.24 |
| LIGHTGBM | 18.69% | 21.29% | 18.69% | 13.44% | 17.33% | 15.21% | 10.93% | 18.45 |

![multiclass model comparison](../figures/eval_tournament_leaderboard_multiclass.png)

### XGBOOST

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Backdoor_Malware | 58.14% | 56.18% | 57.14% | 89 |
| BenignTraffic | 78.19% | 84.83% | 81.37% | 600 |
| BrowserHijacking | 75.61% | 69.40% | 72.37% | 134 |
| CommandInjection | 66.35% | 57.98% | 61.88% | 119 |
| DDoS-ACK_Fragmentation | 100.00% | 100.00% | 100.00% | 600 |
| DDoS-HTTP_Flood | 99.66% | 99.17% | 99.42% | 600 |
| DDoS-ICMP_Flood | 100.00% | 100.00% | 100.00% | 600 |
| DDoS-ICMP_Fragmentation | 100.00% | 100.00% | 100.00% | 600 |
| DDoS-PSHACK_Flood | 100.00% | 100.00% | 100.00% | 600 |
| DDoS-RSTFINFlood | 100.00% | 100.00% | 100.00% | 600 |
| DDoS-SYN_Flood | 99.67% | 99.83% | 99.75% | 600 |
| DDoS-SlowLoris | 99.33% | 99.50% | 99.42% | 600 |
| DDoS-SynonymousIP_Flood | 100.00% | 99.83% | 99.92% | 600 |
| DDoS-TCP_Flood | 100.00% | 99.67% | 99.83% | 600 |
| DDoS-UDP_Flood | 100.00% | 100.00% | 100.00% | 600 |
| DDoS-UDP_Fragmentation | 100.00% | 99.67% | 99.83% | 600 |
| DNS_Spoofing | 76.14% | 77.67% | 76.90% | 600 |
| DictionaryBruteForce | 71.04% | 73.04% | 72.02% | 319 |
| DoS-HTTP_Flood | 100.00% | 99.83% | 99.92% | 600 |
| DoS-SYN_Flood | 100.00% | 100.00% | 100.00% | 600 |
| DoS-TCP_Flood | 99.50% | 100.00% | 99.75% | 600 |
| DoS-UDP_Flood | 100.00% | 100.00% | 100.00% | 600 |
| MITM-ArpSpoofing | 87.83% | 83.00% | 85.35% | 600 |
| Mirai-greeth_flood | 100.00% | 99.67% | 99.83% | 600 |
| Mirai-greip_flood | 99.67% | 100.00% | 99.83% | 600 |
| Mirai-udpplain | 99.67% | 99.83% | 99.75% | 600 |
| Recon-HostDiscovery | 80.96% | 87.17% | 83.95% | 600 |
| Recon-OSScan | 72.79% | 71.33% | 72.05% | 600 |
| Recon-PingSweep | 68.18% | 56.60% | 61.86% | 53 |
| Recon-PortScan | 68.62% | 74.00% | 71.21% | 600 |
| SqlInjection | 65.87% | 56.08% | 60.58% | 148 |
| Uploading_Attack | 25.00% | 3.03% | 5.41% | 33 |
| VulnerabilityScan | 99.67% | 99.50% | 99.58% | 600 |
| XSS | 63.16% | 46.60% | 53.63% | 103 |

![XGBOOST normalized confusion matrix](../figures/eval_cm_XGBOOST_multiclass.png)

![XGBOOST per-class precision, recall and F1](../figures/eval_f1_per_class_XGBOOST_multiclass.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_XGBOOST_multiclass.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_XGBOOST_multiclass.csv), [Per-class metrics CSV](../metrics/class_metrics_XGBOOST_multiclass.csv)


### CATBOOST

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Backdoor_Malware | 71.43% | 56.18% | 62.89% | 89 |
| BenignTraffic | 71.65% | 83.83% | 77.27% | 600 |
| BrowserHijacking | 87.36% | 56.72% | 68.78% | 134 |
| CommandInjection | 82.61% | 47.90% | 60.64% | 119 |
| DDoS-ACK_Fragmentation | 99.66% | 98.83% | 99.25% | 600 |
| DDoS-HTTP_Flood | 98.13% | 96.33% | 97.22% | 600 |
| DDoS-ICMP_Flood | 100.00% | 99.67% | 99.83% | 600 |
| DDoS-ICMP_Fragmentation | 99.66% | 97.83% | 98.74% | 600 |
| DDoS-PSHACK_Flood | 99.50% | 100.00% | 99.75% | 600 |
| DDoS-RSTFINFlood | 100.00% | 99.50% | 99.75% | 600 |
| DDoS-SYN_Flood | 99.83% | 99.67% | 99.75% | 600 |
| DDoS-SlowLoris | 94.88% | 98.83% | 96.82% | 600 |
| DDoS-SynonymousIP_Flood | 99.83% | 99.83% | 99.83% | 600 |
| DDoS-TCP_Flood | 100.00% | 99.50% | 99.75% | 600 |
| DDoS-UDP_Flood | 100.00% | 99.33% | 99.67% | 600 |
| DDoS-UDP_Fragmentation | 98.99% | 97.83% | 98.41% | 600 |
| DNS_Spoofing | 73.59% | 76.17% | 74.86% | 600 |
| DictionaryBruteForce | 69.90% | 65.52% | 67.64% | 319 |
| DoS-HTTP_Flood | 98.51% | 99.50% | 99.00% | 600 |
| DoS-SYN_Flood | 99.66% | 98.50% | 99.08% | 600 |
| DoS-TCP_Flood | 99.67% | 99.50% | 99.58% | 600 |
| DoS-UDP_Flood | 99.67% | 99.67% | 99.67% | 600 |
| MITM-ArpSpoofing | 84.97% | 81.00% | 82.94% | 600 |
| Mirai-greeth_flood | 99.33% | 98.17% | 98.74% | 600 |
| Mirai-greip_flood | 98.33% | 98.33% | 98.33% | 600 |
| Mirai-udpplain | 100.00% | 99.50% | 99.75% | 600 |
| Recon-HostDiscovery | 68.80% | 84.17% | 75.71% | 600 |
| Recon-OSScan | 71.22% | 65.17% | 68.06% | 600 |
| Recon-PingSweep | 94.12% | 60.38% | 73.56% | 53 |
| Recon-PortScan | 63.57% | 74.17% | 68.46% | 600 |
| SqlInjection | 67.20% | 56.76% | 61.54% | 148 |
| Uploading_Attack | 25.00% | 3.03% | 5.41% | 33 |
| VulnerabilityScan | 96.12% | 99.17% | 97.62% | 600 |
| XSS | 75.00% | 32.04% | 44.90% | 103 |

![CATBOOST normalized confusion matrix](../figures/eval_cm_CATBOOST_multiclass.png)

![CATBOOST per-class precision, recall and F1](../figures/eval_f1_per_class_CATBOOST_multiclass.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_CATBOOST_multiclass.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_CATBOOST_multiclass.csv), [Per-class metrics CSV](../metrics/class_metrics_CATBOOST_multiclass.csv)


### RANDOM_FOREST

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Backdoor_Malware | 100.00% | 13.48% | 23.76% | 89 |
| BenignTraffic | 67.82% | 81.83% | 74.17% | 600 |
| BrowserHijacking | 85.00% | 38.06% | 52.58% | 134 |
| CommandInjection | 68.92% | 42.86% | 52.85% | 119 |
| DDoS-ACK_Fragmentation | 99.83% | 99.00% | 99.41% | 600 |
| DDoS-HTTP_Flood | 99.15% | 97.50% | 98.32% | 600 |
| DDoS-ICMP_Flood | 100.00% | 100.00% | 100.00% | 600 |
| DDoS-ICMP_Fragmentation | 100.00% | 98.83% | 99.41% | 600 |
| DDoS-PSHACK_Flood | 100.00% | 100.00% | 100.00% | 600 |
| DDoS-RSTFINFlood | 100.00% | 99.83% | 99.92% | 600 |
| DDoS-SYN_Flood | 99.83% | 99.50% | 99.67% | 600 |
| DDoS-SlowLoris | 95.35% | 99.17% | 97.22% | 600 |
| DDoS-SynonymousIP_Flood | 99.67% | 99.67% | 99.67% | 600 |
| DDoS-TCP_Flood | 99.67% | 99.67% | 99.67% | 600 |
| DDoS-UDP_Flood | 100.00% | 99.33% | 99.67% | 600 |
| DDoS-UDP_Fragmentation | 99.49% | 98.17% | 98.83% | 600 |
| DNS_Spoofing | 72.71% | 76.83% | 74.72% | 600 |
| DictionaryBruteForce | 62.87% | 67.40% | 65.05% | 319 |
| DoS-HTTP_Flood | 99.34% | 99.67% | 99.50% | 600 |
| DoS-SYN_Flood | 99.66% | 98.83% | 99.25% | 600 |
| DoS-TCP_Flood | 99.83% | 99.50% | 99.67% | 600 |
| DoS-UDP_Flood | 99.50% | 99.83% | 99.67% | 600 |
| MITM-ArpSpoofing | 79.59% | 78.00% | 78.79% | 600 |
| Mirai-greeth_flood | 100.00% | 99.50% | 99.75% | 600 |
| Mirai-greip_flood | 99.83% | 98.83% | 99.33% | 600 |
| Mirai-udpplain | 100.00% | 99.50% | 99.75% | 600 |
| Recon-HostDiscovery | 67.58% | 86.17% | 75.75% | 600 |
| Recon-OSScan | 62.39% | 61.67% | 62.03% | 600 |
| Recon-PingSweep | 66.67% | 3.77% | 7.14% | 53 |
| Recon-PortScan | 60.98% | 75.00% | 67.26% | 600 |
| SqlInjection | 56.00% | 18.92% | 28.28% | 148 |
| Uploading_Attack | 100.00% | 3.03% | 5.88% | 33 |
| VulnerabilityScan | 95.67% | 99.50% | 97.55% | 600 |
| XSS | 66.67% | 11.65% | 19.83% | 103 |

![RANDOM_FOREST normalized confusion matrix](../figures/eval_cm_RANDOM_FOREST_multiclass.png)

![RANDOM_FOREST per-class precision, recall and F1](../figures/eval_f1_per_class_RANDOM_FOREST_multiclass.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_RANDOM_FOREST_multiclass.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_RANDOM_FOREST_multiclass.csv), [Per-class metrics CSV](../metrics/class_metrics_RANDOM_FOREST_multiclass.csv)


### EXTRA_TREES

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Backdoor_Malware | 97.83% | 50.56% | 66.67% | 89 |
| BenignTraffic | 46.54% | 75.00% | 57.43% | 600 |
| BrowserHijacking | 88.57% | 23.13% | 36.69% | 134 |
| CommandInjection | 63.54% | 51.26% | 56.74% | 119 |
| DDoS-ACK_Fragmentation | 99.50% | 98.83% | 99.16% | 600 |
| DDoS-HTTP_Flood | 78.35% | 83.83% | 81.00% | 600 |
| DDoS-ICMP_Flood | 100.00% | 100.00% | 100.00% | 600 |
| DDoS-ICMP_Fragmentation | 100.00% | 98.83% | 99.41% | 600 |
| DDoS-PSHACK_Flood | 100.00% | 100.00% | 100.00% | 600 |
| DDoS-RSTFINFlood | 100.00% | 99.83% | 99.92% | 600 |
| DDoS-SYN_Flood | 60.69% | 94.17% | 73.81% | 600 |
| DDoS-SlowLoris | 82.99% | 79.67% | 81.29% | 600 |
| DDoS-SynonymousIP_Flood | 98.73% | 77.50% | 86.83% | 600 |
| DDoS-TCP_Flood | 66.55% | 95.50% | 78.44% | 600 |
| DDoS-UDP_Flood | 65.46% | 96.33% | 77.95% | 600 |
| DDoS-UDP_Fragmentation | 99.33% | 98.33% | 98.83% | 600 |
| DNS_Spoofing | 57.78% | 66.83% | 61.98% | 600 |
| DictionaryBruteForce | 78.45% | 44.51% | 56.80% | 319 |
| DoS-HTTP_Flood | 85.31% | 86.17% | 85.74% | 600 |
| DoS-SYN_Flood | 91.41% | 58.50% | 71.34% | 600 |
| DoS-TCP_Flood | 91.45% | 51.67% | 66.03% | 600 |
| DoS-UDP_Flood | 93.33% | 49.00% | 64.26% | 600 |
| MITM-ArpSpoofing | 73.60% | 65.50% | 69.31% | 600 |
| Mirai-greeth_flood | 98.76% | 92.67% | 95.61% | 600 |
| Mirai-greip_flood | 93.16% | 97.67% | 95.36% | 600 |
| Mirai-udpplain | 100.00% | 99.33% | 99.67% | 600 |
| Recon-HostDiscovery | 57.65% | 75.33% | 65.32% | 600 |
| Recon-OSScan | 39.56% | 36.33% | 37.88% | 600 |
| Recon-PingSweep | 83.33% | 9.43% | 16.95% | 53 |
| Recon-PortScan | 49.68% | 52.33% | 50.97% | 600 |
| SqlInjection | 45.45% | 13.51% | 20.83% | 148 |
| Uploading_Attack | 0.00% | 0.00% | 0.00% | 33 |
| VulnerabilityScan | 88.42% | 91.67% | 90.02% | 600 |
| XSS | 50.00% | 13.59% | 21.37% | 103 |

![EXTRA_TREES normalized confusion matrix](../figures/eval_cm_EXTRA_TREES_multiclass.png)

![EXTRA_TREES per-class precision, recall and F1](../figures/eval_f1_per_class_EXTRA_TREES_multiclass.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_EXTRA_TREES_multiclass.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_EXTRA_TREES_multiclass.csv), [Per-class metrics CSV](../metrics/class_metrics_EXTRA_TREES_multiclass.csv)


### PYTORCH_MLP

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Backdoor_Malware | 36.36% | 8.99% | 14.41% | 89 |
| BenignTraffic | 63.09% | 55.83% | 59.24% | 600 |
| BrowserHijacking | 72.00% | 13.43% | 22.64% | 134 |
| CommandInjection | 31.62% | 31.09% | 31.36% | 119 |
| DDoS-ACK_Fragmentation | 99.16% | 98.83% | 99.00% | 600 |
| DDoS-HTTP_Flood | 77.47% | 83.67% | 80.45% | 600 |
| DDoS-ICMP_Flood | 100.00% | 100.00% | 100.00% | 600 |
| DDoS-ICMP_Fragmentation | 100.00% | 98.33% | 99.16% | 600 |
| DDoS-PSHACK_Flood | 100.00% | 99.67% | 99.83% | 600 |
| DDoS-RSTFINFlood | 100.00% | 99.83% | 99.92% | 600 |
| DDoS-SYN_Flood | 54.68% | 93.50% | 69.00% | 600 |
| DDoS-SlowLoris | 88.83% | 91.50% | 90.15% | 600 |
| DDoS-SynonymousIP_Flood | 66.37% | 73.67% | 69.83% | 600 |
| DDoS-TCP_Flood | 69.48% | 17.83% | 28.38% | 600 |
| DDoS-UDP_Flood | 58.89% | 93.83% | 72.37% | 600 |
| DDoS-UDP_Fragmentation | 99.49% | 98.33% | 98.91% | 600 |
| DNS_Spoofing | 48.82% | 45.00% | 46.83% | 600 |
| DictionaryBruteForce | 34.61% | 42.63% | 38.20% | 319 |
| DoS-HTTP_Flood | 89.13% | 75.17% | 81.56% | 600 |
| DoS-SYN_Flood | 73.94% | 17.50% | 28.30% | 600 |
| DoS-TCP_Flood | 52.83% | 91.67% | 67.03% | 600 |
| DoS-UDP_Flood | 85.12% | 34.33% | 48.93% | 600 |
| MITM-ArpSpoofing | 69.20% | 62.17% | 65.50% | 600 |
| Mirai-greeth_flood | 93.13% | 61.00% | 73.72% | 600 |
| Mirai-greip_flood | 70.93% | 94.33% | 80.97% | 600 |
| Mirai-udpplain | 99.83% | 99.67% | 99.75% | 600 |
| Recon-HostDiscovery | 42.66% | 81.33% | 55.96% | 600 |
| Recon-OSScan | 33.75% | 40.50% | 36.82% | 600 |
| Recon-PingSweep | 37.50% | 11.32% | 17.39% | 53 |
| Recon-PortScan | 40.44% | 27.83% | 32.97% | 600 |
| SqlInjection | 38.58% | 33.11% | 35.64% | 148 |
| Uploading_Attack | 0.00% | 0.00% | 0.00% | 33 |
| VulnerabilityScan | 90.17% | 94.83% | 92.45% | 600 |
| XSS | 0.00% | 0.00% | 0.00% | 103 |

![PYTORCH_MLP normalized confusion matrix](../figures/eval_cm_PYTORCH_MLP_multiclass.png)

![PYTORCH_MLP per-class precision, recall and F1](../figures/eval_f1_per_class_PYTORCH_MLP_multiclass.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_PYTORCH_MLP_multiclass.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_PYTORCH_MLP_multiclass.csv), [Per-class metrics CSV](../metrics/class_metrics_PYTORCH_MLP_multiclass.csv)


### LIGHTGBM

Test samples: **16598**

| Class | Precision | Recall | F1 score | Support |
|---|---:|---:|---:|---:|
| Backdoor_Malware | 0.00% | 0.00% | 0.00% | 89 |
| BenignTraffic | 0.00% | 0.00% | 0.00% | 600 |
| BrowserHijacking | 0.00% | 0.00% | 0.00% | 134 |
| CommandInjection | 0.00% | 0.00% | 0.00% | 119 |
| DDoS-ACK_Fragmentation | 66.67% | 0.33% | 0.66% | 600 |
| DDoS-HTTP_Flood | 0.00% | 0.00% | 0.00% | 600 |
| DDoS-ICMP_Flood | 75.37% | 84.67% | 79.75% | 600 |
| DDoS-ICMP_Fragmentation | 99.59% | 81.00% | 89.34% | 600 |
| DDoS-PSHACK_Flood | 8.57% | 10.67% | 9.50% | 600 |
| DDoS-RSTFINFlood | 0.00% | 0.00% | 0.00% | 600 |
| DDoS-SYN_Flood | 0.00% | 0.00% | 0.00% | 600 |
| DDoS-SlowLoris | 0.00% | 0.00% | 0.00% | 600 |
| DDoS-SynonymousIP_Flood | 0.00% | 0.00% | 0.00% | 600 |
| DDoS-TCP_Flood | 29.67% | 9.00% | 13.81% | 600 |
| DDoS-UDP_Flood | 36.16% | 92.33% | 51.97% | 600 |
| DDoS-UDP_Fragmentation | 30.45% | 90.33% | 45.55% | 600 |
| DNS_Spoofing | 33.33% | 0.17% | 0.33% | 600 |
| DictionaryBruteForce | 0.00% | 0.00% | 0.00% | 319 |
| DoS-HTTP_Flood | 5.43% | 92.17% | 10.26% | 600 |
| DoS-SYN_Flood | 50.00% | 0.17% | 0.33% | 600 |
| DoS-TCP_Flood | 0.00% | 0.00% | 0.00% | 600 |
| DoS-UDP_Flood | 57.14% | 1.33% | 2.61% | 600 |
| MITM-ArpSpoofing | 12.00% | 1.00% | 1.85% | 600 |
| Mirai-greeth_flood | 0.00% | 0.00% | 0.00% | 600 |
| Mirai-greip_flood | 0.00% | 0.00% | 0.00% | 600 |
| Mirai-udpplain | 83.38% | 53.50% | 65.18% | 600 |
| Recon-HostDiscovery | 1.31% | 0.33% | 0.53% | 600 |
| Recon-OSScan | 0.00% | 0.00% | 0.00% | 600 |
| Recon-PingSweep | 0.00% | 0.00% | 0.00% | 53 |
| Recon-PortScan | 0.00% | 0.00% | 0.00% | 600 |
| SqlInjection | 0.00% | 0.00% | 0.00% | 148 |
| Uploading_Attack | 0.00% | 0.00% | 0.00% | 33 |
| VulnerabilityScan | 0.00% | 0.00% | 0.00% | 600 |
| XSS | 0.00% | 0.00% | 0.00% | 103 |

![LIGHTGBM normalized confusion matrix](../figures/eval_cm_LIGHTGBM_multiclass.png)

![LIGHTGBM per-class precision, recall and F1](../figures/eval_f1_per_class_LIGHTGBM_multiclass.png)

Data: [Raw confusion matrix CSV](../metrics/confusion_matrix_LIGHTGBM_multiclass.csv), [Normalized confusion matrix CSV](../metrics/confusion_matrix_normalized_LIGHTGBM_multiclass.csv), [Per-class metrics CSV](../metrics/class_metrics_LIGHTGBM_multiclass.csv)

## Dataset visuals

### 34-class distribution

![34-class distribution](../figures/eda_class_distribution_34.png)

### Macro-category distribution

![Macro-category distribution](../figures/eda_macro_categories.png)

### Feature correlation

![Feature correlation](../figures/eda_feature_correlation.png)

### Protocol distribution

![Protocol distribution](../figures/eda_protocol_distribution.png)

## Raspberry Pi edge benchmark

These figures describe the machine used to run the benchmark, not necessarily a Raspberry Pi.

[Benchmark results CSV](../metrics/raspberry_pi_edge_benchmark.csv)

### Accuracy and inference latency

![Accuracy and inference latency](../figures/eval_rpi_latency_vs_accuracy.png)

### Resource footprint

![Resource footprint](../figures/eval_rpi_resource_footprint.png)

### Feature importance

![Feature importance](../figures/eval_rpi_feature_importance_iat.png)
## Dataset and interpretation notes

- The test scores apply to the cached stratified sample and should not be interpreted as full-dataset or live-network performance.
- Macro averages weight each class equally; weighted averages account for class support.
- A high accuracy with a lower macro F1 can indicate weaker performance on underrepresented classes.
- Edge benchmark latency must be measured on the actual target Raspberry Pi before deployment.
