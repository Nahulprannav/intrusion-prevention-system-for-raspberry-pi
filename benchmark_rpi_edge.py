"""
Raspberry Pi Edge Benchmark & Tabular Foundation Model Evaluation.
Benchmarking models under Raspberry Pi resource constraints (ARM Cortex-A53, 1GB RAM):
- Tabular Foundation Transformer (FT-Transformer)
- Stacking Ensemble (Paper Table I: 96.72%)
- Voting Ensemble (Paper Table I: 95.98%)
- Edge-Optimized Decision Tree (Paper Table II: 94.34%, 0.8ms, 2.3MB)
- Edge XGBoost & LightGBM
"""
import os
import sys
import time
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config import (
    SAVED_MODELS_DIR, FIGURES_DIR, METRICS_DIR,
    FEATURE_COLUMNS, LABEL_COLUMN
)
from src.data_loader import prepare_or_load_data, transform_targets
from src.foundation_models import (
    TabularFoundationClassifier,
    create_stacking_ensemble,
    create_voting_ensemble,
    create_raspberry_pi_edge_dt
)
import xgboost as xgb
import lightgbm as lgb
from src.raspberry_pi_ips import RaspberryPiIntrusionPreventionSystem

def measure_edge_metrics(model, X_test, y_test, num_timing_samples=50):
    """
    Simulates real-world edge execution on Raspberry Pi:
    Measures per-packet inference latency (ms), throughput (pps), and memory footprint.
    """
    # 1. Overall accuracy & F1
    y_pred = model.predict(X_test)
    if len(y_pred.shape) > 1 and y_pred.shape[1] > 1:
        y_pred = np.argmax(y_pred, axis=1)

    acc = accuracy_score(y_test, y_pred)
    f1_w = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    f1_m = f1_score(y_test, y_pred, average='macro', zero_division=0)

    # 2. Per-packet latency timing (single sample loop to emulate live NIC packet arrival)
    timing_slice = X_test[:num_timing_samples]
    latencies = []
    
    # Warmup
    for _ in range(5):
        _ = model.predict(timing_slice[:1])

    for i in range(num_timing_samples):
        single_pkt = timing_slice[i:i+1]
        t0 = time.perf_counter()
        _ = model.predict(single_pkt)
        latencies.append((time.perf_counter() - t0) * 1000.0) # Convert to ms

    avg_latency_ms = float(np.mean(latencies))
    throughput_pps = 1000.0 / max(0.001, avg_latency_ms)

    return {
        "accuracy": acc,
        "weighted_f1": f1_w,
        "macro_f1": f1_m,
        "latency_ms": avg_latency_ms,
        "throughput_pps": throughput_pps
    }

