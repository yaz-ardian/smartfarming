import json
import threading

import paho.mqtt.client as mqtt

from config import *

class Collector:

    def __init__(self, total_jobs):

        self.total_jobs = total_jobs

        self.results = []

        self.finished = threading.Event()
        self.ready = threading.Event()

        self.client = mqtt.Client()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):

        print("Collector Connected")

        client.subscribe(RESULT_TOPIC)

        # Beritahu bahwa collector sudah siap menerima data
        self.ready.set()

    def on_message(self, client, userdata, msg):

        data = json.loads(msg.payload.decode())

        self.results.append(data)

        if DEBUG:
            print(f"Collected {len(self.results)}/{self.total_jobs}")

        if len(self.results) >= self.total_jobs:

            print("All jobs collected.")

            self.finished.set()

            self.client.disconnect()

    def start(self):

        self.client.connect(BROKER, PORT)

        threading.Thread(
            target=self.client.loop_forever,
            daemon=True
        ).start()

    def wait(self):

        self.finished.wait()

        return self.results