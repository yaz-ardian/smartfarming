import json
import os

import paho.mqtt.client as mqtt

from config import *

dataset = []


def on_connect(client, userdata, flags, rc):

    print("Connected!")

    client.subscribe(RAW_TOPIC)


def on_message(client, userdata, msg):

    global dataset

    data = json.loads(msg.payload.decode())

    data["id"] = len(dataset) + 1

    dataset.append(data)

    print(f"{len(dataset)}/{DATASET_SIZE}")

    if len(dataset) >= DATASET_SIZE:

        os.makedirs("datasets", exist_ok=True)

        with open(DATASET_FILE, "w") as f:

            json.dump(dataset, f, indent=4)

        print()
        print("Dataset Saved!")

        client.disconnect()


client = mqtt.Client()

client.on_connect = on_connect

client.on_message = on_message

client.connect(BROKER, PORT)

client.loop_forever()

print("Receiver Finished")