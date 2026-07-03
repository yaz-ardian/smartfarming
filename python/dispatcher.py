import json
import time

import paho.mqtt.client as mqtt

from config import *

client = mqtt.Client()


def dispatch(dataset):

    client.connect(BROKER, PORT)

    client.loop_start()

    print(f"Dispatcher started ({len(dataset)} jobs)...")

    worker = 1

    for data in dataset:

        topic = f"{JOB_TOPIC_PREFIX}/{worker}"

        info = client.publish(topic, json.dumps(data))

        info.wait_for_publish()   # Tunggu publish selesai

        worker += 1

        if worker > NUM_WORKERS:
            worker = 1

    print("Dispatcher finished.")

    time.sleep(0.5)

    client.loop_stop()

    client.disconnect()