"""
Exploratory Data Analysis (EDA) Runner for CICIoT2023 Dataset.
Generates comprehensive distribution plots, correlation matrices, protocol usage, and class balance summaries.
"""
import os
import sys

# Ensure project root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import prepare_or_load_data
from src.eda import run_eda

def main():
    print("="*75)
    print("             CICIOT2023 EXPLORATORY DATA ANALYSIS")
    print("="*75)
    
    # Load stratified dataset
    train_df, _, _ = prepare_or_load_data()
    
    # Run EDA
    run_eda(train_df, output_prefix="eda")
    print("\n[SUCCESS] EDA successfully completed! All figures saved in 'results/figures/'")

if __name__ == "__main__":
    main()
