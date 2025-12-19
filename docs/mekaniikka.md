# Portin automaatiojärjestelmä - Mekaniikka ja sähköistys

## Yleiskuvaus

Automaattinen porttivinssijärjestelmä 12V DC -käyttöisellä vinssillä ja ESP32-pohjaisella ohjauksella. Järjestelmä sisältää verkkovirtalaturin, sulanpitovastuksen ja täyden integraation kameravalvontaan.

## Järjestelmäarkkitehtuuri

### Päätehonsyöttö (12V DC)
- **Akku**: 12V AGM/Gel, 40-70 Ah
- **Pääkatkaisin**: 12V 100A
- **Pääsulake**: ANL/MIDI 80-100A akun plusnavan lähellä
- **Ylläpitolaturi**: 230V AC → 12V DC, pitää akun varattuna

### Moottoriohjaus
- **PWM/H-silta**: 60A jatkuva, >100A hetkellinen
  - PWM-taajuus: 15-20 kHz
  - Ohjaus: ESP32 (ENA/PWM + DIR -signaalit)
- **TVS-diodi**: 24V bidirectional (SM8S24A) moottorin napojen yli
- **LC-suodatin**: 100µH + 470µF 25V PWM-syöttöön

### Vinssi ja mekaaniikka
- **Vinssi**: Biltema 15-510 (tai vastaava 1000-1500kg)
- **Ketjupyörä**: d=50-60mm, 12-15 hammasta, teräs, hitsattu vinssin ulostuloon
- **Ketju**: ANSI 40 / ISO 08B, ruostumaton/galvanoitu, ~2×1335mm
- **Kiristin**: Jousikuormitettu rulla, säätövara ±50mm
- **Laakerit**: 2× 6202-2RS ketjupyörälle
- **Suojaus**: Ketjukotelo, valutusreiät, tiivisteet

### Ohjaus ja anturit
- **ESP32**: WROOM/WROVER dev board
- **DC/DC-muunnin**: 12V→5V, 3A, eristetty
- **Relekortti**: 4-8 kanavaa, 12V kelat
  - Magneettilukko (12V DC, ≥180kg vetovoima)
  - LED-valot (12V, PWM-himmennys)
  - Sulanapitokaapelin ohjaus
- **MOSFET-kanavat**: 30A valoille ja lisäkuormille
- **Rajakytkimet**: 2kpl IP67 mekaaniset rullavarrella (auki/kiinni)
- **Liikkeentunnistin**: IP66 PIR tai 24GHz tutka, estää sulkemisen

### Sulanpito (230V AC)
- **Sulanapitovastus**: 20-30W/m kiskokaapeli
- **Ohjaus**: Termostaatti/NTC + rele
- **Suojaus**: RCD-vikavirtasuoja, maadoitus

## Komponenttilista

### Tehosähkö
| Komponentti | Tyyppi/Arvo | Määrä | Huomiot |
|-------------|-------------|-------|---------|
| Akku | 12V AGM/Gel 40-70Ah | 1 | Syväpurkaussuojalla |
| Pääkatkaisin | 100A 12V | 1 | Helposti saavutettava |
| Pääsulake | ANL/MIDI 80-100A | 1 | + sulakepesä |
| Vinsskaapelit | 16mm² (AWG 6) | 2×5m | Puristuskaapelikengät |
| H-silta/PWM | 60A cont, 100A peak | 1 | 12V DC moottoriohjain |
| TVS-diodi | SM8S24A (24V bidir) | 1 | Ylijännitesuoja |
| LC-suodatin | 100µH + 470µF 25V | 1 | PWM-häiriösuodatus |

### Ohjaus
| Komponentti | Tyyppi/Arvo | Määrä | Huomiot |
|-------------|-------------|-------|---------|
| ESP32 | WROOM/WROVER | 1 | Dev board |
| DC/DC-muunnin | 12V→5V 3A eristetty | 1 | ESP32:n syöttö |
| Relekortti | 4-8 kanavaa 12V | 1 | Optoeristetty |
| MOSFET-moduuli | 30A PWM | 1 | Valojen himmennys |
| Rajakytkimet | IP67 mekaaninen | 2 | Rullavarrella |
| Liikkeentunnistin | PIR/24GHz IP66 | 1 | Turvallisuus |
| Magneettilukko | 12V DC ≥180kg | 1 | + varmistusdiodi |
| LED-valot | 12V 20-60W total | n | Himmennettävät |

