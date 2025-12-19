#ifndef CONFIG_H
#define CONFIG_H

// WiFi Configuration
#define WIFI_SSID "YourWiFiNetwork"
#define WIFI_PASSWORD "YourWiFiPassword"

// MQTT Configuration
#define MQTT_BROKER "192.168.1.10"
#define MQTT_PORT 1883
#define MQTT_USER "your_mqtt_user"      // Leave empty if no auth
#define MQTT_PASSWORD "your_mqtt_pass"  // Leave empty if no auth

// MQTT Topics
#define MQTT_TOPIC_CMD "gate/cmd"
#define MQTT_TOPIC_STATUS "gate/status"
#define MQTT_TOPIC_MOTION "gate/sensor/motion"
#define MQTT_TOPIC_LIMIT_OPEN "gate/sensor/limit_open"
#define MQTT_TOPIC_LIMIT_CLOSED "gate/sensor/limit_closed"
#define MQTT_TOPIC_VOLTAGE "gate/power/voltage"
#define MQTT_TOPIC_CURRENT "gate/power/current"

// GPIO Pin Configuration
#define PIN_PWM_ENABLE 25        // PWM/H-bridge enable
#define PIN_PWM_OUTPUT 26        // PWM output to motor controller
#define PIN_DIRECTION 27         // Motor direction
#define PIN_LIMIT_OPEN 32        // Limit switch - gate fully open
#define PIN_LIMIT_CLOSED 33      // Limit switch - gate fully closed
#define PIN_MOTION_SENSOR 34     // Motion sensor (PIR/radar)
#define PIN_ESTOP 35             // Emergency stop button
#define PIN_RELAY_LOCK 18        // Magnetic lock relay
#define PIN_RELAY_HEATER 19      // Heating cable relay
#define PIN_MOSFET_LIGHTS 23     // LED lights PWM
#define PIN_VOLTAGE_SENSE 36     // Battery voltage sense (ADC)
#define PIN_CURRENT_SENSE 39     // Current sense (ADC)
#define PIN_TEMP_HEATSINK 4      // Temperature sensor (OneWire/analog)

// Motor Control Settings
#define PWM_FREQUENCY 15000      // 15 kHz PWM frequency
#define PWM_RESOLUTION 8         // 8-bit resolution (0-255)
#define PWM_CHANNEL 0            // PWM channel
#define SOFT_START_DURATION 2000 // Soft start ramp duration (ms)
#define SOFT_STOP_DURATION 1500  // Soft stop ramp duration (ms)
#define MAX_PWM_DUTY 255         // Maximum PWM duty cycle
#define MIN_PWM_DUTY 100         // Minimum PWM to overcome friction

// Safety Settings
#define MAX_CURRENT_AMPS 100.0   // Maximum current before shutdown
#define OVERCURRENT_DELAY 2000   // Time above max current before shutdown (ms)
#define MOTION_BLOCK_TIME 5000   // Block closing for 5s after motion detected
#define DEBOUNCE_TIME 50         // Button debounce time (ms)
#define GATE_TIMEOUT 60000       // Max time for full open/close cycle (ms)

// Heating Settings
#define HEATER_ENABLE_TEMP 5.0   // Enable heating below this temp (°C)
#define HEATER_DISABLE_TEMP 10.0 // Disable heating above this temp (°C)

// Web Server
#define WEB_SERVER_PORT 80

// Device Name
#define DEVICE_NAME "GateController"
#define DEVICE_VERSION "1.0.0"

// Debug Settings
#define DEBUG_SERIAL true
#define DEBUG_VERBOSE false

#endif // CONFIG_H
