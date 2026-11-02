"""
Real-time Network Threat Inference CLI.
Takes sample packet flow records and generates instant classification, severity rating, and threat alerts.
"""
import os
import sys
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.inference import simulate_realtime_detection

def main():
    parser = argparse.ArgumentParser(description="Live Network Packet Threat Detection Engine")
    parser.add_argument("--samples", type=int, default=10, help="Number of flow samples to analyze")
    parser.add_argument("--task", type=str, default="category", choices=["category", "multiclass", "binary"])
    args = parser.parse_args()

    simulate_realtime_detection(num_samples=args.samples, task=args.task)

if __name__ == "__main__":
    main()
