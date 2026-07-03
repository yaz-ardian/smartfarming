import json
import time

import paho.mqtt.client as mqtt

from config import *


class TimeServer:
    """
    Node otoritas waktu (time authority) dalam simulasi Smart Farming.

    Setiap node lain (worker, dispatcher, dsb) bisa meminta koreksi waktu
    ke node ini. Pendekatan yang dipakai mirip Cristian's Algorithm / NTP:
    client mengirim t1, server mencatat t2 (terima) & t3 (kirim balasan),
    lalu client menghitung offset berdasarkan t1..t4.
    """

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("Time Server Connected.")
        client.subscribe(TIME_SYNC_REQUEST_TOPIC)

    def on_message(self, client, userdata, msg):

        request = json.loads(msg.payload.decode())

        node_id = request["node_id"]
        t1 = request["t1"]          # waktu node mengirim request

        t2 = time.time()            # waktu server menerima request

        response = {
            "node_id": node_id,
            "t1": t1,
            "t2": t2,
            "t3": time.time()       # waktu server mengirim balasan
        }

        topic = f"{TIME_SYNC_RESPONSE_TOPIC}/{node_id}"

        client.publish(topic, json.dumps(response))

        if DEBUG:
            print(f"Sync request dari '{node_id}' dilayani.")

    def start(self):
        self.client.connect(BROKER, PORT)
        self.client.loop_forever()


if __name__ == "__main__":
    print("========== TIME SERVER (Sinkronisasi Waktu Antar Node) ==========")
    server = TimeServer()
    server.start()
