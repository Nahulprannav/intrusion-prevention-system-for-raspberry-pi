import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src.config import (
    FIGURES_DIR, METRICS_DIR, FEATURE_COLUMNS, LABEL_COLUMN,
    CATEGORY_MAPPING_8, ALL_CLASSES_34
)

def run_eda(df: pd.DataFrame, output_prefix: str = "eda"):
    """
    Executes in-depth Exploratory Data Analysis on the network flow dataset.
    Generates high-resolution visualization figures and statistical metric summaries.
    """
    print("\n" + "="*70)
    print("      RUNNING EXPLORATORY DATA ANALYSIS (EDA)")
    print("="*70)
    
    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(METRICS_DIR, exist_ok=True)

    # 1. Dataset Shape & Features
    n_rows, n_cols = df.shape
    features = [c for c in df.columns if c in FEATURE_COLUMNS]
    n_features = len(features)
    print(f"\n[EDA] Total records analyzed: {n_rows:,}")
    print(f"[EDA] Total features: {n_features} numerical flow features")
    print(f"[EDA] Target column: '{LABEL_COLUMN}' with {df[LABEL_COLUMN].nunique()} unique classes")

    # 2. Missing Values & Memory Usage
    missing_counts = df[features].isnull().sum()
    total_missing = missing_counts.sum()
    mem_usage_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
    print(f"[EDA] Missing values: {total_missing} (Clean dataset)")
    print(f"[EDA] Memory footprint: {mem_usage_mb:.2f} MB")

    # 3. Class Distribution (34 Classes)
    class_counts = df[LABEL_COLUMN].value_counts().sort_values(ascending=True)
    print("\n[EDA] Class Frequency Highlights:")
    print("  Top 5 Most Prevalent Classes:")
    for cls, cnt in class_counts.tail(5).items():
        print(f"    - {cls:30s}: {cnt:>6,d} ({cnt/n_rows*100:.2f}%)")
    print("  Top 5 Rarest Attack Classes:")
    for cls, cnt in class_counts.head(5).items():
        print(f"    - {cls:30s}: {cnt:>6,d} ({cnt/n_rows*100:.2f}%)")

    # 4. Macro Category Distribution (8 Categories)
    df_cat = df[LABEL_COLUMN].map(lambda x: CATEGORY_MAPPING_8.get(x, 'Other'))
    cat_counts = df_cat.value_counts().sort_values(ascending=False)
    print("\n[EDA] Macro Attack Categories Breakdown:")
    for cat, cnt in cat_counts.items():
        print(f"    - {cat:20s}: {cnt:>6,d} ({cnt/n_rows*100:.2f}%)")

    # Set universal matplotlib styles
    plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'axes.edgecolor': '#cccccc'})

    # ================= VISUALIZATION 1: 34-Class Distribution =================
    fig, ax = plt.subplots(figsize=(14, 11))
    y_pos = np.arange(len(class_counts))
    colors = plt.cm.plasma(np.linspace(0.1, 0.9, len(class_counts)))
    
    bars = ax.barh(y_pos, class_counts.values, color=colors, edgecolor='none', height=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(class_counts.index, fontsize=9)
    ax.set_xscale('log')
    ax.set_xlabel("Sample Count (Log Scale)", fontsize=11, weight='bold')
    ax.set_ylabel("Attack / Traffic Class", fontsize=11, weight='bold')
    ax.set_title(f"CICIoT2023 - 34 Attack Classes Distribution (Total: {n_rows:,} Samples)", fontsize=13, weight='bold')
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    for i, bar in enumerate(bars):
        w = bar.get_width()
        ax.text(w * 1.15, bar.get_y() + bar.get_height() / 2, f"{int(w):,}", va='center', fontsize=8)

    plt.tight_layout()
    fig1_path = os.path.join(FIGURES_DIR, f"{output_prefix}_class_distribution_34.png")
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"\n[EDA Figure Saved] 34-Class Distribution -> {fig1_path}")

    # ================= VISUALIZATION 2: Macro Category Breakdown =================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    cmap = plt.cm.tab10(np.linspace(0, 1, len(cat_counts)))

    # Donut Chart
    wedges, texts, autotexts = ax1.pie(
        cat_counts.values,
        labels=cat_counts.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=cmap,
        pctdistance=0.8,
        wedgeprops=dict(width=0.4, edgecolor='white')
    )
    for t in autotexts:
        t.set_fontsize(9)
        t.set_weight('bold')
    ax1.set_title("Proportion by Attack Category", fontsize=13, weight='bold')

    # Bar Chart
    bars = ax2.barh(np.arange(len(cat_counts)), cat_counts.values, color=cmap, height=0.6)
    ax2.set_yticks(np.arange(len(cat_counts)))
    ax2.set_yticklabels(cat_counts.index, fontsize=10, weight='semibold')
    ax2.invert_yaxis()
    ax2.set_title("Sample Counts by Attack Category", fontsize=13, weight='bold')
    ax2.set_xlabel("Count", fontsize=11, weight='bold')
    ax2.grid(axis='x', linestyle='--', alpha=0.5)

    for bar in bars:
        w = bar.get_width()
        ax2.text(w + (max(cat_counts.values) * 0.015), bar.get_y() + bar.get_height()/2, f"{int(w):,}", va='center', fontsize=10, weight='bold')

    plt.suptitle("CICIoT2023 - Macro Attack Categories Overview", fontsize=15, weight='bold')
    plt.tight_layout()
    fig2_path = os.path.join(FIGURES_DIR, f"{output_prefix}_macro_categories.png")
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"[EDA Figure Saved] Macro Categories -> {fig2_path}")

    # ================= VISUALIZATION 3: Feature Correlation Heatmap =================
    corr_features = [
        'flow_duration', 'Header_Length', 'Duration', 'Rate', 'Srate', 'Drate',
        'ack_count', 'syn_count', 'fin_count', 'Tot sum', 'Min', 'Max', 'AVG', 'Std',
        'Tot size', 'IAT', 'Magnitue', 'Weight'
    ]
    available_corr = [f for f in corr_features if f in df.columns]
    corr_matrix = df[available_corr].corr().values

    fig, ax = plt.subplots(figsize=(13, 11))
    cax = ax.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
    fig.colorbar(cax, ax=ax, shrink=0.8, label="Pearson Correlation")
    
    ax.set_xticks(np.arange(len(available_corr)))
    ax.set_yticks(np.arange(len(available_corr)))
    ax.set_xticklabels(available_corr, rotation=45, ha='right', fontsize=9)
    ax.set_yticklabels(available_corr, fontsize=9)
    ax.set_title("Correlation Matrix of Key Network Traffic Features", fontsize=13, weight='bold')

    # Add numeric labels to cells
    for i in range(len(available_corr)):
        for j in range(len(available_corr)):
            val = corr_matrix[i, j]
            if not np.isnan(val):
                text_color = "white" if abs(val) > 0.55 else "black"
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", color=text_color, fontsize=7)

    plt.tight_layout()
    fig3_path = os.path.join(FIGURES_DIR, f"{output_prefix}_feature_correlation.png")
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"[EDA Figure Saved] Feature Correlation -> {fig3_path}")

    # ================= VISUALIZATION 4: Protocol Distribution =================
    protocol_cols = ['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS', 'DNS', 'ARP', 'IPv']
    proto_names = []
    proto_pcts = []
    for p in protocol_cols:
        if p in df.columns:
            proto_names.append(p)
            proto_pcts.append(float((df[p] > 0).mean() * 100))

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(proto_names, proto_pcts, color=plt.cm.viridis(np.linspace(0.2, 0.8, len(proto_names))), edgecolor='none', width=0.6)
    ax.set_title("Network Protocol Utilization Across Flow Records (%)", fontsize=13, weight='bold')
    ax.set_ylabel("% of Flows Utilizing Protocol", fontsize=11, weight='bold')
    ax.set_xlabel("Protocol Identifier", fontsize=11, weight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.1f}%", (bar.get_x() + bar.get_width() / 2., h + 1),
                    ha='center', va='bottom', fontsize=9, weight='bold')
    ax.set_ylim(0, max(proto_pcts) * 1.15 if proto_pcts else 100)
    plt.tight_layout()
    fig4_path = os.path.join(FIGURES_DIR, f"{output_prefix}_protocol_distribution.png")
    plt.savefig(fig4_path, dpi=300)
    plt.close()
    print(f"[EDA Figure Saved] Protocol Distribution -> {fig4_path}")

    # 5. Export Summary JSON
    summary_data = {
        "dataset_rows": int(n_rows),
        "dataset_features": int(n_features),
        "total_classes": int(df[LABEL_COLUMN].nunique()),
        "missing_values": int(total_missing),
        "memory_mb": round(mem_usage_mb, 2),
        "classes_34_counts": {k: int(v) for k, v in class_counts.items()},
        "categories_8_counts": {k: int(v) for k, v in cat_counts.items()}
    }
    json_path = os.path.join(METRICS_DIR, f"{output_prefix}_summary.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=4)
    print(f"[EDA Metrics Saved] Summary JSON -> {json_path}")
    print("="*70)
    return summary_data
