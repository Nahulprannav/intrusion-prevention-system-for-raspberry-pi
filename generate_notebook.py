import json
import os

notebook = {
    'cells': [],
    'metadata': {
        'language_info': {
            'name': 'python',
            'version': '3.12'
        },
        'orig_nbformat': 4
    },
    'nbformat': 4,
    'nbformat_minor': 2
}

def add_md(text):
    notebook['cells'].append({
        'cell_type': 'markdown',
        'metadata': {},
        'source': [line + '\n' for line in text.split('\n')]
    })

def add_code(text):
    notebook['cells'].append({
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [line + '\n' for line in text.split('\n')]
    })

# CELL 1: Header
add_md('''# Raspberry Pi Edge Intrusion Prevention System (IPS) - CICIoT2023
### Tabular Model Evaluation, Edge Benchmarking & IPS Simulation

---
### Key Objectives & System Architecture:
1. **Edge Hardware Constraint**: Tailored for resource-constrained IoT gateways (e.g., **Raspberry Pi 3B+ / 4 / 5**, ARM Cortex-A53 quad-core, 1GB RAM).
2. **Two-Phase Architecture**:
   - **Phase 1**: Circular ring-buffer memory management (preventing RAM exhaustion) & feature extraction prioritizing **Inter-Arrival Time (IAT)**.
   - **Phase 2**: Low-latency threat classification, to be measured on target hardware.
3. **IPS Demonstration**:
   - Generates proposed Linux firewall rules for inspection; the current demo does not apply rules to the host.
4. **Tabular Model Comparison**:
   - Evaluates tree ensembles, an FT-Transformer-style model trained from scratch, and an optional pretrained TabPFN comparison on a shared 1,000-row subset.
''')

# CELL 2: Step 1 Setup
add_md('''## Step 1: Environment Setup & Dependencies
''')

add_code('''import os
import sys
import time
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import Image, display

# Verify imports
import torch
import xgboost as xgb
import lightgbm as lgb
from src.data_loader import prepare_or_load_data, transform_targets
from src.config import FEATURE_COLUMNS, LABEL_COLUMN

print(f"PyTorch: {torch.__version__} | XGBoost: {xgb.__version__} | LightGBM: {lgb.__version__}")
''')

# CELL 3: Step 2 Load Data
add_md('''## Step 2: Load Stratified Parquet Dataset
We load our balanced, stratified samples (69,611 training records, 16,598 test records) preserving rare attack categories.
''')

add_code('''train_df, val_df, test_df = prepare_or_load_data()
print(f"Train Shape: {train_df.shape} | Test Shape: {test_df.shape}")
''')

# CELL 4: Step 3 Edge Benchmark
add_md('''## Step 3: Raspberry Pi Edge Benchmark (Accuracy vs Latency vs Size)
We benchmark an FT-Transformer-style model trained from scratch, stacking and voting ensembles, and compact tree models. Latency measured on this machine is not Raspberry Pi latency.
''')

add_code('''# Run the benchmark engine
!python benchmark_rpi_edge.py
''')

# CELL 5: Step 4 Visual Results
add_md('''## Step 4: Edge Visual Results & Pareto Frontier Gallery
''')

add_code('''print("=== 1. Pareto Frontier: Accuracy vs Inference Latency ===")
display(Image(filename="results/figures/eval_rpi_latency_vs_accuracy.png", width=750))

print("\\n=== 2. Edge Hardware Resource Footprint (Model Size & Latency) ===")
display(Image(filename="results/figures/eval_rpi_resource_footprint.png", width=850))

print("\\n=== 3. Key Feature Importance Ranking (Highlighting IAT) ===")
display(Image(filename="results/figures/eval_rpi_feature_importance_iat.png", width=750))
''')

# CELL 6: Step 5 IPS Demo
add_md('''## Step 5: IPS Demonstration
Simulate incoming network packet flows and inspect proposed firewall-rule strings. This demo does not apply rules to the host.
''')

add_code('''from src.raspberry_pi_ips import RaspberryPiIntrusionPreventionSystem

ips = RaspberryPiIntrusionPreventionSystem(model_task="category")

# Simulate 5 incoming test flows
mock_flows = test_df.sample(n=5, random_state=101)
test_ips = ["192.168.1.110", "10.0.0.52", "172.16.10.4", "45.33.32.1", "192.168.1.1"]
test_ports = [80, 22, 443, 23, 8080]

print("="*85)
print("              RASPBERRY PI IPS RULE-GENERATION DEMONSTRATION")
print("="*85)
for idx, (_, row) in enumerate(mock_flows.iterrows()):
    src_ip = test_ips[idx]
    dport = test_ports[idx]
    verdict = ips.inspect_and_mitigate(row.to_dict(), source_ip=src_ip, dest_port=dport)
    print(f"[{idx+1}] Inbound {src_ip}:{dport} -> Verdict: {verdict['verdict']} ({verdict['confidence']}) | Action: {verdict['ips_action']}")
    print(f"    Firewall Rule: {verdict['firewall_rule']}")
    print(f"    Mitigation:    {verdict['mitigation_summary']}\\n")

ips.print_telemetry()
''')

project_root = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(project_root, 'CICIoT2023_Intrusion_Detection_Pipeline.ipynb')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)

print(f"Updated {out_path} successfully!")
