# KiCad Sähkökaaviot - PorttiAutomaatio

Yksityiskohtaiset sähkökaaviot portin automaatiojärjestelmälle.

## 📁 Rakenne

```
kicad/
├── PorttiAutomaatio.kicad_pro    # Projektitiedosto
├── PorttiAutomaatio.kicad_sch    # Pääarkki (hierarkia)
├── 230v_ac.kicad_sch             # 230V AC järjestelmä
├── 12v_dc.kicad_sch              # 12V DC tehokisko
├── esp32_control.kicad_sch       # ESP32 ohjaus
├── export_schematics.py          # PDF-vienti skripti
├── exports/                      # Viedyt PDF:t
└── README.md                     # Tämä tiedosto
```

## 🚀 Pika-aloitus

### 1. Avaa projekti KiCadissa

```bash
# macOS:
open -a KiCad PorttiAutomaatio.kicad_pro

# tai käynnistä KiCad ja File → Open Project
```

### 2. Navigoi arkkien välillä

- **Pääarkki**: Näyttää hierarkian (3 aliarkkia)
- **230V AC**: Laturi, RCD, sulanapito
- **12V DC**: Akku, PWM, vinssi, DC/DC
- **ESP32**: GPIO-kytkennät, anturit, releet

Klikkaa hierarkia-laatikoita päästäksesi aliarkkeille.

## 📝 Muokkaaminen

### Komponenttien lisääminen

1. Paina `A` (Add Symbol)
2. Etsi komponentti (esim. "ESP32", "Relay", "Fuse")
3. Sijoita kaaviolle
4. Paina `W` (Wire) vetääksesi kytkennät

### GPIO-taulukko (ESP32)

Kopioi tämä `esp32_control.kicad_sch` arkkiin:

| GPIO | Funktio | Suunta | Komponentti |
|------|---------|--------|-------------|
| 25 | PWM_ENABLE | OUT | H-silta |
| 26 | PWM_OUTPUT | OUT | H-silta |
| 27 | DIRECTION | OUT | H-silta |
| 32 | LIMIT_OPEN | IN | Rajakytkin |
| 33 | LIMIT_CLOSED | IN | Rajakytkin |
| 34 | MOTION_SENSOR | IN | PIR |
| 35 | E_STOP | IN | Hätäseis |
| 18 | RELAY_LOCK | OUT | Magneettilukko |
| 19 | RELAY_HEATER | OUT | Sulatusrele |
| 23 | MOSFET_LIGHTS | OUT | LED-valot |
| 36 | VOLTAGE_SENSE | ADC | Jännitemittaus |
| 39 | CURRENT_SENSE | ADC | Virran mittaus |
| 4 | TEMP_HEATSINK | ADC | Lämpömittaus |

## 📤 PDF-vienti

### Automaattinen (skripti)

```bash
cd ~/PorttiAutomaatio/hardware/electrical/kicad/
./export_schematics.py
```

**Tulokset**: `exports/` kansiossa
- `PorttiAutomaatio.pdf` (pääarkki)
- `230v_ac.pdf`
- `12v_dc.pdf`
- `esp32_control.pdf`
- `PorttiAutomaatio_complete.pdf` (kaikki yhdistettynä)

### Manuaalinen vienti

1. Avaa arkki KiCadissa
2. **File → Plot**
3. Valitse:
   - Output format: PDF
   - Output directory: `exports/`
   - ✅ Plot border and title block
4. **Plot All Pages**

## 🔧 Komponenttikirjastot

### Sisäänrakennetut (käytettävissä heti)

- `Device`: R, C, L, Fuse, Switch
- `Connector`: Terminal blocks, screw terminals
- `Relay`: Generic relays
- `Motor`: DC motors
- `power`: +12V, GND, +5V

### Lisättävät erikseen

**ESP32 Dev Board:**
```
Symbol Library Manager → Add →
https://github.com/espressif/kicad-libraries
```

**BTS7960 H-silta:**
Luo custom symboli tai käytä generic "Motor Driver"

## 📊 BOM (Bill of Materials) -vienti

```bash
# KiCad CLI:
kicad-cli sch export bom \
  --output exports/BOM.csv \
  PorttiAutomaatio.kicad_sch
```

Tai KiCad:ssa: **Tools → Generate BOM**

## 🔗 Linkit dokumentaatioon

- [schematic.md](../schematic.md) - ASCII-kaaviot ja tekniset tiedot
- [docs/mekaniikka.md](../../../docs/mekaniikka.md) - Asennusohjeet
- [Fusion 360 layout](../layouts/) - 3D komponenttisijoittelu

## 💡 Vinkit

### Nopeat näppäimet

- `A` - Add symbol
- `W` - Wire (johdin)
- `L` - Label (signaalinimi)
- `P` - Power symbol (+12V, GND)
- `M` - Move
- `C` - Copy
- `Del` - Delete
- `E` - Edit properties
- `R` - Rotate

### Parhaita käytäntöjä

1. **Käytä net labeleita**: Nimeä signaalit (esim. "PWM_OUT", "GND")
2. **Hierarkiset kytkennät**: Yhdistä arkit signaaleilla, ei viivoilla
3. **Kommenttitekstit**: Lisää selityksiä (Text tool)
4. **Komponenttiviitteet**: Numeroi johdonmukaisesti (F1, F2, U1, U2...)
5. **Electrical Rules Check**: Tools → ERC (tarkista virheet)

## 🐛 Vianetsintä

### "Symbol not found"
→ Symbol Library Manager: Lisää puuttuvat kirjastot

### "Hierarchical sheet not found"
→ Tarkista että aliarkkit ovat samassa kansiossa

### PDF-vienti ei toimi
→ Asenna KiCad uudelleen tai käytä Manual Plot

### Skripti ei löydä kicad-cli
→ Päivitä polku `export_schematics.py` tiedostossa

## 📞 Tuki

Ongelmia? Kysy:
- [KiCad Forum](https://forum.kicad.info/)
- [KiCad Documentation](https://docs.kicad.org/)

---

**Versio**: 1.0  
**Luotu**: 2025-12-19  
**Tekijä**: PorttiAutomaatio-projekti
