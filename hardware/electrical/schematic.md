# Sähkökaavio - Portin automaatiojärjestelmä

## Yleiskuva

Järjestelmä koostuu kolmesta pääosasta:
1. **12V DC tehokisko** (akku → vinssi)
2. **Ohjauselektroniikka** (ESP32 + anturit)
3. **230V AC** (laturi + sulanapito)

---

## 1. Tehokisko (12V DC)

```
                    PÄÄSULAKE ANL 100A
                           │
    AKKU 12V               │         PÄÄKATKAISIN 100A
    40-70Ah                │                │
      (+)──────────────────┴────────────────┴─────┬────────────── +12V TEHOKISKO
                                                  │
                                                  ├─────────────────┐
                                                  │                 │
                                            [TVS: SM8S24A]          │
                                                  │                 │
      (-)─────────────────────────────────────────┴─────────────────┴─ GND TEHOKISKO
                                                  │                 │
                                                  │                 │
                    ┌───────────────────────────────┼─────────────────────┐
                    │                               │                     │
                    │                               │                     │
              ┌─────▼─────┐                   ┌─────▼─────┐       ┌──────▼──────┐
              │ PWM/H-SILTA│                   │  DC/DC    │       │ RELEKORTTI  │
              │  60A Cont  │                   │ 12V → 5V  │       │  12V Kelat  │
              │ 100A Peak  │                   │   3A      │       │  4-8 CH     │
              └─────┬─────┘                   └─────┬─────┘       └──────┬──────┘
                    │                               │                     │
                    │                               │              ┌──────┴──────┐
              ┌─────▼─────┐                   ┌─────▼─────┐       │             │
              │   VINSSI  │                   │   ESP32   │   Kanava 1-4:      │
              │ Biltema   │                   │  WROOM/   │   - Magneettilukko │
              │  15-510   │                   │  WROVER   │   - LED-valot      │
              └───────────┘                   └───────────┘   - Sulatusrele    │
                                                              - (vara)          │
                                                              └──────────────────┘

    Kaapelit:
    - Akku → Vinssi: 16mm² (AWG 6), punainen/musta
    - DC/DC: 2.5mm² riittää
    - Relekortti: 1.5mm² riittää
```

### Komponentit ja liitännät

| Komponentti | Tyyppi | Liitäntä | Kaapeli | Huom |
|-------------|--------|----------|---------|------|
| Akku | 12V 40-70Ah | M8 navat | 16mm² | Maadoitettu miinusnapa |
| Pääsulake | ANL 100A | Sulakepesä | 16mm² | Akun plusnavassa |
| Pääkatkaisin | 100A | Ruuviliittimet | 16mm² | Helposti saavutettava |
| PWM/H-silta | 60A/100A | Terminal blocks | 16mm² tulo, 16mm² lähtö | Jäähdytyslevy |
| DC/DC | 12V→5V 3A | Terminal/screw | 2.5mm² | Eristetty |
| TVS-diodi | SM8S24A | Moottorin navat | - | Ylijännitesuoja |

---

## 2. Ohjauselektroniikka (ESP32)

### GPIO-kytkennät

```
                                ESP32 DEV BOARD
                               ┌─────────────────┐
                               │                 │
    PWM/H-SILTA OHJAUS:        │  GPIO 25 (OUT) ─┼─→ PWM_ENABLE (H-silta)
                               │  GPIO 26 (OUT) ─┼─→ PWM_OUTPUT (PWM signaali)
                               │  GPIO 27 (OUT) ─┼─→ DIRECTION (suunta)
                               │                 │
    RAJAKYTKIMET:              │  GPIO 32 (IN)  ─┼─← LIMIT_OPEN (pull-up)
                               │  GPIO 33 (IN)  ─┼─← LIMIT_CLOSED (pull-up)
                               │                 │
    ANTURIT:                   │  GPIO 34 (IN)  ─┼─← MOTION_SENSOR
                               │  GPIO 35 (IN)  ─┼─← E_STOP (pull-up)
                               │                 │
    RELEET:                    │  GPIO 18 (OUT) ─┼─→ RELAY_LOCK
                               │  GPIO 19 (OUT) ─┼─→ RELAY_HEATER
                               │  GPIO 23 (OUT) ─┼─→ MOSFET_LIGHTS (PWM)
                               │                 │
    ADC (MITTAUKSET):          │  GPIO 36 (ADC) ─┼─← VOLTAGE_SENSE
                               │  GPIO 39 (ADC) ─┼─← CURRENT_SENSE
                               │  GPIO 4  (ADC) ─┼─← TEMP_HEATSINK
                               │                 │
    VIRTA:                     │  5V            ─┼─← DC/DC muunnin
                               │  GND           ─┼─← Ohjausmaa (tähtipiste)
                               └─────────────────┘
```

