#include <WiFi.h>

const int thumb_pin = 34;
const int index_pin = 35;
const int middle_pin = 32;
const int ring_pin = 33;
const int pinky_pin = 25;

int thumb_value, index_value, middle_value, ring_value, pinky_value;

const char* ssid = "wifi";
const char* password = "12345678";

const char* host = "10.179.221.238";
const uint16_t port = 8080;

void initWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  Serial.println(WiFi.localIP());
}

WiFiClient client;

void setup() {
  Serial.begin(115200);
  delay(1000);
  initWiFi();
  while(!client.connect(host, port))
    Serial.println("Connecting...");
}

void loop() {
  thumb_value = analogRead(thumb_pin);
  index_value = analogRead(index_pin);
  middle_value = analogRead(middle_pin);
  ring_value = analogRead(ring_pin);
  pinky_value = analogRead(pinky_pin);
  delay(100);

  client.println("$");
  client.println(thumb_value);
  client.println(index_value);
  client.println(middle_value);
  client.println(ring_value);
  client.println(pinky_value);
  client.flush();
}
