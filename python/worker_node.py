import json
import sys

import paho.mqtt.client as mqtt

from config import *
from processing import process_data

worker_id = int(sys.argv[1])

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

    client.publish(
        RESULT_TOPIC,
        json.dumps(result)
    )


client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

client.loop_forever()