### Mekaniikka
| Komponentti | Tyyppi/Arvo | Määrä | Huomiot |
|-------------|-------------|-------|---------|
| Ketju | ANSI 40/ISO 08B | 2670mm | Ruostumaton/galvanoitu |
| Ketjupyörä | d=50-60mm, 12-15T | 1 | Teräs, hitsataan vinssiin |
| Kiristin | Jousikuormitettu | 1 | Säätövara ±50mm |
| Laakerit | 6202-2RS | 2 | + laakeripesät |
| Ketjukotelo | Alumiini/teräs | 1 | Valutusreiät |

### Verkko ja sulanpito
| Komponentti | Tyyppi/Arvo | Määrä | Huomiot |
|-------------|-------------|-------|---------|
| Sulanapitovastus | 230V 20-30W/m | ~5m | Alumiinikiskossa |
| Termostaatti/NTC | -5...+10°C | 1 | Ohjaussignaali ESP32:lle |
| RCD | 30mA | 1 | Vikavirtasuoja |
| Akkulaturi | 230V AC → 12V DC | 1 | Float-lataus |

## Sähköinen rakenne

### Virtareitit

```
230V AC:
Verkko → RCD → Laturi → 12V Akku
     → RCD → Rele → Sulanapitovastus

12V DC:
Akku(+) → Pääsulake → Pääkatkaisin → [Tehokisko]
                                     ├→ PWM/H-silta → Vinssi
                                     ├→ Relekortti → Lukko, Sulatus
                                     └→ DC/DC → ESP32 → Anturit

Ohjaussignaalit:
ESP32 → PWM/H-silta (ENA/PWM, DIR)
ESP32 → Relekortti (4-8 kanavaa)
ESP32 → MOSFET (PWM valoille)
Rajakytkimet → ESP32 (pull-up + debounce)
Liikkeentunnistin → ESP32
```

### Maadoitus ja häiriösuojaus
- **Tähtipiste**: Ohjausmaa yhdessä pisteessä
- **Ferriittihelmet**: Anturisignaaleissa
- **TVS + LC-suodatin**: PWM-häiriöiden minimoimiseksi
- **Optoeristys**: Relekortti ja moottoriohjain

## Mekaaninen rakenne

### Ketjuasennus

1. **Ketjupyörä vinssiin**:
   - Hitsaa ketjupyörä (d=50-60mm) vinssin ulostuloon
   - Varmista keskitys ja linjaus porttikiskon kanssa
   - Laakeroi tarvittaessa erilliselle akselille (vähentää sivuttaiskuormaa)

2. **Ketjureitti**:
   - Pituus: ~2×1335mm (2670mm yhteensä)
   - Kiinnitys porttiin: hitsatut/pultatut kiinnikkeet
   - Ohjainrullat kaarteissa: minimimutkasäde ≥10×ketjun pitch

3. **Kiristin**:
   - Jousikuormitettu rulla ketjun alaosaan
   - Säätövara: ±50mm
   - Oikea kireys: 10-20mm notkahdus keskeltä

4. **Suojaus**:
   - Ketjukotelo: estää takertuminen, suojaa säältä
   - Valutusreiät pohjassa
   - Tiivisteet läpivienneissä

### Toleranssit ja linjaus

- **Ketjupyörän keskolinjaus**: ±2mm
- **Ketjun sivuttaispoikkeama**: max 3mm
- **Kiristimen säätövara**: ±50mm
- **Laakerivälys**: 0.02-0.05mm

## Asennusohjeet (vaiheittain)

### 1. Sähköasennus

