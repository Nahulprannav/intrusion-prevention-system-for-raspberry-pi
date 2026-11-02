"""
Master End-to-End Orchestrator for CICIoT2023 Intrusion Detection System.
Executes:
1. Data streaming & stratified sampling
2. Exploratory Data Analysis & visual generation
3. Multi-model tournament training & hyperparameter fitting
4. Comprehensive test evaluation, confusion matrices, and leaderboard generation
5. Real-time sample inference simulation
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import prepare_or_load_data
from src.eda import run_eda
from src.train import train_pipeline
from src.inference import simulate_realtime_detection

def main():
    print("#"*78)
    print("#   END-TO-END CICIOT2023 CYBERSECURITY INTRUSION DETECTION PIPELINE   #")
    print("#"*78)

    # Step 1: Data Preparation & Stratified Sampling
    print("\n>>> STEP 1: PREPARING STRATIFIED DATASET...")
    train_df, val_df, test_df = prepare_or_load_data(force_recompute=False)

    # Step 2: Exploratory Data Analysis
    print("\n>>> STEP 2: RUNNING EXPLORATORY DATA ANALYSIS...")
    run_eda(train_df, output_prefix="eda")

    # Step 3: Model Tournament Training & Evaluation (8 Macro Categories)
    print("\n>>> STEP 3: TRAINING 7 ML/DL MODELS ON MACRO CATEGORIES (8-CLASS)...")
    train_pipeline(
        task="category",
        selected_models=["LIGHTGBM", "XGBOOST", "CATBOOST", "RANDOM_FOREST", "EXTRA_TREES", "HIST_GRADIENT_BOOSTING", "PYTORCH_MLP"],
        force_resample=False
    )

    # Step 4: Real-Time Inference Simulation
    print("\n>>> STEP 4: REAL-TIME INFERENCE SIMULATION...")
    simulate_realtime_detection(num_samples=10, task="category")

    print("\n" + "#"*78)
    print("#                      PIPELINE RUN COMPLETE!                        #")
    print("#  Check 'results/figures/' for all generated high-res plots          #")
    print("#  Check 'results/metrics/' for leaderboard and metrics               #")
    print("#  Check 'saved_models/' for trained model artifacts                  #")
    print("#"*78)

if __name__ == "__main__":
    main()
