#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "Shopify Guest";      
const char* password = "welcome2shopify"; 
const char* serverAddress = "http://10.93.94.131:5000";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi");
  }
  
  Serial.println("Connected to WiFi");
}

void loop() {

  DynamicJsonDocument jsonDoc(200);
  jsonDoc["test"] = 123;
  String payload;
  serializeJson(jsonDoc, payload);

  HTTPClient http;
 Serial.println("Server Address: " + String(serverAddress));

  http.begin(serverAddress);
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(payload);

  if (httpResponseCode > 0) {
    Serial.printf("HTTP Response code: %d\n", httpResponseCode);
    String response = http.getString();
    Serial.println(response);
  } else {
    Serial.printf("HTTP Request failed: %s\n", http.errorToString(httpResponseCode).c_str());
  }

  http.end();

  delay(5000);
}