**Tehokisko ja suojat:**
```
1. Asenna pääkatkaisin akun läheisyyteen
2. Asenna pääsulake (80-100A) akun plusnavaan
3. Vedä 16mm² kaapelit vinssille (plus ja miinus erikseen)
4. Luo ohjausmaan tähtipiste
```

**PWM/H-silta:**
```
1. Kytke: Akku → Pääsulake → PWM-tulo
2. Kytke: PWM-lähtö → Vinssin moottori
3. Asenna TVS-diodi moottorin napojen yli
4. Asenna LC-suodatin PWM-syöttöön
5. Kytke ohjaussignaalit ESP32:sta (ENA/PWM, DIR)
```

**ESP32 ja apulaitteet:**
```
1. Syötä ESP32 eristetystä DC/DC-muuntimesta (12V→5V)
2. Kytke relekortti ESP32:een (4-8 kanavaa):
   - Kanava 1: Magneettilukko
   - Kanava 2-3: LED-valot (tai MOSFET)
   - Kanava 4: Sulanapitokaapelin ohjaus
3. Kytke H-sillan ohjaussignaalit (ENA/PWM, DIR) ESP32:lle
```

**Anturit:**
```
1. Asenna rajakytkimet portin auki/kiinni -päihin
2. Vedä anturijohdot ESP32:lle (pull-up + häiriösuodatus)
3. Asenna liikkeentunnistin portin edustalle
4. Testaa antureiden toiminta (debug-output ESP32:sta)
```

### 2. Mekaniikka-asennus

**Ketju ja pyörä:**
```
1. Hitsaa ketjupyörä vinssin ulostuloon
   - Varmista keskitys (max ±2mm)
   - Koelinjaa porttikiskon kanssa
2. Asenna ketju porttiin
   - Kiinnitä molempiin päihin
   - Tarkista hammas- ja ketjulinja
3. Asenna kiristin alaosaan
   - Jousikuormitus ~50N
   - Säädä kireys: 10-20mm notkahdus
4. Asenna ohjainrullat tarvittaessa
```

**Laakerointi (jos tarvitaan):**
```
1. Jos ketjupyörä erillisellä akselilla:
   - Käytä 6202-2RS laakereita (2 kpl)
   - Asenna laakeripesät tukevasti
   - Varmista oikea akseliväli
2. Testaa pyöriminen: kevyt, tasainen, ei sivuttaisliikettä
```

**Suojaus:**
```
1. Asenna ketjukotelo
   - Valutusreiät pohjassa
   - Huoltokansi tarkistuksille
2. Tiivistä läpiviennit
3. Maalaa/suojaa ruostumiselta
```

### 3. Sulanapitovastus (230V AC)

```
1. Asenna vastus alumiinikiskoon
2. Kytke ohjaus releelle (ESP32:n kautta)
3. Lisää termostaatti/NTC-anturi (-5...+10°C)
4. Asenna RCD-vikavirtasuoja (30mA)
5. Maadoita kaikki metallirakenteet
```

### 4. Ohjelmisto ja integraatio

**ESP32:**
```
1. Lataa firmware (web-UI + MQTT)
2. Konfiguroi WiFi ja MQTT-broker
3. Aseta rajakytkinlogiikka ja soft start/stop
4. Testaa käsin (debug-näyttö/seriaaliprintti)
```

**ZoneMinder/NVR-integraatio:**
```
1. Konfiguroi webhook/MQTT-triggerit
2. Testaa: kamera havaitsee liikkeen → ESP32 saa signaalin
3. Aseta authorized approach -logiikka
```

**MQTT-julkaisu:**
```
Topics:
- gate/cmd: open|close|stop
- gate/status: open|closed|stopped|fault|moving
- gate/sensor/motion: true|false
- gate/sensor/limit_open: true|false
- gate/sensor/limit_closed: true|false
```

### 5. Testaus

**Kuivaharjoittelu (ilman kuormaa):**
```
1. Soft start/stop PWM:llä
2. Rajakytkimien toiminta
3. Hätäpysäytys
4. Liikkeentunnistimen esto
```

