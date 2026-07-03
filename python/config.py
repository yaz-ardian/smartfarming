# MQTT CONFIGURATION
BROKER = "test.mosquitto.org"
PORT = 1883

PROJECT_ID = "smartfarm_068"

RAW_TOPIC = f"{PROJECT_ID}/data"
JOB_TOPIC_PREFIX = f"{PROJECT_ID}/jobs"
RESULT_TOPIC = f"{PROJECT_ID}/result"
TIME_SYNC_REQUEST_TOPIC = f"{PROJECT_ID}/time_sync/request"
TIME_SYNC_RESPONSE_TOPIC = f"{PROJECT_ID}/time_sync/response"

# DATASET
DATASET_SIZE = 100

DATASET_FILE = "datasets/dataset.json"

# Dataset yang akan dipakai benchmark
BENCHMARK_SIZES = [
    100,
    1000,
    10000
]

# PARALLEL
NUM_CORES = 4

# DISTRIBUTED

NUM_WORKERS = 3

# WORKLOAD SIMULATION
# Pilihan:
# LIGHT
# MEDIUM
# HEAVY

WORKLOAD = "HEAVY"

WORKLOAD_LEVEL = {
    "LIGHT": 1000,
    "MEDIUM": 5000,
    "HEAVY": 20000
}

HEAVY_ANALYSIS_ITERATIONS = WORKLOAD_LEVEL[WORKLOAD]

# DEBUG

DEBUG = False