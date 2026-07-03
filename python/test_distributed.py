import json

from config import DATASET_FILE
from distributed import run_distributed


def main():

    with open(DATASET_FILE, "r") as f:
        dataset = json.load(f)

    # Biar cepet test, jangan langsung 100 data
    dataset = dataset[:10]

    print("Running Distributed...")

    elapsed = run_distributed(dataset)

    print(f"\nDistributed selesai dalam {elapsed:.4f} detik")


if __name__ == "__main__":
    main()