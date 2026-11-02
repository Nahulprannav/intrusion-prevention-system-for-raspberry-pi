import os
import sys
import time
import json
import logging
import joblib
from collections import deque
import numpy as np
import pandas as pd

from src.config import SAVED_MODELS_DIR, RESULTS_DIR

# Set up logging for Raspberry Pi IPS
LOG_DIR = os.path.join(RESULTS_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
IPS_LOG_FILE = os.path.join(LOG_DIR, "rpi_ips_prevention.log")

logging.basicConfig(
    filename=IPS_LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [RPI-IPS] %(message)s'
)

class CircularFlowBuffer:
    """
    Fixed-size circular ring-buffer for Raspberry Pi memory control (Section V-B).
    Prevents memory overflow during continuous long-term deployment on 1GB RAM.
    """
    def __init__(self, capacity: int = 1000):
        self.buffer = deque(maxlen=capacity)

    def append(self, flow_record: dict):
        self.buffer.append(flow_record)

    def get_recent(self, count: int = 10):
        return list(self.buffer)[-count:]

class RaspberryPiIntrusionPreventionSystem:
    """
    Autonomous Real-Time Intrusion Prevention System (IPS) for Raspberry Pi IoT Gateways.
    Implements the two-phase architecture and active response mechanisms from Section V.
    """
    def __init__(self, model_task: str = "category"):
        self.model_task = model_task
        self.pipeline_file = os.path.join(SAVED_MODELS_DIR, f"rpi_edge_{model_task}_pipeline.joblib")
        
        # Fallback to general champion if rpi_edge not yet created
        if not os.path.exists(self.pipeline_file):
            self.pipeline_file = os.path.join(SAVED_MODELS_DIR, f"champion_{model_task}_pipeline.joblib")

        print(f"[RPI-IPS Engine] Initializing Edge IPS with model: {self.pipeline_file}")
        artifacts = joblib.load(self.pipeline_file)
        self.model = artifacts['model']
        self.scaler = artifacts['scaler']
        self.label_encoder = artifacts['label_encoder']
        self.feature_cols = artifacts['feature_cols']
        self.class_names = artifacts['class_names']
        
        self.flow_buffer = CircularFlowBuffer(capacity=1000)
        self.blocked_ips = set()
        self.quarantine_ports = set()
        
        # Performance Counters (for Raspberry Pi telemetry)
        self.packets_processed = 0
        self.threats_blocked = 0
        self.total_inference_time_ms = 0.0

    def inspect_and_mitigate(self, packet_features: dict, source_ip: str = "192.168.1.105", dest_port: int = 80) -> dict:
        """
        Processes a single packet flow in real-time (<1ms budget):
        1. Feature standardization
        2. Threat inference
        3. Automated active prevention action (iptables/nftables generation)
        """
        t0 = time.perf_counter()

        # Vectorize features matching training column order
        vec = []
        for col in self.feature_cols:
            vec.append(float(packet_features.get(col, 0.0)))
        X_raw = np.array(vec, dtype=np.float32).reshape(1, -1)

        # Scale features
        X_scaled = self.scaler.transform(X_raw)

        # Predict threat
        if hasattr(self.model, 'predict_proba'):
            probs = self.model.predict_proba(X_scaled)[0]
            pred_idx = np.argmax(probs)
            confidence = float(probs[pred_idx]) * 100
        else:
            pred_idx = self.model.predict(X_scaled)[0]
            confidence = 100.0

        latency_ms = (time.perf_counter() - t0) * 1000.0
        predicted_class = self.label_encoder.inverse_transform([pred_idx])[0]

        # Update telemetry
        self.packets_processed += 1
        self.total_inference_time_ms += latency_ms

        # Determine Active Prevention Policy (Section V-B)
        action_decision = self._enforce_prevention_policy(predicted_class, source_ip, dest_port, confidence)

        if action_decision['action'] != "PASS":
            self.threats_blocked += 1

        result = {
            "source_ip": source_ip,
            "dest_port": dest_port,
            "verdict": predicted_class,
            "confidence": f"{confidence:.1f}%",
            "latency_ms": round(latency_ms, 3),
            "ips_action": action_decision['action'],
            "firewall_rule": action_decision['rule'],
            "mitigation_summary": action_decision['description']
        }

        # Store in circular buffer and log audit trail
        self.flow_buffer.append(result)
        logging.info(f"Packet from {source_ip}:{dest_port} -> Verdict: {predicted_class} ({confidence:.1f}%) | Action: {action_decision['action']} | Latency: {latency_ms:.3f}ms")

        return result

    def _enforce_prevention_policy(self, threat_type: str, source_ip: str, dest_port: int, confidence: float) -> dict:
        """
        Generates automated Linux iptables/nftables rules based on threat severity.
        """
        threat_upper = threat_type.upper()

        if "BENIGN" in threat_upper:
            return {
                "action": "PASS",
                "rule": "ACCEPT",
                "description": "Legitimate flow allowed without penalty."
            }
        
        elif "DDOS" in threat_upper or "DOS" in threat_upper:
            # Immediate drop & rate-limit attacker
            rule = f"iptables -I INPUT -s {source_ip} -j DROP"
            self.blocked_ips.add(source_ip)
            return {
                "action": "BLOCK_AND_DROP",
                "rule": rule,
                "description": f"Volumetric flood detected! IP {source_ip} blacklisted in iptables DROP table."
            }

        elif "RECON" in threat_upper or "SCAN" in threat_upper:
            # Port quarantine & reject probe
            rule = f"iptables -I INPUT -p tcp --dport {dest_port} -s {source_ip} -j REJECT"
            self.quarantine_ports.add(dest_port)
            return {
                "action": "QUARANTINE_PORT",
                "rule": rule,
                "description": f"Network scanning detected! Port {dest_port} quarantined for source {source_ip}."
            }

        elif "MIRAI" in threat_upper or "MALWARE" in threat_upper:
            # Botnet quarantine & command-and-control port isolation
            rule = f"iptables -I OUTPUT -d {source_ip} -j DROP; iptables -I INPUT -s {source_ip} -j DROP"
            self.blocked_ips.add(source_ip)
            return {
                "action": "ISOLATE_BOTNET",
                "rule": rule,
                "description": f"Mirai/Malware IoT communication intercepted! Bidirectional traffic terminated."
            }

        elif "SPOOFING" in threat_upper or "ARP" in threat_upper:
            # ARP poison / DNS cache poison defense
            rule = f"ip neigh replace {source_ip} lladdr 00:00:00:00:00:00 nud failed"
            return {
                "action": "ARP_DEFENSE",
                "rule": rule,
                "description": f"Spoofing detected! Invalidating poisoned ARP entry for {source_ip}."
            }

        else: # Web_Attack, Brute_Force, etc.
            rule = f"iptables -A INPUT -s {source_ip} -m recent --name BAD_CLIENTS --set -j DROP"
            return {
                "action": "THROTTLE_DROP",
                "rule": rule,
                "description": f"Application layer attack detected! Added {source_ip} to BAD_CLIENTS throttle table."
            }

    def print_telemetry(self):
        """
        Outputs edge system resource metrics matching Raspberry Pi hardware constraints.
        """
        avg_latency = self.total_inference_time_ms / max(1, self.packets_processed)
        throughput_pps = 1000.0 / max(0.001, avg_latency)

        print("\n" + "="*70)
        print("          RASPBERRY PI EDGE IPS TELEMETRY REPORT")
        print("="*70)
        print(f"  Total Packets Inspected:      {self.packets_processed:,}")
        print(f"  Intrusions Blocked:           {self.threats_blocked:,}")
        print(f"  Average Processing Latency:   {avg_latency:.3f} ms / packet (< 1.0 ms budget)")
        print(f"  Theoretical Edge Throughput:  {throughput_pps:,.0f} packets / second")
        print(f"  Active Blacklisted IPs:       {len(self.blocked_ips)}")
        print(f"  Quarantined Ports:            {len(self.quarantine_ports)}")
        print(f"  Audit Log Path:               {IPS_LOG_FILE}")
        print("="*70)
