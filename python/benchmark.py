import json
import os
import time
import pandas as pd

from config import *
from sequential import run_sequential
from parallel import run_parallel
from distributed import run_distributed


def load_dataset():

    with open(DATASET_FILE, "r") as f:
        return json.load(f)


def create_dataset(base_dataset, size):

    dataset = []

    current_id = 1

    while len(dataset) < size:

        for item in base_dataset:

            if len(dataset) >= size:
                break

            new_item = item.copy()
            new_item["id"] = current_id

            dataset.append(new_item)

            current_id += 1

    return dataset


def normalize_results(results):

    normalized = []

    for item in results:

        new_item = item.copy()

        # Hapus metadata worker (khusus distributed)
        new_item.pop("worker", None)

        normalized.append(new_item)

    normalized = sorted(normalized, key=lambda x: x["id"])

    return normalized


def benchmark_sequential(dataset):

    start = time.perf_counter()

    result = run_sequential(dataset)

    end = time.perf_counter()

    return end - start, result


def benchmark_parallel(dataset):

    start = time.perf_counter()

    result = run_parallel(dataset)

    end = time.perf_counter()

    return end - start, result


def benchmark_distributed(dataset):

    return run_distributed(dataset)


def main():

    os.makedirs("results", exist_ok=True)

    base_dataset = load_dataset()

    benchmark_results = []

    print("========== SMART FARMING BENCHMARK ==========")

    for size in BENCHMARK_SIZES:

        print(f"\nDataset Size : {size}")

        dataset = create_dataset(base_dataset, size)

        # ===============================
        # Sequential
        # ===============================
        print("Running Sequential...")
        seq_time, seq_result = benchmark_sequential(dataset)

        # ===============================
        # Parallel
        # ===============================
        print("Running Parallel...")
        par_time, par_result = benchmark_parallel(dataset)

        # ===============================
        # Distributed
        # ===============================
        print("Running Distributed...")
        dist_time, dist_result = benchmark_distributed(dataset)

        # ===============================
        # Validation
        # ===============================

        seq_result = normalize_results(seq_result)
        par_result = normalize_results(par_result)
        dist_result = normalize_results(dist_result)

        validation = (
            seq_result == par_result == dist_result
        )

        print(f"Result Validation : {'PASSED' if validation else 'FAILED'}")

        # ===============================
        # Throughput
        # ===============================

        seq_throughput = size / seq_time
        par_throughput = size / par_time
        dist_throughput = size / dist_time

        # ===============================
        # Speedup
        # ===============================

        parallel_speedup = seq_time / par_time
        distributed_speedup = seq_time / dist_time

        # ===============================
        # Efficiency
        # ===============================

        parallel_efficiency = parallel_speedup / NUM_CORES
        distributed_efficiency = distributed_speedup / NUM_WORKERS

        # ===============================
        # Improvement (%)
        # ===============================

        parallel_improvement = (
            (seq_time - par_time) / seq_time
        ) * 100

        distributed_improvement = (
            (seq_time - dist_time) / seq_time
        ) * 100

        # ===============================
        # Save Result
        # ===============================

        benchmark_results.append({

            "Dataset": size,

            "Sequential Time (s)": round(seq_time, 4),
            "Parallel Time (s)": round(par_time, 4),
            "Distributed Time (s)": round(dist_time, 4),

            "Sequential Throughput (data/s)": round(seq_throughput, 2),
            "Parallel Throughput (data/s)": round(par_throughput, 2),
            "Distributed Throughput (data/s)": round(dist_throughput, 2),

            "Parallel Speedup": round(parallel_speedup, 2),
            "Distributed Speedup": round(distributed_speedup, 2),

            "Parallel Efficiency": round(parallel_efficiency, 2),
            "Distributed Efficiency": round(distributed_efficiency, 2),

            "Parallel Improvement (%)": round(parallel_improvement, 2),
            "Distributed Improvement (%)": round(distributed_improvement, 2),

            "Validation": validation

        })

        # ===============================
        # Console Output
        # ===============================

        print("\nExecution Time")
        print(f"Sequential  : {seq_time:.4f} s")
        print(f"Parallel    : {par_time:.4f} s")
        print(f"Distributed : {dist_time:.4f} s")

        print("\nThroughput")
        print(f"Sequential  : {seq_throughput:.2f} data/s")
        print(f"Parallel    : {par_throughput:.2f} data/s")
        print(f"Distributed : {dist_throughput:.2f} data/s")

        print("\nSpeedup")
        print(f"Parallel    : {parallel_speedup:.2f}x")
        print(f"Distributed : {distributed_speedup:.2f}x")

        print("\nEfficiency")
        print(f"Parallel    : {parallel_efficiency:.2f}")
        print(f"Distributed : {distributed_efficiency:.2f}")

        print("\nImprovement")
        print(f"Parallel    : {parallel_improvement:.2f}%")
        print(f"Distributed : {distributed_improvement:.2f}%")

        print("-" * 60)

    df = pd.DataFrame(benchmark_results)

    df.to_csv("results/benchmark.csv", index=False)

    print("\n========================================")
    print("Benchmark selesai.")
    print("Hasil disimpan di results/benchmark.csv")
    print("========================================")


if __name__ == "__main__":
    main()