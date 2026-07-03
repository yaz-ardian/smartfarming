import time

from dispatcher import dispatch
from collector import Collector


def run_distributed(dataset):

    collector = Collector(len(dataset))

    collector.start()

    collector.ready.wait()

    start = time.perf_counter()

    dispatch(dataset)

    results = collector.wait()

    end = time.perf_counter()

    # Urutkan hasil berdasarkan id
    results = sorted(results, key=lambda x: x["id"])

    return end - start, results