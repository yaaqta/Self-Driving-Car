#include "ESP8266WiFi.h"
#define HEADER 10

const char* ssid = "Thao";
const char* password = "12345678";
int pin0 = 16;
int pin1 = 5;
int pin2 = 4;

WiFiServer server(1234);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(1000);
  WiFi.hostname("");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED){
    delay(1000);
    Serial.println("Connecting ...");
  }

  Serial.println("Connected to WiFi. IP: ");
  Serial.println(WiFi.localIP());

  server.begin();
  pinMode(pin0, OUTPUT);
  pinMode(pin1, OUTPUT);
  pinMode(pin2, OUTPUT);
}

void stopAll(){
  digitalWrite(pin2, LOW);
}

void openAll(){
  digitalWrite(pin2, HIGH);
}

void handleRequest(String request){
  if(request == (String("forward") + char(13))){
    openAll();
    digitalWrite(pin0, HIGH);
    digitalWrite(pin1, HIGH);
    delay(100);
    stopAll();
    Serial.println("Done Forward");
  }
  else if(request == (String("backward") + char(13))){
    openAll();
    digitalWrite(pin0, LOW);
    digitalWrite(pin1, LOW);
    delay(100);
    stopAll(); 
    Serial.println("Done BackWard");
  }
  else if(request == (String("left") + char(13))){
    openAll();
    digitalWrite(pin0, LOW);
    digitalWrite(pin1, HIGH);
    delay(100);
    stopAll(); 
    Serial.println("Done Turn Left");
  }
  else if(request == (String("right") + char(13))){
    openAll();
    digitalWrite(pin0, HIGH);
    digitalWrite(pin1, LOW);
    delay(100);
    stopAll(); 
    Serial.println("Done Turn Right");
  }
}

void handleClient(){
  WiFiClient client = server.available();
  String result = "";
  if(client){
    Serial.println("Connected");  
    while(client.connected()){
      while(client.available() > 0){
        char c = client.read();
        result += c;
      }
      if (result != ""){
        handleRequest(result);
        result = "";
      }
    }
    client.stop();
    Serial.println("Client is disconnected.");
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  handleClient();
}