### Rajakytkin-kytkentä (tyypillinen)

```
    +12V ───┬────┬──────────────┐
            │    │              │
           [R1] [R2]            │
           10k  10k             │
            │    │              │
            │    │              │
        ESP32   ESP32       RAJAKYTKIN
        GP32    GP33        (NC tai NO)
         │       │              │
         └───────┴──────────────┴─── GND

    R1, R2 = 10kΩ pull-up (sisäinen tai ulkoinen)
    Ferriitti helmi signaalijohdossa
    Debounce ohjelmallisesti (50ms)
```

### Liikkeentunnistin (PIR/Tutka)

```
    PIR/TUTKA MODUULI
    ┌─────────────┐
    │ VCC  (5-12V)├──── +12V (tai +5V jos PIR vaatii)
    │ OUT         ├──── ESP32 GPIO 34
    │ GND         ├──── GND
    └─────────────┘
    
    Jos 24GHz tutka:
    - RCWL-0516 tai vastaava
    - 4-28V syöttö
    - 3.3V TTL output → suoraan ESP32:een
```

### MOSFET-kytkentä (LED-valot)

```
                    MOSFET (IRLZ44N tai IRF540)
                         ┌───┐
    ESP32 GP23 ─[R 1kΩ]──┤ G │
                         │   │
    +12V ────────────────┤ D ├──┬──[LED-valonauhaa]──┐
                         │   │  │                    │
                         │ S ├──┴────────────────────┴── GND
                         └───┘
    
    Diodi D-S napojen väliin (valinnainen)
    PWM-taajuus: 1-5 kHz himmennettäville LEDeille
```

### Relekortti (4-8 kanavaa)

```
    OPTOERISTETTY RELEKORTTI
    ┌─────────────────────────┐
    │ VCC (+12V)              │──── +12V
    │ GND                     │──── GND
    │                         │
    │ IN1 (Lukko)             │──── ESP32 GPIO 18
    │ IN2 (Sulatus)           │──── ESP32 GPIO 19
    │ IN3 (vara)              │──── ESP32 GPIO xx
    │ IN4 (vara)              │──── ESP32 GPIO xx
    │                         │
    │ COM1 ────┐              │
    │ NO1      │ Lukko 12V    │──── Magneettilukko (+)
    │          │              │
    │ COM2 ────┐              │
    │ NO2      │ Sulatus 230V │──── Sulanapitovastus (L)
    └─────────────────────────┘
```

### Jännite/Virta-anturit

```
    JÄNNITTEEN MITTAUS (0-20V → 0-3.3V):
    
    +12V ──[R1: 27kΩ]──┬──[R2: 10kΩ]── GND
                       │
                       └─── ESP32 GPIO 36 (ADC)
    
    Jakosuhde: 3.3V / (12V * 10/(27+10)) ≈ 0.91
    
    
    VIRRAN MITTAUS (ACS712 tai INA219):
    
    ACS712-30A:
    ┌─────────────┐
    │ VCC (5V)    │──── +5V (DC/DC:stä)
    │ GND         │──── GND
    │ OUT         │──── ESP32 GPIO 39 (ADC)
    │ IP+ IP-     │──── Sarjaan tehokiskoon
    └─────────────┘
    
    Sensitivity: 66mV/A (30A versio)
    Offset: 2.5V (0A)
```

---

## 3. 230V AC -järjestelmä

```
    230V AC VERKKOVIRTA
         L ────┬────────────────────────────────┬─────────────────────────┐
               │                                │                         │
               │                           ┌────▼────┐               ┌────▼────┐
         N ────┼───────────────────────────┤  RCD    ├───────────────┤  RCD    │
               │                           │  30mA   │               │  30mA   │
               │                           └────┬────┘               └────┬────┘
         PE ───┼────────────────────────────────┼─────────────────────────┼─────
               │                                │                         │
               │                           ┌────▼────┐               ┌────▼────┐
               │                           │ LATURI  │               │  RELE   │
               │                           │ 230V AC │               │  230V   │
               │                           │   ↓     │               └────┬────┘
               │                           │ 12V DC  │                    │
               │                           └────┬────┘              ESP32 GPIO 19
               │                                │                    ohjaus
               │                                │                         │
               └───────────────────────────→ AKKU               ┌─────────▼──────────┐
                                              12V               │ SULANAPITOVASTUS   │
                                                                │  230V 20-30W/m    │
                                                                │  Alumiinikiskossa  │
                                                                └────────────────────┘
                                                                        │
                                                                  [Termostaatti]
                                                                   -5...+10°C
                                                                        │
                                                                       PE
```

