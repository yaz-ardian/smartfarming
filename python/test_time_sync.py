import time

from time_sync_client import TimeSyncClient


def main():

    print("========== SINKRONISASI WAKTU ANTAR NODE ==========\n")
    print(f"{'Node':<10}{'Drift (s)':<12}{'Offset (s)':<14}{'Delay (s)':<12}"
          f"{'Selisih Sblm':<15}{'Selisih Ssdh':<15}")

    # Simulasikan 3 node dengan jam lokal yang TIDAK sinkron
    nodes = [
        TimeSyncClient("worker_1", clock_drift=2.5),
        TimeSyncClient("worker_2", clock_drift=-1.3),
        TimeSyncClient("worker_3", clock_drift=0.8),
    ]

    reference_time = time.time()

    for node in nodes:

        before = node.local_time() - reference_time

        ok = node.sync()

        if not ok:
            print(f"{node.node_id:<10} GAGAL sinkronisasi (timeout)")
            continue

        after = node.synced_time() - reference_time

        print(
            f"{node.node_id:<10}"
            f"{node.clock_drift:<12.2f}"
            f"{node.offset:<14.4f}"
            f"{node.delay:<12.4f}"
            f"{before:<15.4f}"
            f"{after:<15.4f}"
        )

    print("\nSelisih waktu antar node berhasil dikoreksi mendekati 0 setelah sinkronisasi.")


if __name__ == "__main__":
    main()