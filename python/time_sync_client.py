import json
import time
import threading

import paho.mqtt.client as mqtt

from config import *


class TimeSyncClient:
    """
    Dipakai oleh setiap node (worker, dispatcher, dll) untuk menyelaraskan
    jam lokalnya terhadap TimeServer.

        t1 -> waktu node mengirim request
        t2 -> waktu server menerima request
        t3 -> waktu server mengirim balasan
        t4 -> waktu node menerima balasan

        round_trip_delay = (t4 - t1) - (t3 - t2)
        offset           = ((t2 - t1) + (t3 - t4)) / 2
    """

    def __init__(self, node_id, clock_drift=0.0):

        self.node_id = node_id
        self.clock_drift = clock_drift

        self.offset = 0.0
        self.delay = 0.0

        self._synced = threading.Event()
        self._connected = threading.Event()

        self.client = mqtt.Client()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def local_time(self):
        return time.time() + self.clock_drift

    def synced_time(self):
        return self.local_time() + self.offset

    def on_connect(self, client, userdata, flags, rc):

        client.subscribe(
            f"{TIME_SYNC_RESPONSE_TOPIC}/{self.node_id}"
        )

        self._connected.set()

    def on_message(self, client, userdata, msg):

        data = json.loads(msg.payload.decode())

        t1 = data["t1"]
        t2 = data["t2"]
        t3 = data["t3"]
        t4 = self.local_time()

        self.delay = (t4 - t1) - (t3 - t2)

        self.offset = (
            (t2 - t1) +
            (t3 - t4)
        ) / 2

        self._synced.set()

    def sync(self, timeout=5):

        self._connected.clear()
        self._synced.clear()

        self.client.connect(BROKER, PORT)

        self.client.loop_start()

        # Tunggu sampai connect + subscribe selesai
        if not self._connected.wait(timeout):

            self.client.loop_stop()
            self.client.disconnect()

            return False

        request = {
            "node_id": self.node_id,
            "t1": self.local_time()
        }

        info = self.client.publish(
            TIME_SYNC_REQUEST_TOPIC,
            json.dumps(request)
        )

        info.wait_for_publish()

        ok = self._synced.wait(timeout)

        self.client.loop_stop()
        self.client.disconnect()

        return ok