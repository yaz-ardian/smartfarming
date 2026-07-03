import json

from config import DATASET_FILE
from sequential import run_sequential
from parallel import run_parallel


def main():

    with open(DATASET_FILE, "r") as f:
        dataset = json.load(f)

    print("Running Sequential...")
    seq = run_sequential(dataset)

    print("Running Parallel...")
    par = run_parallel(dataset)

    print("\n==============================")
    print("HASIL TEST")
    print("==============================")

    print(f"Sequential Result : {len(seq)} data")
    print(f"Parallel Result   : {len(par)} data")

    print("\nData Pertama Sequential:")
    print(seq[0])

    print("\nData Pertama Parallel:")
    print(par[0])

    print("\nApakah hasilnya sama?")
    print(seq == par)


if __name__ == "__main__":
    main()