**Kuormitettu testaus:**
```
1. Mittaa virta (pitää olla <60A jatkuvasti)
2. Tarkista jännitehäviö kaapeleissa (<0.5V)
3. Seuraa lämpötiloja (H-silta, kaapelit)
4. Testaa täysi aukiaulo-sulkusykli
```

**Talviprofiili:**
```
1. Aktivoi sulanapitovastus automaattisesti (<+5°C)
2. Testaa jään ravistus (pieni edestakainen liike)
3. Varmista lukituksen toiminta pakkasella
```

## Turvallisuus

### Pakollliset turvaominaisuudet

1. **E-stop**: Hätäpysäytyspainike, katkaisee virran H-sillalta
2. **Rajakytkimet sarjaan**: Estävät yliajon
3. **Fail-safe lukitus**: Lukko kiinni ellei avauskomento aktiivinen
4. **Ylikuormituksen katkaisu**: >100A katkaisu 2s viiveellä
5. **Liikkeentunnistin**: Estää sulkemisen jos liikettä havaitaan
6. **RCD-suoja**: Sulanapitokaapelille (230V AC)
7. **Soft start/stop**: Estää äkilliset kuormituspiikit

### Huolto-ohjeet

**Viikoittain:**
- Tarkista portin toiminta silmämääräisesti
- Kuuntele epänormaalit äänet

**Kuukausittain:**
- Tarkista ketjun kireys ja voitelu
- Puhdista anturit
- Testaa rajakytkimet ja liikkeentunnistin

**Vuosittain:**
- Tarkista kaikki liitokset ja kiristykset
- Mittaa eristysvastuks (>1MΩ)
- Huolla laakerit
- Vaihda kuluneet ketjun osat

## Vianhaku

| Oire | Mahdollinen syy | Korjaus |
|------|----------------|---------|
| Vinssi ei käynnisty | Pääsulake palanut | Vaihda sulake, tutki ylikuorma |
| | Rajakytkin aktiivinen | Tarkista rajakytkimien tila |
| | ESP32 offline | Tarkista WiFi, käynnistä uudelleen |
| Vinssi toimii hitaasti | Akku heikko | Lataa akku, tarkista laturi |
| | Ketju liian kireällä | Löysää kiristintä |
| Ketju hyppää | Liian löysä | Kiristä kiristintä |
| | Kuluneet hampaat | Vaihda ketjupyörä |
| Sulanapito ei toimi | Rele rikki | Vaihda rele |
| | Termostaatti jumissa | Testaa/vaihda termostaatti |
| | RCD lauennut | Tutki maavuoto, nollaa RCD |

## API-dokumentaatio

### HTTP-rajapinta

```
GET  /status          - Portin tila
POST /open            - Avaa portti
POST /close           - Sulje portti
POST /stop            - Pysäytä liike
GET  /sensors         - Kaikkien antureiden tila
POST /light/{0-100}   - Aseta valojen kirkkaus (PWM)
```

### MQTT-viestit

**Komennot (subscribe: gate/cmd):**
```
open   - Avaa portti
close  - Sulje portti
stop   - Pysäytä välittömästi
```

**Tila (publish: gate/status):**
```
open     - Portti täysin auki
closed   - Portti täysin kiinni
opening  - Aukeamassa
closing  - Sulkeutumassa
stopped  - Pysäytetty
fault    - Vikatila
```

**Anturit (publish):**
```
gate/sensor/motion          - true/false
gate/sensor/limit_open      - true/false
gate/sensor/limit_closed    - true/false
gate/power/voltage          - 12.4 (V)
gate/power/current          - 15.2 (A)
gate/temperature/heatsink   - 45.3 (°C)
```

## Liitteet

- `layout_config.json` - Komponenttien sijoittelu ja johdotukset
- `PorttiKomponentit.py` - Fusion 360 add-in layoutin generointiin
- Sähkökaavio (erillinen tiedosto)
- Mekaaniset piirustukset (erillinen tiedosto)

---

**Dokumentin versio**: 1.0  
**Päivitetty**: 2025-12-19  
**Laatija**: Rauli Virtanen