### 230V Turvallisuus

| Komponentti | Arvo | Tarkoitus |
|-------------|------|-----------|
| RCD (laturi) | 30mA | Vikavirtasuoja laturille |
| RCD (sulatus) | 30mA | Vikavirtasuoja vastukselle |
| Maadoitus | PE | Kaikki metallikoterot |
| Sulake | 10A | Sulanapitovastuksen suojaus |
| Termostaatti | -5...+10°C | Aktivoi kun kylmä |

---

## 4. Kaapelointi ja värikoodit

### 12V DC Tehokisko

| Reitti | Kaapeli | Väri | Pituus (arvio) | Liittimet |
|--------|---------|------|----------------|-----------|
| Akku(+) → Sulake | 16mm² | Punainen | 0.3m | M8 kenkä + ANL |
| Sulake → Katkaisin | 16mm² | Punainen | 0.5m | ANL + ruuvi |
| Katkaisin → PWM | 16mm² | Punainen | 1.0m | Ruuvi + terminal |
| PWM → Vinssi (+) | 16mm² | Punainen | 2.0m | Terminal + puristus |
| Akku(-) → GND kisko | 16mm² | Musta | 0.3m | M8 kenkä |
| GND → Vinssi (-) | 16mm² | Musta | 2.0m | Terminal + puristus |
| +12V → DC/DC | 2.5mm² | Punainen | 0.5m | Terminal |
| GND → DC/DC | 2.5mm² | Musta | 0.5m | Terminal |
| +12V → Releet | 2.5mm² | Punainen | 0.5m | Terminal |

### Ohjauskaapelit (ESP32)

| Signaali | Kaapeli | Väri | Pituus | Huom |
|----------|---------|------|--------|------|
| PWM → H-silta | 0.5mm² | Keltainen | 1.0m | Suojattu kaapeli |
| Direction → H-silta | 0.5mm² | Sininen | 1.0m | Suojattu |
| Enable → H-silta | 0.5mm² | Vihreä | 1.0m | Suojattu |
| Rajakytkin Open | 0.5mm² | Valk/Sin | 3.0m | Cat5e/6 |
| Rajakytkin Close | 0.5mm² | Valk/Ora | 3.0m | Cat5e/6 |
| Motion Sensor | 0.5mm² | Valk/Vih | 2.0m | Cat5e/6 |
| E-Stop | 0.5mm² | Punainen | 1.0m | Paksu |

### 230V AC

| Reitti | Kaapeli | Väri | Huom |
|--------|---------|------|------|
| Verkko → RCD | 3×1.5mm² | L:Rusk, N:Sin, PE:Vih/Kelt | Kiinteä asennus |
| RCD → Laturi | 3×1.5mm² | L:Rusk, N:Sin, PE:Vih/Kelt | - |
| RCD → Rele | 3×1.5mm² | L:Rusk, N:Sin, PE:Vih/Kelt | - |
| Rele → Vastus | 3×1.5mm² | L:Rusk, N:Sin, PE:Vih/Kelt | Ulkoasennus |

---

## 5. Komponenttiluettelo ostoksiin

### Tehosähkö

| # | Komponentti | Speksit | Kpl | Hinta (arvio) | Linkki/Myyjä |
|---|-------------|---------|-----|---------------|--------------|
| 1 | Akku | 12V 50Ah AGM | 1 | 150€ | Biltema/Motonet |
| 2 | Pääkatkaisin | 100A 12V | 1 | 20€ | eBay |
| 3 | ANL-sulake | 100A | 2 | 5€ | eBay |
| 4 | Sulakepesä | ANL-koko | 1 | 10€ | eBay |
| 5 | PWM/H-silta | 60A IBT-2 tai BTS7960 | 1 | 15-30€ | AliExpress |
| 6 | TVS-diodi | SM8S24A | 1 | 2€ | Mouser/Digikey |
| 7 | Kaapeli 16mm² | Punainen | 5m | 25€ | Wurth |
| 8 | Kaapeli 16mm² | Musta | 5m | 25€ | Wurth |
| 9 | Puristusliittimet | M8 kaapelikengät | 10 | 15€ | K-Rauta |

