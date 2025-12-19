// Firmware placeholder - ESP32 porttiohjaus
// Tulossa: täysi toteutus järjestelmäkuvauksen mukaisesti

#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include "config.h"

// Global objects
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

// State variables
enum GateState {
  GATE_CLOSED,
  GATE_OPEN,
  GATE_OPENING,
  GATE_CLOSING,
  GATE_STOPPED,
  GATE_FAULT
};

GateState currentState = GATE_STOPPED;
unsigned long lastStateChange = 0;
bool motionDetected = false;
unsigned long motionDetectedTime = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("\n\n=== Portin ohjausjärjestelmä ===");
  Serial.print("Versio: ");
  Serial.println(DEVICE_VERSION);
  
  // Initialize pins
  pinMode(PIN_PWM_ENABLE, OUTPUT);
  pinMode(PIN_DIRECTION, OUTPUT);
  pinMode(PIN_RELAY_LOCK, OUTPUT);
  pinMode(PIN_RELAY_HEATER, OUTPUT);
  pinMode(PIN_MOSFET_LIGHTS, OUTPUT);
  
  pinMode(PIN_LIMIT_OPEN, INPUT_PULLUP);
  pinMode(PIN_LIMIT_CLOSED, INPUT_PULLUP);
  pinMode(PIN_MOTION_SENSOR, INPUT);
  pinMode(PIN_ESTOP, INPUT_PULLUP);
  
  // Initialize PWM
  ledcSetup(PWM_CHANNEL, PWM_FREQUENCY, PWM_RESOLUTION);
  ledcAttachPin(PIN_PWM_OUTPUT, PWM_CHANNEL);
  ledcWrite(PWM_CHANNEL, 0);
  
  // Ensure motor is stopped
  digitalWrite(PIN_PWM_ENABLE, LOW);
  digitalWrite(PIN_RELAY_LOCK, LOW);
  
  Serial.println("GPIO initialized");
  
  // Connect to WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
  
  // Setup MQTT
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setCallback(mqttCallback);
  
  Serial.println("Setup complete - ready!");
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  Serial.print("MQTT message [");
  Serial.print(topic);
  Serial.print("]: ");
  Serial.println(message);
  
  if (String(topic) == MQTT_TOPIC_CMD) {
    if (message == "open") {
      openGate();
    } else if (message == "close") {
      closeGate();
    } else if (message == "stop") {
      stopGate();
    }
  }
}

void reconnectMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("Connecting to MQTT...");
    if (mqttClient.connect(DEVICE_NAME, MQTT_USER, MQTT_PASSWORD)) {
      Serial.println("connected");
      mqttClient.subscribe(MQTT_TOPIC_CMD);
      publishState();
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" retry in 5s");
      delay(5000);
    }
  }
}

void publishState() {
  const char* stateStr;
  switch (currentState) {
    case GATE_OPEN: stateStr = "open"; break;
    case GATE_CLOSED: stateStr = "closed"; break;
    case GATE_OPENING: stateStr = "opening"; break;
    case GATE_CLOSING: stateStr = "closing"; break;
    case GATE_STOPPED: stateStr = "stopped"; break;
    case GATE_FAULT: stateStr = "fault"; break;
    default: stateStr = "unknown";
  }
  mqttClient.publish(MQTT_TOPIC_STATUS, stateStr, true);
}

void openGate() {
  if (digitalRead(PIN_LIMIT_OPEN) == LOW) {
    Serial.println("Gate already open");
    return;
  }
  
  Serial.println("Opening gate");
  currentState = GATE_OPENING;
  digitalWrite(PIN_DIRECTION, HIGH);
  digitalWrite(PIN_PWM_ENABLE, HIGH);
  ledcWrite(PWM_CHANNEL, MAX_PWM_DUTY);
  publishState();
}

void closeGate() {
  // Check motion sensor
  if (motionDetected && (millis() - motionDetectedTime < MOTION_BLOCK_TIME)) {
    Serial.println("Motion detected - blocking close");
    return;
  }
  
  if (digitalRead(PIN_LIMIT_CLOSED) == LOW) {
    Serial.println("Gate already closed");
    return;
  }
  
  Serial.println("Closing gate");
  currentState = GATE_CLOSING;
  digitalWrite(PIN_DIRECTION, LOW);
  digitalWrite(PIN_PWM_ENABLE, HIGH);
  ledcWrite(PWM_CHANNEL, MAX_PWM_DUTY);
  publishState();
}

void stopGate() {
  Serial.println("Stopping gate");
  digitalWrite(PIN_PWM_ENABLE, LOW);
  ledcWrite(PWM_CHANNEL, 0);
  currentState = GATE_STOPPED;
  publishState();
}

void checkLimitSwitches() {
  static bool lastOpenState = HIGH;
  static bool lastClosedState = HIGH;
  
  bool openState = digitalRead(PIN_LIMIT_OPEN);
  bool closedState = digitalRead(PIN_LIMIT_CLOSED);
  
  // Gate reached open position
  if (openState == LOW && lastOpenState == HIGH && currentState == GATE_OPENING) {
    Serial.println("Gate fully open");
    stopGate();
    currentState = GATE_OPEN;
    publishState();
  }
  
  // Gate reached closed position
  if (closedState == LOW && lastClosedState == HIGH && currentState == GATE_CLOSING) {
    Serial.println("Gate fully closed");
    stopGate();
    currentState = GATE_CLOSED;
    digitalWrite(PIN_RELAY_LOCK, HIGH); // Engage lock
    publishState();
  }
  
  lastOpenState = openState;
  lastClosedState = closedState;
}

void checkMotionSensor() {
  bool motion = digitalRead(PIN_MOTION_SENSOR);
  if (motion && !motionDetected) {
    Serial.println("Motion detected!");
    motionDetected = true;
    motionDetectedTime = millis();
    mqttClient.publish(MQTT_TOPIC_MOTION, "true");
  } else if (!motion && motionDetected) {
    motionDetected = false;
    mqttClient.publish(MQTT_TOPIC_MOTION, "false");
  }
}

void loop() {
  // Maintain MQTT connection
  if (!mqttClient.connected()) {
    reconnectMQTT();
  }
  mqttClient.loop();
  
  // Check sensors
  checkLimitSwitches();
  checkMotionSensor();
  
  // TODO: Implement soft start/stop
  // TODO: Implement overcurrent protection
  // TODO: Implement heating control
  // TODO: Implement web server
  // TODO: Implement voltage/current monitoring
  
  delay(10);
}
