#include <WiFi.h>
#include <PubSubClient.h>

// WiFi & MQTT Configuration
const char* ssid = "Wokwi-GUEST";
const char* password = "";

const char* mqttServer = "test.mosquitto.org";
const int mqttPort = 1883;
const char* topic = "smartfarm/data";

// MQTT Client
WiFiClient espClient;
PubSubClient client(espClient);

// Connect WiFi
void setupWiFi() {

  Serial.print("Connecting to WiFi");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi Connected!");
}

// Connect MQTT
void reconnectMQTT() {

  while (!client.connected()) {

    Serial.print("Connecting to MQTT... ");

    if (client.connect("ESP32Farm")) {

      Serial.println("SUCCESS!");

    } else {

      Serial.print("FAILED, rc=");
      Serial.print(client.state());
      Serial.println(" -> Retry in 2 seconds");

      delay(2000);
    }
  }
}

// Setup
void setup() {

  Serial.begin(115200);

  delay(1000);

  setupWiFi();

  client.setServer(mqttServer, mqttPort);
}

// Loop
void loop() {

  if (!client.connected()) {
    reconnectMQTT();
  }

  client.loop();

  int grid = random(1, 501);

  float temp = random(200, 380) / 10.0;
  int hum = random(40, 90);
  int soil = random(300, 900);
  float ph = random(50, 75) / 10.0;
  int light = random(200, 1000);

  String payload = "{";
  payload += "\"grid\":\"Grid" + String(grid) + "\",";
  payload += "\"suhu\":" + String(temp) + ",";
  payload += "\"kelembapan\":" + String(hum) + ",";
  payload += "\"tanah\":" + String(soil) + ",";
  payload += "\"ph\":" + String(ph) + ",";
  payload += "\"cahaya\":" + String(light);
  payload += "}";

  Serial.println(payload);

  client.publish(topic, payload.c_str());

  delay(1000);
}