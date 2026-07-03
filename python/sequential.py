from processing import process_data

def run_sequential(dataset):

    result = []

    for data in dataset:
        result.append(process_data(data))

    return result