/*
 * PWM Soft Start/Stop LED-testi
 * 
 * Testaa PWM-ramping logiikkaa LED:llä ennen oikean moottorin käyttöä
 * 
 * Kytkentä:
 * - LED pitkä jalka → ESP32 GPIO 26 (PWM_OUTPUT)
 * - LED lyhyt jalka → 220Ω vastus → GND
 * 
 * Testaa:
 * 1. LED kirkastuu tasaisesti 2 sekunnissa (soft start)
 * 2. LED pysyy täydellä kirkkaudella 2 sekuntia
 * 3. LED himmenee tasaisesti 1 sekunnissa (soft stop)
 * 4. Toista loputtomiin
 * 
 * Seuraa Serial Monitor (115200 baud) telemetriaa
 */

#include <Arduino.h>

// GPIO-määritykset (samat kuin oikeassa firmwaressa)
#define PWM_OUTPUT 26
#define PWM_FREQ 5000        // 5 kHz PWM-taajuus
#define PWM_CHANNEL 0
#define PWM_RESOLUTION 8     // 8-bit = 0-255

// Ramping-parametrit
#define RAMP_STEPS 50
#define START_RAMP_TIME_MS 2000  // 2 sekuntia 0→100%
#define STOP_RAMP_TIME_MS 1000   // 1 sekunti 100%→0%

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("========================================");
  Serial.println("PWM Soft Start/Stop LED-testi");
  Serial.println("========================================");
  Serial.println();
  
  // Konfiguroi PWM (ESP32 LEDC)
  ledcSetup(PWM_CHANNEL, PWM_FREQ, PWM_RESOLUTION);
  ledcAttachPin(PWM_OUTPUT, PWM_CHANNEL);
  ledcWrite(PWM_CHANNEL, 0);  // Aloita pimeänä
  
  Serial.println("✅ PWM konfiguroitu:");
  Serial.print("   GPIO: ");
  Serial.println(PWM_OUTPUT);
  Serial.print("   Taajuus: ");
  Serial.print(PWM_FREQ);
  Serial.println(" Hz");
  Serial.print("   Resoluutio: ");
  Serial.print(PWM_RESOLUTION);
  Serial.println(" bit (0-255)");
  Serial.println();
}

void softStartLED(int targetSpeed, int rampTimeMs) {
  Serial.println("🚀 SOFT START:");
  Serial.println("PWM\tTime(ms)\tProgress");
  Serial.println("---\t--------\t--------");
  
  unsigned long startTime = millis();
  int delayPerStep = rampTimeMs / RAMP_STEPS;
  
  for (int i = 0; i <= RAMP_STEPS; i++) {
    int pwm = (targetSpeed * i) / RAMP_STEPS;
    ledcWrite(PWM_CHANNEL, pwm);
    
    // Telemetria
    unsigned long elapsed = millis() - startTime;
    float progress = (float)i / RAMP_STEPS * 100.0;
    
    Serial.print(pwm);
    Serial.print("\t");
    Serial.print(elapsed);
    Serial.print("\t\t");
    Serial.print(progress, 1);
    Serial.println("%");
    
    delay(delayPerStep);
  }
  
  Serial.print("✅ Saavutettu PWM: ");
  Serial.print(targetSpeed);
  Serial.print(" (");
  Serial.print(millis() - startTime);
  Serial.println(" ms)");
  Serial.println();
}

void softStopLED(int currentSpeed, int rampTimeMs) {
  Serial.println("🛑 SOFT STOP:");
  Serial.println("PWM\tTime(ms)\tProgress");
  Serial.println("---\t--------\t--------");
  
  unsigned long startTime = millis();
  int delayPerStep = rampTimeMs / RAMP_STEPS;
  
  for (int i = RAMP_STEPS; i >= 0; i--) {
    int pwm = (currentSpeed * i) / RAMP_STEPS;
    ledcWrite(PWM_CHANNEL, pwm);
    
    // Telemetria
    unsigned long elapsed = millis() - startTime;
    float progress = (float)(RAMP_STEPS - i) / RAMP_STEPS * 100.0;
    
    Serial.print(pwm);
    Serial.print("\t");
    Serial.print(elapsed);
    Serial.print("\t\t");
    Serial.print(progress, 1);
    Serial.println("%");
    
    delay(delayPerStep);
  }
  
  Serial.print("✅ Pysäytetty (");
  Serial.print(millis() - startTime);
  Serial.println(" ms)");
  Serial.println();
}

void loop() {
  // Testi-sykli
  Serial.println("╔════════════════════════════════════════╗");
  Serial.println("║       UUSI TESTI-SYKLI                ║");
  Serial.println("╚════════════════════════════════════════╝");
  Serial.println();
  
  // 1. Soft start 0 → 255 (2 sekuntia)
  softStartLED(255, START_RAMP_TIME_MS);
  
  // 2. Pidä täydellä 2 sekuntia
  Serial.println("⏸️  Pidetään täydellä kirkkaudella 2s...");
  delay(2000);
  Serial.println();
  
  // 3. Soft stop 255 → 0 (1 sekunti)
  softStopLED(255, STOP_RAMP_TIME_MS);
  
  // 4. Paussi 3 sekuntia ennen seuraavaa
  Serial.println("💤 Paussi 3s ennen seuraavaa testiä...");
  Serial.println();
  delay(3000);
}
