import os

# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dataset paths
DATASET_DIR = os.path.join(BASE_DIR, "CICIOT23")
TRAIN_CSV = os.path.join(DATASET_DIR, "train", "train.csv")
VAL_CSV = os.path.join(DATASET_DIR, "validation", "validation.csv")
TEST_CSV = os.path.join(DATASET_DIR, "test", "test.csv")

# Output paths
SAMPLED_DATA_DIR = os.path.join(BASE_DIR, "data_sampled")
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
FIGURES_DIR = os.path.join(RESULTS_DIR, "figures")
METRICS_DIR = os.path.join(RESULTS_DIR, "metrics")

# Sampled file paths
SAMPLED_TRAIN_FILE = os.path.join(SAMPLED_DATA_DIR, "train_stratified.parquet")
SAMPLED_VAL_FILE = os.path.join(SAMPLED_DATA_DIR, "val_stratified.parquet")
SAMPLED_TEST_FILE = os.path.join(SAMPLED_DATA_DIR, "test_stratified.parquet")

# 46 Network Flow Features
FEATURE_COLUMNS = [
    'flow_duration', 'Header_Length', 'Protocol Type', 'Duration', 'Rate', 'Srate', 'Drate',
    'fin_flag_number', 'syn_flag_number', 'rst_flag_number', 'psh_flag_number', 'ack_flag_number',
    'ece_flag_number', 'cwr_flag_number', 'ack_count', 'syn_count', 'fin_count', 'urg_count',
    'rst_count', 'HTTP', 'HTTPS', 'DNS', 'Telnet', 'SMTP', 'SSH', 'IRC', 'TCP', 'UDP', 'DHCP',
    'ARP', 'ICMP', 'IPv', 'LLC', 'Tot sum', 'Min', 'Max', 'AVG', 'Std', 'Tot size', 'IAT',
    'Number', 'Magnitue', 'Radius', 'Covariance', 'Variance', 'Weight'
]

LABEL_COLUMN = 'label'

# Official CICIoT2023 34 Fine-Grained Classes
ALL_CLASSES_34 = [
    'Backdoor_Malware', 'BenignTraffic', 'BrowserHijacking', 'CommandInjection',
    'DDoS-ACK_Fragmentation', 'DDoS-HTTP_Flood', 'DDoS-ICMP_Flood', 'DDoS-ICMP_Fragmentation',
    'DDoS-PSHACK_Flood', 'DDoS-RSTFINFlood', 'DDoS-SYN_Flood', 'DDoS-SlowLoris',
    'DDoS-SynonymousIP_Flood', 'DDoS-TCP_Flood', 'DDoS-UDP_Flood', 'DDoS-UDP_Fragmentation',
    'DNS_Spoofing', 'DictionaryBruteForce', 'DoS-HTTP_Flood', 'DoS-SYN_Flood',
    'DoS-TCP_Flood', 'DoS-UDP_Flood', 'MITM-ArpSpoofing', 'Mirai-greeth_flood',
    'Mirai-greip_flood', 'Mirai-udpplain', 'Recon-HostDiscovery', 'Recon-OSScan',
    'Recon-PingSweep', 'Recon-PortScan', 'SqlInjection', 'Uploading_Attack',
    'VulnerabilityScan', 'XSS'
]

# Official 8 Macro Categories Mapping
CATEGORY_MAPPING_8 = {
    # DDoS Attacks
    'DDoS-ACK_Fragmentation': 'DDoS',
    'DDoS-HTTP_Flood': 'DDoS',
    'DDoS-ICMP_Flood': 'DDoS',
    'DDoS-ICMP_Fragmentation': 'DDoS',
    'DDoS-PSHACK_Flood': 'DDoS',
    'DDoS-RSTFINFlood': 'DDoS',
    'DDoS-SlowLoris': 'DDoS',
    'DDoS-SYN_Flood': 'DDoS',
    'DDoS-SynonymousIP_Flood': 'DDoS',
    'DDoS-TCP_Flood': 'DDoS',
    'DDoS-UDP_Flood': 'DDoS',
    'DDoS-UDP_Fragmentation': 'DDoS',

    # DoS Attacks
    'DoS-HTTP_Flood': 'DoS',
    'DoS-SYN_Flood': 'DoS',
    'DoS-TCP_Flood': 'DoS',
    'DoS-UDP_Flood': 'DoS',

    # Mirai Botnet
    'Mirai-greeth_flood': 'Mirai',
    'Mirai-greip_flood': 'Mirai',
    'Mirai-udpplain': 'Mirai',

    # Reconnaissance & Scanning
    'Recon-HostDiscovery': 'Recon',
    'Recon-OSScan': 'Recon',
    'Recon-PingSweep': 'Recon',
    'Recon-PortScan': 'Recon',
    'VulnerabilityScan': 'Recon',

    # Spoofing
    'DNS_Spoofing': 'Spoofing',
    'MITM-ArpSpoofing': 'Spoofing',

    # Web & Injection Attacks
    'BrowserHijacking': 'Web_Attack',
    'CommandInjection': 'Web_Attack',
    'SqlInjection': 'Web_Attack',
    'Uploading_Attack': 'Web_Attack',
    'XSS': 'Web_Attack',
    'Backdoor_Malware': 'Web_Attack',

    # Brute Force
    'DictionaryBruteForce': 'Brute_Force',

    # Benign Normal Traffic
    'BenignTraffic': 'Benign'
}

# Binary Mapping: Benign (0) vs Attack (1)
def get_binary_label(label: str) -> str:
    return 'Benign' if label == 'BenignTraffic' else 'Attack'

# Stratified Sampling Defaults
SAMPLE_CONFIG = {
    'train_per_class': 2500,     # Up to 2,500 samples per class for training (~75k rows)
    'val_per_class': 600,        # Up to 600 samples per class for validation (~20k rows)
    'test_per_class': 600,       # Up to 600 samples per class for test (~20k rows)
    'chunksize': 250000,
    'random_state': 42
}