### Ohjaus

| # | Komponentti | Speksit | Kpl | Hinta (arvio) | Linkki/Myyjä |
|---|-------------|---------|-----|---------------|--------------|
| 10 | ESP32 | WROOM/WROVER Dev Board | 1 | 10€ | AliExpress |
| 11 | DC/DC | 12V→5V 3A eristetty | 1 | 8€ | AliExpress |
| 12 | Relekortti | 4CH 12V optoeristetty | 1 | 8€ | AliExpress |
| 13 | MOSFET | IRLZ44N tai IRF540 | 2 | 3€ | Partco |
| 14 | Rajakytkimet | IP67 mekaaninen rullavarsi | 2 | 20€ | AliExpress |
| 15 | Liikkeentunnistin | RCWL-0516 (24GHz) | 1 | 3€ | AliExpress |
| 16 | Magneettilukko | 12V 180kg | 1 | 25€ | AliExpress |
| 17 | Virta-anturi | ACS712-30A | 1 | 5€ | AliExpress |
| 18 | Cat6 kaapeli | Ulkokäyttö | 20m | 15€ | K-Rauta |

### 230V AC

| # | Komponentti | Speksit | Kpl | Hinta (arvio) | Linkki/Myyjä |
|---|-------------|---------|-----|---------------|--------------|
| 19 | Laturi | 230V AC → 12V DC 5A | 1 | 40€ | Biltema |
| 20 | RCD | 30mA 16A | 2 | 60€ | Sähköliike |
| 21 | Sulanapitovastus | 230V 25W/m | 5m | 50€ | Sähköliike |
| 22 | Termostaatti | -5...+10°C | 1 | 25€ | AliExpress |
| 23 | Rele 230V | 16A kelalla 12V | 1 | 8€ | AliExpress |
| 24 | Kaapeli 3×1.5mm² | Ulkokäyttö | 20m | 40€ | K-Rauta |

**Yhteensä arvio**: ~570€ + Vinssi (~100€) + LED-valot (~30€) = **~700€**

---

## 6. Testausjärjestys

### Vaihe 1: Tehokisko (ilman moottoria)

1. Kytke akku, sulake, katkaisin
2. Mittaa jännite kiskossa: 12.0-13.8V
3. Kytke DC/DC, mittaa 5V
4. Testaa relekortti: click-ääni

### Vaihe 2: ESP32 ohjaus

1. Syötä 5V ESP32:lle
2. Flashaa firmware
3. Testaa GPIO:t LED:llä
4. Testaa WiFi/MQTT

### Vaihe 3: Anturit

1. Testaa rajakytkimet: Serial Monitor
2. Testaa liikkeentunnistin: Serial Monitor
3. Testaa jännite/virta-anturit: Serial Monitor

### Vaihe 4: Vinssi (tyhjäkäynti)

1. Kytke vinssi ILMAN KUORMAA
2. Testaa suunta molempiin suuntiin
3. Mittaa virta: <5A tyhjänä
4. Testaa soft start/stop

### Vaihe 5: Vinssi kuormitettuna

1. Lisää kevyt kuorma (10-20kg)
2. Testaa täysi aukiaulo
3. Mittaa virta: 20-40A kuormalla
4. Testaa rajakytkimien pysäytys

### Vaihe 6: Integraatio

1. Testaa MQTT-komennot
2. Testaa liikkeentunnistimen esto
3. Testaa E-stop
4. Testaa ylikuormasuoja

---

## 7. Turvallisuustarkistus

- [ ] E-stop katkaisee virran välittömästi
- [ ] Rajakytkimet estävät yliajon
- [ ] Ylikuormasuoja toimii (>100A)
- [ ] Liikkeentunnistin estää sulkemisen
- [ ] Magneettilukko fail-safe (auki vain komennolla)
- [ ] RCD:t testattu (test-nappi)
- [ ] Kaikki 230V kotelot maadoitettu
- [ ] Kaapelit kiinnitetty, ei kiristystä
- [ ] TVS-diodit asennettu
- [ ] Eristysv astuus >1MΩ (230V osat)

---

**Versio**: 1.0  
**Päivitetty**: 2025-12-19  
**Laatija**: Rauli Virtanen