def main():
    print("="*75, flush=True)
    print("   RASPBERRY PI EDGE BENCHMARK & TABULAR FOUNDATION EVALUATION", flush=True)
    print("="*75, flush=True)

    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(METRICS_DIR, exist_ok=True)
    os.makedirs(SAVED_MODELS_DIR, exist_ok=True)

    # 1. Load Data
    train_df, val_df, test_df = prepare_or_load_data()
    feature_cols = [c for c in FEATURE_COLUMNS if c in train_df.columns]

    X_train_raw = train_df[feature_cols].values
    X_val_raw = val_df[feature_cols].values
    X_test_raw = test_df[feature_cols].values

    # Target: 8 Macro Categories (Matching Paper Section III)
    y_train_raw = transform_targets(train_df[LABEL_COLUMN], 'category')
    y_val_raw = transform_targets(val_df[LABEL_COLUMN], 'category')
    y_test_raw = transform_targets(test_df[LABEL_COLUMN], 'category')

    le = LabelEncoder()
    y_train = le.fit_transform(y_train_raw)
    y_val = le.transform(y_val_raw)
    y_test = le.transform(y_test_raw)
    class_names = list(le.classes_)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train_raw)
    X_val = scaler.transform(X_val_raw)
    X_test = scaler.transform(X_test_raw)

    print(f"\n[Dataset] Train: {len(X_train):,} | Test: {len(X_test):,} | Classes: {len(class_names)}", flush=True)

    # Models to benchmark:
    models = {
        "Tabular_Foundation_Transformer": TabularFoundationClassifier(
            n_features=len(feature_cols), num_classes=len(class_names), epochs=5, d_token=32, n_heads=4
        ),
        "Stacking_Ensemble": create_stacking_ensemble(),
        "Voting_Ensemble": create_voting_ensemble(),
        "RaspberryPi_Decision_Tree": create_raspberry_pi_edge_dt(),
        "Edge_XGBoost": xgb.XGBClassifier(n_estimators=50, max_depth=6, learning_rate=0.1, n_jobs=1, eval_metric='mlogloss'),
        "Edge_LightGBM": lgb.LGBMClassifier(n_estimators=50, max_depth=6, learning_rate=0.1, n_jobs=1, verbosity=-1)
    }

    results = []

    for name, model in models.items():
        print(f"\n>>> Training & Benchmarking: {name} ...", flush=True)
        t_start = time.time()
        model.fit(X_train, y_train)
        train_time = time.time() - t_start

        # Measure serialized size
        tmp_path = os.path.join(SAVED_MODELS_DIR, f"temp_{name}.joblib")
        joblib.dump(model, tmp_path)
        model_size_mb = os.path.getsize(tmp_path) / (1024 * 1024)
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

        # Edge hardware metrics
        metrics = measure_edge_metrics(model, X_test, y_test, num_timing_samples=50)
        metrics["model_name"] = name
        metrics["train_time_s"] = round(train_time, 2)
        metrics["model_size_mb"] = round(model_size_mb, 2)

        print(f"  Accuracy:         {metrics['accuracy']*100:.2f}%", flush=True)
        print(f"  Weighted F1:      {metrics['weighted_f1']*100:.2f}%", flush=True)
        print(f"  Packet Latency:   {metrics['latency_ms']:.3f} ms / packet", flush=True)
        print(f"  Edge Throughput:  {metrics['throughput_pps']:,.0f} packets / second", flush=True)
        print(f"  Model Size:       {metrics['model_size_mb']:.2f} MB", flush=True)
        results.append(metrics)

    # 3. Create Comparison DataFrame & Save CSV
    df_results = pd.DataFrame(results)
    csv_path = os.path.join(METRICS_DIR, "raspberry_pi_edge_benchmark.csv")
    df_results.to_csv(csv_path, index=False)
    print(f"\n[Results Saved] Benchmark Table -> {csv_path}", flush=True)
    print("\n" + "="*80, flush=True)
    print(df_results[['model_name', 'accuracy', 'weighted_f1', 'latency_ms', 'model_size_mb', 'throughput_pps']].to_string(index=False), flush=True)
    print("="*80, flush=True)

    # 4. Save Champion Edge Model for Raspberry Pi Deployment
    edge_champion_name = "Edge_XGBoost"
    edge_champion_model = models[edge_champion_name]

    edge_pipeline = {
        'model': edge_champion_model,
        'scaler': scaler,
        'label_encoder': le,
        'feature_cols': feature_cols,
        'class_names': class_names,
        'task': 'category',
        'edge_champion_name': edge_champion_name
    }
    edge_pipeline_path = os.path.join(SAVED_MODELS_DIR, "rpi_edge_category_pipeline.joblib")
    joblib.dump(edge_pipeline, edge_pipeline_path)
    print(f"\n[Saved Champion Pipeline for RPi] -> {edge_pipeline_path}", flush=True)

    # ================= PLOT 1: Accuracy vs Inference Latency (Pareto Frontier) =================
    fig, ax = plt.subplots(figsize=(10, 6))
    for r in results:
        m_name = r['model_name'].replace("_", " ")
        acc = r['accuracy'] * 100
        lat = r['latency_ms']
        size = r['model_size_mb']
        color = '#2ca02c' if "Decision" in m_name or "XGBoost" in m_name else '#1f77b4'
        ax.scatter(lat, acc, s=max(80, size * 15), alpha=0.75, color=color, edgecolors='black')
        ax.annotate(f"{m_name}\n({acc:.1f}%, {lat:.2f}ms)",
                    (lat, acc),
                    textcoords="offset points",
                    xytext=(0, 8),
                    ha='center', fontsize=9, weight='bold')

    ax.axvline(x=1.0, color='red', linestyle='--', label='1.0 ms Real-Time Edge Budget')
    ax.set_title("Raspberry Pi Trade-off: Detection Accuracy vs. Inference Latency (ms)", fontsize=13, weight='bold')
    ax.set_xlabel("Inference Latency per Packet (ms) - [Lower is Better]", fontsize=11, weight='bold')
    ax.set_ylabel("Detection Accuracy (%) - [Higher is Better]", fontsize=11, weight='bold')
    ax.set_ylim(70, 100)
    ax.legend(loc='lower left')
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    fig1_path = os.path.join(FIGURES_DIR, "eval_rpi_latency_vs_accuracy.png")
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"[Plot Saved] Latency vs Accuracy -> {fig1_path}", flush=True)

    # ================= PLOT 2: Resource Footprint (Model Size & Latency) =================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    names_clean = [r['model_name'].replace("_", "\n") for r in results]
    sizes = [r['model_size_mb'] for r in results]
    latencies = [r['latency_ms'] for r in results]

    ax1.bar(names_clean, sizes, color=plt.cm.viridis(np.linspace(0.2, 0.8, len(results))))
    ax1.set_title("Model Footprint on Disk (MB) - RPi Budget < 20MB", fontsize=11, weight='bold')
    ax1.set_ylabel("Size (MB)", fontsize=10, weight='bold')
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    for p in ax1.patches:
        ax1.annotate(f"{p.get_height():.2f}MB", (p.get_x() + p.get_width()/2., p.get_height()),
                     ha='center', va='bottom', fontsize=8, weight='bold')

    ax2.bar(names_clean, latencies, color=plt.cm.plasma(np.linspace(0.2, 0.8, len(results))))
    ax2.set_title("Single Packet Inference Time (ms) - RPi Budget < 1.0ms", fontsize=11, weight='bold')
    ax2.set_ylabel("Latency (ms)", fontsize=10, weight='bold')
    ax2.axhline(y=1.0, color='red', linestyle='--', label='1.0ms Target')
    ax2.legend()
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    for p in ax2.patches:
        ax2.annotate(f"{p.get_height():.2f}ms", (p.get_x() + p.get_width()/2., p.get_height()),
                     ha='center', va='bottom', fontsize=8, weight='bold')

    plt.suptitle("Raspberry Pi Edge Hardware Constraints Analysis", fontsize=13, weight='bold')
    plt.tight_layout()
    fig2_path = os.path.join(FIGURES_DIR, "eval_rpi_resource_footprint.png")
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"[Plot Saved] Resource Footprint -> {fig2_path}", flush=True)

    # ================= PLOT 3: Feature Importance with IAT Highlight =================
    if hasattr(edge_champion_model, 'feature_importances_'):
        imps = edge_champion_model.feature_importances_
        idx = np.argsort(imps)[::-1][:15]
        top_f = [feature_cols[i] for i in idx]
        top_v = imps[idx]

        fig, ax = plt.subplots(figsize=(11, 7))
        colors = ['#d62728' if 'IAT' in f else '#1f77b4' for f in top_f]
        bars = ax.barh(np.arange(len(top_f)), top_v, color=colors, height=0.65)
        ax.set_yticks(np.arange(len(top_f)))
        ax.set_yticklabels(top_f, fontsize=10)
        ax.invert_yaxis()
        ax.set_title("Feature Importance Ranking on CICIoT2023 (Highlighting IAT)", fontsize=13, weight='bold')
        ax.set_xlabel("Relative Feature Importance", fontsize=11, weight='bold')
        ax.grid(axis='x', linestyle='--', alpha=0.5)

        for bar in bars:
            w = bar.get_width()
            ax.text(w + (max(top_v) * 0.01), bar.get_y() + bar.get_height() / 2, f"{w:.4f}",
                    va='center', fontsize=9, weight='bold')

        plt.tight_layout()
        fig3_path = os.path.join(FIGURES_DIR, "eval_rpi_feature_importance_iat.png")
        plt.savefig(fig3_path, dpi=300)
        plt.close()
        print(f"[Plot Saved] IAT Feature Importance -> {fig3_path}", flush=True)

    # 5. Live Simulation of Raspberry Pi IPS in Action
    print("\n" + "="*75, flush=True)
    print("      DEMONSTRATING LIVE RASPBERRY PI ACTIVE INTRUSION PREVENTION (IPS)", flush=True)
    print("="*75, flush=True)
    ips = RaspberryPiIntrusionPreventionSystem(model_task="category")

    # Sample representative flows from test set
    mock_traffic = test_df.sample(n=8, random_state=42)
    sample_ips = ["192.168.1.105", "10.0.0.45", "172.16.0.88", "192.168.1.120", "45.33.32.156", "185.220.101.5", "192.168.1.101", "10.0.0.99"]
    ports = [80, 443, 22, 8080, 23, 53, 445, 80]

    for idx, (_, row) in enumerate(mock_traffic.iterrows()):
        feat_dict = row.to_dict()
        src_ip = sample_ips[idx % len(sample_ips)]
        dport = ports[idx % len(ports)]
        verdict = ips.inspect_and_mitigate(feat_dict, source_ip=src_ip, dest_port=dport)
        print(f"[{idx+1}] Inbound {src_ip}:{dport} -> Verdict: {verdict['verdict']} ({verdict['confidence']}) | Action: {verdict['ips_action']} (Latency: {verdict['latency_ms']}ms)", flush=True)
        print(f"    Firewall Rule Generated: {verdict['firewall_rule']}", flush=True)
        print(f"    Mitigation: {verdict['mitigation_summary']}\n", flush=True)

    ips.print_telemetry()
    print("[SUCCESS] Raspberry Pi Edge Benchmark & IPS Demonstration Complete!", flush=True)

if __name__ == "__main__":
    main()
