import json
import sys

import paho.mqtt.client as mqtt

from config import *
from processing import process_data
from time_sync_client import TimeSyncClient   

worker_id = int(sys.argv[1])

time_sync = TimeSyncClient(f"worker_{worker_id}")
time_sync.sync()
client = mqtt.Client()


def on_connect(client, userdata, flags, rc):

    topic = f"{JOB_TOPIC_PREFIX}/{worker_id}"

    client.subscribe(topic)

    print(f"Worker {worker_id} connected.")

def on_message(client, userdata, msg):

    data = json.loads(msg.payload.decode())

    if DEBUG:
        print(f"Worker {worker_id} processing ID {data['id']}")

    result = process_data(data)

    result["worker"] = worker_id
    result["timestamp"] = time_sync.synced_time()

    client.publish(
        RESULT_TOPIC,
        json.dumps(result)
    )


client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

client.loop_forever()