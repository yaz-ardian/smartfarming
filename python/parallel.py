from concurrent.futures import ProcessPoolExecutor

from config import NUM_CORES
from processing import process_data


def run_parallel(dataset):

    with ProcessPoolExecutor(max_workers=NUM_CORES) as executor:
        result = list(executor.map(process_data, dataset))

    return result