import os
import gc
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from src.config import (
    TRAIN_CSV, VAL_CSV, TEST_CSV,
    SAMPLED_TRAIN_FILE, SAMPLED_VAL_FILE, SAMPLED_TEST_FILE,
    FEATURE_COLUMNS, LABEL_COLUMN, ALL_CLASSES_34, CATEGORY_MAPPING_8,
    SAMPLE_CONFIG, get_binary_label
)

def clean_numerical_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans infinite and NaN values in numeric features and casts to float32 for RAM efficiency.
    """
    features = [col for col in df.columns if col in FEATURE_COLUMNS]
    for col in features:
        # Replace positive and negative inf with NaN
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        # Impute NaN with median (or 0.0)
        if df[col].isnull().any():
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val if not np.isnan(median_val) else 0.0)
        # Cast to float32
        df[col] = df[col].astype(np.float32)
    return df

def sample_stratified_from_csv(csv_path: str, max_per_class: int = 2500, chunksize: int = 250000, random_state: int = 42) -> pd.DataFrame:
    """
    Efficiently streams through huge CSV in chunks and performs stratified sampling.
    Preserves 100% of samples for rare attack types and bounds majority attacks.
    """
    print(f"\n[Data Loader] Streaming & stratified sampling from: {csv_path}")
    print(f"Target max samples per class: {max_per_class:,} (chunk size: {chunksize:,})")

    collected = {cls_name: [] for cls_name in ALL_CLASSES_34}
    counts = {cls_name: 0 for cls_name in ALL_CLASSES_34}
    total_processed = 0

    chunk_idx = 0
    for chunk in pd.read_csv(csv_path, chunksize=chunksize):
        chunk_idx += 1
        total_processed += len(chunk)
        
        # Check counts per class in this chunk
        for label, group in chunk.groupby(LABEL_COLUMN):
            if label not in counts:
                counts[label] = 0
                collected[label] = []

            needed = max_per_class - counts[label]
            if needed > 0:
                sampled = group.sample(n=min(len(group), needed), random_state=random_state + chunk_idx)
                collected[label].append(sampled)
                counts[label] += len(sampled)

        print(f"  Chunk {chunk_idx}: Processed {total_processed:,} rows | Classes with target reached: {sum(c >= max_per_class for c in counts.values())}/{len(counts)}", end="\r")

    print(f"\n[Data Loader] Finished streaming {total_processed:,} rows.")

    dfs = []
    for label, parts in collected.items():
        if parts:
            dfs.append(pd.concat(parts, axis=0))

    if not dfs:
        raise ValueError(f"No records collected from {csv_path}!")

    sampled_df = pd.concat(dfs, axis=0)
    sampled_df = sampled_df.sample(frac=1.0, random_state=random_state).reset_index(drop=True)
    sampled_df = clean_numerical_features(sampled_df)
    
    print(f"[Data Loader] Sampled dataset shape: {sampled_df.shape} | Classes: {sampled_df[LABEL_COLUMN].nunique()}")
    del collected, dfs
    gc.collect()
    return sampled_df

def prepare_or_load_data(force_recompute: bool = False, max_train_per_class: int = 2500, max_test_per_class: int = 600):
    """
    Loads saved stratified parquet datasets if available, otherwise samples from raw CSVs.
    """
    os.makedirs(os.path.dirname(SAMPLED_TRAIN_FILE), exist_ok=True)
    
    if (not force_recompute and
        os.path.exists(SAMPLED_TRAIN_FILE) and
        os.path.exists(SAMPLED_VAL_FILE) and
        os.path.exists(SAMPLED_TEST_FILE)):
        print("[Data Loader] Loading existing stratified datasets from Parquet cache...")
        train_df = pd.read_parquet(SAMPLED_TRAIN_FILE)
        val_df = pd.read_parquet(SAMPLED_VAL_FILE)
        test_df = pd.read_parquet(SAMPLED_TEST_FILE)
        print(f"  Train: {train_df.shape}, Val: {val_df.shape}, Test: {test_df.shape}")
        return train_df, val_df, test_df

    print("[Data Loader] Cache not found or recompute requested. Generating stratified samples...")
    train_df = sample_stratified_from_csv(TRAIN_CSV, max_per_class=max_train_per_class, chunksize=SAMPLE_CONFIG['chunksize'])
    val_df = sample_stratified_from_csv(VAL_CSV, max_per_class=max_test_per_class, chunksize=SAMPLE_CONFIG['chunksize'])
    test_df = sample_stratified_from_csv(TEST_CSV, max_per_class=max_test_per_class, chunksize=SAMPLE_CONFIG['chunksize'])

    print("[Data Loader] Caching sampled datasets to fast Parquet format...")
    train_df.to_parquet(SAMPLED_TRAIN_FILE, index=False)
    val_df.to_parquet(SAMPLED_VAL_FILE, index=False)
    test_df.to_parquet(SAMPLED_TEST_FILE, index=False)
    print(f"  Saved to:\n    - {SAMPLED_TRAIN_FILE}\n    - {SAMPLED_VAL_FILE}\n    - {SAMPLED_TEST_FILE}")

    return train_df, val_df, test_df

def transform_targets(y_raw: pd.Series, classification_type: str = 'category'):
    """
    Maps target labels according to classification mode:
    - 'category': 8 Macro categories (DDoS, DoS, Mirai, Recon, Spoofing, Web_Attack, Brute_Force, Benign)
    - 'multiclass': 34 Original fine-grained classes
    - 'binary': Attack vs Benign
    """
    if classification_type == 'category':
        y_mapped = y_raw.map(lambda x: CATEGORY_MAPPING_8.get(x, 'Other'))
    elif classification_type == 'binary':
        y_mapped = y_raw.map(get_binary_label)
    elif classification_type == 'multiclass':
        y_mapped = y_raw.copy()
    else:
        raise ValueError(f"Unknown classification_type: {classification_type}. Choose 'category', 'multiclass', or 'binary'.")
    return y_mapped
