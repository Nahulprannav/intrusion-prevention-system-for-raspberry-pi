import os
import joblib
import numpy as np
import pandas as pd
from src.config import SAVED_MODELS_DIR, TEST_CSV, FEATURE_COLUMNS

class NetworkIntrusionDetector:
    """
    Production-ready real-time Network Intrusion Detection Engine.
    Loads saved model, scaler, and label encoder to inspect live network packet flows.
    """
    def __init__(self, model_task: str = "category"):
        self.pipeline_path = os.path.join(SAVED_MODELS_DIR, f"champion_{model_task}_pipeline.joblib")
        if not os.path.exists(self.pipeline_path):
            raise FileNotFoundError(f"Model artifact not found at {self.pipeline_path}. Please run train_and_evaluate.py first.")
        
        print(f"[Inference Engine] Loading champion pipeline from {self.pipeline_path}...")
        artifacts = joblib.load(self.pipeline_path)
        self.model = artifacts['model']
        self.scaler = artifacts['scaler']
        self.label_encoder = artifacts['label_encoder']
        self.feature_cols = artifacts['feature_cols']
        self.class_names = artifacts['class_names']
        self.model_name = artifacts['best_model_name']
        self.task = artifacts['task']
        print(f"[Inference Engine] Loaded {self.model_name} for task '{self.task}' (Classes: {len(self.class_names)})")

    def predict_flow(self, flow_data: pd.DataFrame) -> pd.DataFrame:
        """
        Takes a dataframe of raw flow records and outputs real-time threat predictions with confidence scores.
        """
        # Ensure all required features are present
        features_subset = [col for col in self.feature_cols if col in flow_data.columns]
        missing = set(self.feature_cols) - set(features_subset)
        if missing:
            raise ValueError(f"Missing required flow features: {missing}")

        X_raw = flow_data[self.feature_cols].copy()
        
        # Clean inf/nan
        X_raw = X_raw.replace([np.inf, -np.inf], np.nan).fillna(0.0).values
        
        # Scale features using saved scaler
        X_scaled = self.scaler.transform(X_raw)

        # Predict
        if hasattr(self.model, 'predict_proba'):
            probs = self.model.predict_proba(X_scaled)
            pred_indices = np.argmax(probs, axis=1)
            confidences = np.max(probs, axis=1) * 100
        else:
            pred_indices = self.model.predict(X_scaled)
            confidences = [100.0] * len(pred_indices)

        predicted_classes = self.label_encoder.inverse_transform(pred_indices)

        # Threat severity level mapping
        def assign_severity(cls_name: str) -> str:
            cls_upper = str(cls_name).upper()
            if "BENIGN" in cls_upper:
                return "SAFE (Benign Traffic)"
            elif "RECON" in cls_upper or "SCAN" in cls_upper or "SPOOF" in cls_upper:
                return "WARNING (Recon / Spoofing Activity)"
            elif "DOS" in cls_upper or "DDOS" in cls_upper:
                return "CRITICAL (Denial of Service Attack)"
            elif "WEB" in cls_upper or "INJECTION" in cls_upper or "MALWARE" in cls_upper or "BRUTE" in cls_upper:
                return "CRITICAL (Exploit / Malware Intrusion)"
            return "ALERT (Suspicious Activity)"

        results = []
        for i in range(len(predicted_classes)):
            p_class = predicted_classes[i]
            conf = confidences[i]
            severity = assign_severity(p_class)
            results.append({
                'Sample_ID': i + 1,
                'Predicted_Threat': p_class,
                'Confidence': f"{conf:.2f}%",
                'Severity_Level': severity
            })

        return pd.DataFrame(results)

def simulate_realtime_detection(num_samples: int = 10, task: str = "category"):
    """
    Simulates production traffic by reading random network flows from test.csv and classifying them.
    """
    detector = NetworkIntrusionDetector(model_task=task)
    print(f"\n[Simulation] Slicing {num_samples} unseen flow records from test dataset...")
    test_slice = pd.read_csv(TEST_CSV, nrows=num_samples * 5).sample(n=num_samples, random_state=123)
    
    actual_labels = test_slice['label'].values if 'label' in test_slice.columns else None
    predictions_df = detector.predict_flow(test_slice)
    
    if actual_labels is not None:
        predictions_df.insert(1, 'Actual_Raw_Label', actual_labels)

    print("\n" + "="*85)
    print("                 REAL-TIME NETWORK INTRUSION DETECTION MONITOR")
    print("="*85)
    print(predictions_df.to_string(index=False))
    print("="*85 + "\n")
    return predictions_df

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Real-Time Network Intrusion Detector")
    parser.add_argument("--samples", type=int, default=8, help="Number of test flows to inspect")
    parser.add_argument("--task", type=str, default="category", choices=["category", "multiclass", "binary"])
    args = parser.parse_args()
    simulate_realtime_detection(num_samples=args.samples, task=args.task)
