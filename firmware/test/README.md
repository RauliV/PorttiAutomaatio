# PWM Soft Start/Stop Testi

## 🎯 Tarkoitus
Testaa PWM-ramping logiikka LED:llä ennen oikean moottorin käyttöä.

## 🔌 Kytkentä

```
ESP32 GPIO 26 ──┬──[LED]──[220Ω]──GND
                │
                └── Pitkä jalka (anodi)
```

**Komponentit:**
- 1x LED (mikä tahansa väri)
- 1x 220Ω vastus
- 2x hyppylanka

## 📥 Lataus ESP32:lle

### Vaihtoehto A: PlatformIO
```bash
cd ~/PorttiAutomaatio/firmware
pio run -e pwm_test -t upload -t monitor
```

### Vaihtoehto B: Arduino IDE
1. Avaa `test/pwm_ramp_test.cpp`
2. Valitse **Tools → Board → ESP32 Dev Module**
3. Valitse **Tools → Port → /dev/cu.usbserial-XXX**
4. **Upload** (Ctrl+U)
5. Avaa **Serial Monitor** (115200 baud)

## 👁️ Mitä pitäisi näkyä

### LED:llä:
1. ✅ **Kirkastuu tasaisesti** 2 sekunnissa (ei nykimistä)
2. ✅ **Pysyy täydellä** 2 sekuntia
3. ✅ **Himmenee tasaisesti** 1 sekunnissa
4. ✅ **Paussi** 3 sekuntia
5. ↻ **Toista**

### Serial Monitor:llä:
```
========================================
PWM Soft Start/Stop LED-testi
========================================

✅ PWM konfiguroitu:
   GPIO: 26
   Taajuus: 5000 Hz
   Resoluutio: 8 bit (0-255)

╔════════════════════════════════════════╗
║       UUSI TESTI-SYKLI                ║
╚════════════════════════════════════════╝

🚀 SOFT START:
PWM	Time(ms)	Progress
---	--------	--------
0	0		0.0%
5	40		10.0%
10	80		20.0%
...
255	2000		100.0%
✅ Saavutettu PWM: 255 (2000 ms)

⏸️  Pidetään täydellä kirkkaudella 2s...

🛑 SOFT STOP:
PWM	Time(ms)	Progress
---	--------	--------
255	0		0.0%
250	20		10.0%
...
0	1000		100.0%
✅ Pysäytetty (1000 ms)

💤 Paussi 3s ennen seuraavaa testiä...
```

## ✅ Onnistumiskriteerit

| Testi | Tavoite | Tulos |
|-------|---------|-------|
| **Kirkkaus kasvaa tasaisesti** | Ei nykimistä, sileä fade | ☐ |
| **Aika: 2000ms** | ±100ms | ☐ |
| **Täysi kirkkaus** | LED loistaa täydellä | ☐ |
| **Himmenee tasaisesti** | Sileä fade alas | ☐ |
| **Aika: 1000ms** | ±50ms | ☐ |
| **PWM telemetria** | Arvot 0→255→0 | ☐ |

## 🔧 Parametrien säätö

Muokkaa `pwm_ramp_test.cpp`:ssa:

```cpp
// Hitaampi ramping (sopii raskaammalle portille)
#define START_RAMP_TIME_MS 3000  // 3 sekuntia

// Nopeampi ramping (kevyelle portille)
#define START_RAMP_TIME_MS 1500  // 1.5 sekuntia

// Enemmän askeleita (sileämpi)
#define RAMP_STEPS 100

// Vähemmän askeleita (nykivämpi, mutta toimii)
#define RAMP_STEPS 25
```

## 🚀 Seuraavat vaiheet

Jos LED-testi onnistuu:
1. ✅ **Taso 2**: Pieni moottori (5A)
2. ✅ **Taso 3**: Vinssi penkillä (30A)
3. ✅ **Taso 4**: Oikea portti

## ⚠️ Troubleshooting

**LED ei pala:**
- Tarkista napaisuus (pitkä jalka → GPIO 26)
- Tarkista vastuksen arvo (100Ω-470Ω OK)
- Testaa LED: yhdistä suoraan 3.3V → vastus → GND

**LED vilkkuu, ei fade:**
- PWM-taajuus liian alhainen → nosta 10-20 kHz
- PWM-resoluutio väärä → varmista 8-bit

**Serial ei näytä mitään:**
- Tarkista baud rate (115200)
- Reset ESP32 (EN-nappi)

## 📊 Tulokset

Kun testi valmis, täytä:
- **Päivä**: _______________
- **Ramp time sopiva**: ☐ Kyllä / ☐ Liian hidas / ☐ Liian nopea
- **Smoothness**: ☐ Sileä / ☐ Pieni nykiminen / ☐ Paljon nykimistä
- **Huomiot**: _______________________________________

---

**Valmis seuraavaan vaiheeseen?** → [Taso 2: Pieni moottori](../docs/testing_motor.md)
