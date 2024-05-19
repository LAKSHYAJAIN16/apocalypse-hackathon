#include <chrono>
#include <WiFi.h>
#include <WebServer.h>
#include <PubSubClient.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <iostream>


#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

int heart;
int ideas;
float lat_glob;
float longi_glob;

#define OLED_RESET -1
#define SCREEN_ADDRESS 0x3C
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

//zButton button(27);
const char* mqtt_server = "broker.hivemq.com";
const char* ssid = "Shopify Guests";
const char* password = "welcome2shopify";
const char* tips[] = {
        "Stay calm and assess your situation.",
        "Find or create a shelter to protect yourself from the elements.",
        "Locate a water source and purify any water you find.",
        "Create a signal to help rescuers find you.",
        "Make a fire for warmth, cooking, and signaling.",
        "Find and identify edible plants and animals.",
        "Learn basic first aid and carry a first aid kit.",
        "Stay dry to prevent hypothermia.",
        "Avoid unnecessary risks and injuries.",
        "Use the sun, stars, and natural landmarks for navigation.",
        "Carry a multi-tool or knife for various tasks.",
        "Pack high-energy, non-perishable food items.",
        "Wear appropriate clothing and layers for the environment.",
        "Keep your feet dry and take care of blisters.",
        "Learn to tie basic knots for shelter and other uses.",
        "Use reflective materials to attract attention.",
        "Stay in one place to increase chances of being found.",
        "Avoid drinking alcohol as it dehydrates you.",
        "Know how to signal for help using three blasts or flashes.",
        "Stay positive and keep a survival mindset."};

WiFiClient espClient;
PubSubClient client(espClient);

float distance_to_horde = 242;
const char* ID = "123456543234323456";

const int ID_LENGTH = 18;

void callback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.println("Message arrived [");
  Serial.print(message);
  Serial.println("] ");

  String id = message.substring(ID_LENGTH);
  if(id == ID){
    float dist = message.substring(ID_LENGTH, message.length()).toFloat();
    distance_to_horde = dist;
  }
}

void reconnect() {
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  while (!client.connected()) {
    if (client.connect(ID)) {
      Serial.println("connected");

      HTTPClient http;
      http.begin("https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAGD7NH0n0U1FFajOMxMJ3PiSzg-PIKuDw");
      http.addHeader("Content-Type", "application/json");

      int httpResponseCode = http.POST("{}");

      if (httpResponseCode > 0) {
        String payload = http.getString();
        Serial.println("HTTP Response code: " + String(httpResponseCode));
        Serial.println("Response: " + payload);
        http.end();

        DynamicJsonDocument doc(1024);
        deserializeJson(doc, payload);
        float lat = doc["location"]["lat"];
        lat_glob = lat;
        float lng = doc["location"]["lng"];
        longi_glob = lng;
        
        bool conn = client.subscribe("hordedetection88u8");
        if(conn == true){
          Serial.println("Subscribed");
        }
        else{
          Serial.println("You fucked up");
        }

        String msg = "Latitude: " + String(lat, 6) + ", Longitude: " + String(lng, 6) + ", ID: " + ID;
        client.publish("geolocation", msg.c_str());
      } else {
        Serial.println("Error");
      }
    }
  }
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  Serial.println("Connected");
  
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  reconnect();
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    for(;;);
  }

  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  display.println("Hello!");
  display.display();
  delay(2000);
  display.clearDisplay();
  //Heartbeat monitor costed too much on its own to justify purchasing
  heart = random(45, 122);
  ideas = random(0, 21);
  //button.setDebounceTime(50);
}

void loop() {
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 18);
  display.display();
  if (!client.connected()) {
    reconnect();
  }
  if(WiFi.status()== WL_CONNECTED){
  }

  //button.loop();
  //button.getState();
  float time = millis();
  if(int(time) % 15000 < 3000)
  {
    display.clearDisplay();
    display.println(tips[ideas]);
  } 
  if(int(time) % 36000 > 5000 && int(time) % 36000 < 10000)
  {
    display.clearDisplay();
    display.println("Pulse is " + String(heart) + " beats per minute");
  }
  if(int(time) % 36000 > 15000 && int(time) % 36000 < 20000)
  {
    display.clearDisplay();
    display.println("Latitude : Longitude");
    display.println(String(lat_glob) + " : " + String(longi_glob));
    //Heartbeat monitor costed too much on its own to justify purchasing
    heart = random(45, 122);
  }
  if(int(time) % 36000 > 25000 && int(time) % 36000 < 30000)
  {
    display.clearDisplay();
    display.setCursor(0, 32);
    display.println("Nearest Horde is " + String(distance_to_horde) + " km far away");
  }
  if(int(time) % 36000 > 30000)
  {
    const auto now = std::chrono::system_clock::now();
    const std::time_t t_c = std::chrono::system_clock::to_time_t(now);
    display.clearDisplay();
    display.println(std::ctime(&t_c));
  }

  client.loop();
}