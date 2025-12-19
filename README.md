# Portin automaatiojärjestelmä

Kattava ratkaisu automaattiseen portinohjaukseen ESP32-mikrokontrollerilla, 12V vinssillä ja täydellä integraatiolla kameravalvontaan.

## 📁 Projektirakenne

```
PorttiAutomaatio/
├── docs/                      # Dokumentaatio
│   ├── mekaniikka.md         # Mekaaninen ja sähköinen dokumentaatio
│   └── readme.md             # Fusion 360 AddIn ohje
├── hardware/                  # Laitteistomäärittelyt
│   ├── mechanical/           # 3D-mallit (STEP, STL)
│   └── electrical/           # Sähkökaaviot
├── firmware/                  # ESP32 firmware
│   ├── src/                  # Lähdekoodit
│   ├── include/              # Header-tiedostot
│   ├── lib/                  # Kirjastot
│   └── platformio.ini        # PlatformIO config
├── fusion360-addon/          # Komponenttien layout-generaattori
│   ├── PorttiKomponentit.py  # Fusion 360 Python API script
│   ├── layout_config.json    # Komponenttimäärittelyt
│   └── manifest.json         # AddIn metadata
└── README.md                 # Tämä tiedosto
```

## 🎯 Ominaisuudet

### Laitteisto
- **Voimansiirto**: 12V DC akku, 80-100A pääsulake, 60A PWM/H-silta
- **Vinssi**: Biltema 15-510 + ketjupyörä + ~2.7m ANSI 40 ketju
- **Ohjaus**: ESP32 (WiFi/MQTT), relekortti, MOSFET-valot
- **Anturit**: Rajakytkimet (IP67), PIR/24GHz liikkeentunnistin
- **Turvallisuus**: Magneettilukko 180kg, RCD-suoja, E-stop
- **Sulanpito**: 230V AC kiskokaapeli, termostaatti-ohjattu

### Ohjelmisto
- **Web-käyttöliittymä**: Selainpohjainen ohjaus
- **MQTT-integraatio**: Home Assistant / ZoneMinder -yhteensopiva
- **HTTP API**: RESTful rajapinta
- **Soft start/stop**: PWM-ramppaus, ylikuormasuojaus
- **Talviprofiili**: Automaattinen sulanpito, jään ravistus

## 🚀 Pika-aloitus

### 1. Laitteiston asennus

Katso yksityiskohtaiset ohjeet: [docs/mekaniikka.md](docs/mekaniikka.md)

**Tl;dr:**
1. Asenna tehokisko: Akku → Pääsulake → PWM/H-silta → Vinssi
2. Kytke ESP32 ja anturit
3. Asenna ketju, kiristin ja rajakytkimet
4. Kytke 230V laturi ja sulanapitovastus

### 2. Firmware

```bash
cd firmware
# Asenna PlatformIO Core (jos ei ole)
pip install platformio

# Konfiguroi WiFi
cp src/config.example.h src/config.h
nano src/config.h  # Aseta WiFi-asetukset

# Buildaa ja flashaa
pio run -t upload
pio device monitor  # Seuraa debug-outputtia
```

### 3. Fusion 360 Layout Generator

**Asennus:**
1. Avaa Fusion 360
2. Scripts and Add-Ins → Add-Ins → vihreä + -painike
3. Valitse `fusion360-addon` -kansio
4. Suorita "PorttiKomponentit"

**Käyttö:**
- Generoi komponenttilayout testauslevylle
- Muokkaa `layout_config.json` muuttaaksesi komponenttien paikkoja
- Käytä layouttia komponenttien sijoitteluun

## 🔌 API-dokumentaatio

### HTTP-rajapinta

```bash
# Avaa portti
curl -X POST http://esp32-ip/open

# Sulje portti
curl -X POST http://esp32-ip/close

# Hae tila
curl http://esp32-ip/status
```

### MQTT

**Komennot** (publish → `gate/cmd`):
```
open    # Avaa portti
close   # Sulje portti
stop    # Pysäytä välittömästi
```

**Tila** (subscribe ← `gate/status`):
```
open     # Täysin auki
closed   # Täysin kiinni
opening  # Aukeamassa
closing  # Sulkeutumassa
stopped  # Pysäytetty
fault    # Vikatila
```

**Anturit**:
- `gate/sensor/motion` - Liikkeentunnistin (true/false)
- `gate/sensor/limit_open` - Auki-rajapääte (true/false)
- `gate/sensor/limit_closed` - Kiinni-rajapääte (true/false)
- `gate/power/voltage` - Akkujännite (V)
- `gate/power/current` - Virta (A)

## 🔐 Turvallisuus

**Pakolliset toiminnot:**
- ✅ E-stop katkaisee virran välittömästi
- ✅ Rajakytkimet estävät yliajon
- ✅ Liikkeentunnistin estää sulkemisen
- ✅ Ylikuormasuoja (>100A → katkaisu)
- ✅ Fail-safe lukitus (auki vain komennolla)
- ✅ Soft start/stop (estää kuormituspiikit)

## 📊 Komponentit

Katso täydellinen lista: [docs/mekaniikka.md](docs/mekaniikka.md#komponenttilista)

**Pääkomponentit:**
- Akku: 12V AGM/Gel 40-70Ah
- PWM/H-silta: 60A jatkuva, 100A peak
- ESP32: WROOM/WROVER dev board
- Ketju: ANSI 40/ISO 08B, 2670mm
- Magneettilukko: 12V DC, ≥180kg

## 🛠️ Kehitys

### Projektin kloonaus ja kehitysympäristö

```bash
git clone https://github.com/[username]/PorttiAutomaatio.git
cd PorttiAutomaatio

# ESP32 firmware
cd firmware
pio run

# Fusion 360 AddIn
# Kopioi fusion360-addon/ Fusion 360 AddIns-kansioon
```

### Testaus

```bash
# ESP32 unit testit
cd firmware
pio test

# Integration testit (vaatii laitteiston)
pio test -e integration
```

## 📝 Lisenssi

MIT License - vapaa käyttöön, muokkaukseen ja jakeluun.

## 👤 Tekijä

**Rauli Virtanen**

- GitHub: [@raulivirtanen](https://github.com/raulivirtanen)
- Projekti: [PorttiAutomaatio](https://github.com/raulivirtanen/PorttiAutomaatio)

## 🤝 Osallistuminen

Pull requestit tervetulleita! Isommille muutoksille avaa ensin issue keskustellaksesi muutoksesta.

## 📚 Lisädokumentaatio

- [Mekaaninen ja sähköinen dokumentaatio](docs/mekaniikka.md)
- [Fusion 360 AddIn käyttöohje](docs/readme.md)
- [API-referenssi](docs/api.md) *(tulossa)*
- [Vianmääritys](docs/mekaniikka.md#vianhaku)

---

**Versio**: 1.0.0  
**Päivitetty**: 2025-12-19
