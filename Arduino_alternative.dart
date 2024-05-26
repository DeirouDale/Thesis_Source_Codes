#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "DIR-612-ED2B";
const char* password = "64493930";
const char* mqttBroker = "192.168.0.143"; // Change this to your MQTT broker's IP address or hostname
const char* mqttId = "ESP32_client2";//1 is right, 2 is left
const char* pubId = "esp32/sensor2";
const int mqttPort = 1883; // MQTT default port

const int fsrPinA = 34;
const int fsrPinB = 35;
const int fsrPinC = 32;

int fsrValueA;
int fsrValueB;
int fsrValueC;

int stateA;
int stateB;
int stateC;

int send_flag = 0;
unsigned long interval = 14; //70 inputs per second
unsigned long timer;
unsigned long ref_timer = 0;

WiFiClient espClient;
PubSubClient mqttClient(espClient);

void setup_wifi() {
  delay(10);
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println(WiFi.localIP());
}

void setup_mqtt() {
  mqttClient.setServer(mqttBroker, mqttPort);
  while (!mqttClient.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (mqttClient.connect(mqttId)) {// 2 is left, 1 is right
      Serial.println("connected");
      mqttClient.subscribe("rpi/broadcast");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" try again in 1 second");
      delay(1000);
    }
  }
}
void callback(char* topic, byte* message, unsigned int length){
  String messageTemp;

  for (int i = 0 ; i< length;i++){
    messageTemp += (char)message[i];
  }
  Serial.println(messageTemp);
  if(String(topic) == "rpi/broadcast"){
    if(messageTemp == "Req_Data"){
      //send data here
      char message[100];
      sprintf(message, "%d%d%d", stateA, stateB, stateC); // Print the binary representation
      mqttClient.publish(pubId, message); //sensor 2 is left, sensor 1 is right
      //Serial.println("Published FSR readings to MQTT");
    
    }
    if(messageTemp == "Start"){
      //set reference timer 
      ref_timer = millis();
      send_flag = 1;
    }
    if(messageTemp == "Stop"){
      //send collated data here
      send_flag = 0;
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(fsrPinA, INPUT_PULLUP);
  pinMode(fsrPinB, INPUT_PULLUP);
  pinMode(fsrPinC, INPUT_PULLUP);

  setup_wifi();
  setup_mqtt();
  mqttClient.setCallback(callback);
}

void loop() {
  if (millis() - timer >= interval) {
  timer = millis();
  fsrValueA = analogRead(fsrPinA);
  fsrValueB = analogRead(fsrPinB);
  fsrValueC = analogRead(fsrPinC);

  // Determine binary state based on threshold (50% of 4095)
  stateA = (fsrValueA > 1228) ? 1 : 0;  // A (MSB)
  stateB = (fsrValueB > 1228) ? 1 : 0;  // B (middle)
  stateC = (fsrValueC > 1228) ? 1 : 0;  // C (LSB)
  // Create a binary value (000 to 111)
  //Serial.println(String(timer2)+" "+String(stateA)+String(stateB)+String(stateC));
  char message[100];
  sprintf(message, "(%d,%d%d%d)",millis()-ref_timer,stateA,stateB,stateC);
  if(send_flag == 1){
  mqttClient.publish(pubId, message);
  }
  mqttClient.loop();
  }
}

// unsigned long interval = 142.857142857;
  
//   if (millis() - timer >= interval) {
//     timer = millis();
//     int fsrValueA = analogRead(fsrPinA);
//     int fsrValueB = analogRead(fsrPinB);
//     int fsrValueC = analogRead(fsrPinC);

//     // Determine binary state based on threshold (50% of 4095)
//     int stateA = (fsrValueA > 1228) ? 1 : 0;  // A (MSB)
//     int stateB = (fsrValueB > 1228) ? 1 : 0;  // B (middle)
//     int stateC = (fsrValueC > 1228) ? 1 : 0;  // C (LSB)

//     // Create a binary value (000 to 111)
//     int binaryValue = (stateA << 2) | (stateB << 1) | stateC;

//     char message[100];
//     sprintf(message, "%d%d%d", stateA, stateB, stateC); // Print the binary representation
//     mqttClient.publish("esp32/sensor2", message);
//     Serial.println("Published FSR readings to MQTT");
//   }