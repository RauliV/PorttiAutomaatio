# Mekaniikkakomponentit - Komponenttiluettelo

## 📋 Sisällysluettelo
1. [Voimansiirto](#voimansiirto)
2. [Ketjuasennus](#ketjuasennus)
3. [Laakerointi](#laakerointi)
4. [Kiinnitykset](#kiinnitykset)
5. [Suojaus ja kotelointi](#suojaus-ja-kotelointi)
6. [Työkalut ja tarvikkeet](#työkalut-ja-tarvikkeet)

---

## Voimansiirto

### 1. Vinssi
**Malli**: Biltema 15-510 (tai vastaava)
- **Vetovoima**: 1000-1500 kg
- **Käyttöjännite**: 12V DC
- **Virrankulutus**: 40-80A kuormalla
- **Vaijerin pituus**: Ei tarvita (käytetään ketjua)
- **Linkit**:
  - 🔗 [Biltema 12V Sähkövinssi 900kg](https://www.biltema.fi/autoilu---mp/hinaus/sahkovinssit/sahkovinssi-12-v-900-kg-2000038979)
  - 🔗 [Motonet Powerwinch 1400kg](https://www.motonet.fi/fi/tuote/2310076/Sahkovinssi-Powerwinch-P1400-12V)

**Ominaisuudet**:
- Langaton kaukosäädin (ei välttämätön, koska ESP32 ohjaus)
- Planetaarivaihteisto (hitaampi mutta voimakkaampi)
- Sisäänrakennettu jarru (pitää portin paikallaan)

![Vinssi esimerkki](https://via.placeholder.com/400x300?text=Vinssi+12V+DC)

---

### 2. Ketjupyörä (Sprocket)
**Spesifikaatiot**:
- **Halkaisija**: 50-60 mm
- **Hampaiden määrä**: 12-15 kpl
- **Ketjutyyppi**: ANSI 40 / ISO 08B-1
- **Materiaali**: Teräs (S235 tai parempi)
- **Reikä**: Hitsattava suoraan vinssin rumpuun/akseliin

**Linkit**:
- 🔗 [SKF Ketjupyörä ANSI 40, 15T](https://www.skf.com/group/products/industrial-chains/transmission-chains)
- 🔗 [RS Components - Ketjupyörät](https://fi.rs-online.com/web/c/power-transmission/chains-sprockets/sprockets/)
- 🔗 [Aliexpress - Chain Sprocket 12T-15T](https://www.aliexpress.com/wholesale?SearchText=chain+sprocket+12T+15T+ANSI+40)

**Vaihtoehdot**:
- Polkupyörän ketjupyörä (sovitettava, mitat tarkistettava)
- CNC-sorvaus omasta materiaalista

![Ketjupyörä](https://via.placeholder.com/300x300?text=Ketjupyörä+15T)

---

## Ketjuasennus

### 3. Teollisuusketju
**Tyyppi**: ANSI 40 / ISO 08B-1 (1/2" pitch)
- **Pituus**: ~2670 mm (2×1335 mm per portin sivu)
- **Pitch**: 12.7 mm
- **Rullien halkaisija**: 7.92 mm
- **Materiaali**: Ruostumaton teräs tai galvanoitu teräs
- **Vetolujuus**: Min. 1500 kg

**Linkit**:
- 🔗 [SKF - Teollisuusketju ANSI 40](https://www.skf.com/group/products/industrial-chains/roller-chains)
- 🔗 [Traxit - Ketjut ja tarvikkeet](https://www.traxit.fi/ketjut)
- 🔗 [RS Components - Roller Chains](https://fi.rs-online.com/web/c/power-transmission/chains-sprockets/roller-chains/)

**Ketjun liittimet**:
- Master link (pikalukko)
- Niittiliitin (kestävämpi)

![ANSI 40 ketju](https://via.placeholder.com/400x200?text=ANSI+40+Roller+Chain)

---

### 4. Ketjun kiristin
**Rakenne**: Jousikuormitettu rulla
- **Rullan halkaisija**: 40-50 mm
- **Laakeri**: 6201-2RS tai 6202-2RS
- **Jousi**: Puristusjousi, F=50N, säätövara ±50mm
- **Materiaali**: Teräsrunko, laakeroitu rulla

**Linkit**:
- 🔗 [RS Components - Chain Tensioner](https://fi.rs-online.com/web/c/power-transmission/chains-sprockets/chain-tensioners/)
- 🔗 [SKF - Ketjun ohjainrullat](https://www.skf.com/group/products/industrial-chains/chain-components)

**DIY-vaihtoehto**:
- Oma suunnittelu ja valmistus (3D-piirustus Fusion 360:ssa)
- Hitsattu teräsrunko + laakerirulla + säätöjousi

![Ketjun kiristin](https://via.placeholder.com/300x300?text=Ketjun+Kiristin)

---

### 5. Ketjun ohjainrullat
**Käyttö**: Kaarteissa ja pitkillä osuuksilla
- **Halkaisija**: 40 mm
- **Laakeri**: 6200-2RS
- **Materiaali**: Muovi tai teräs
- **Määrä**: 2-4 kpl tarpeen mukaan

**Linkit**:
- 🔗 [SKF - Ohjainrullat](https://www.skf.com/group/products/industrial-chains)
- 🔗 [RS Components - Guide Rollers](https://fi.rs-online.com/web/c/power-transmission/)

---

## Laakerointi

### 6. Kuulalaakerit
**Malli**: 6202-2RS (ketjupyörälle)
- **Sisähalkaisija**: 15 mm
- **Ulkohalkaisija**: 35 mm
- **Leveys**: 11 mm
- **Tyyppi**: Umpitiivis (2RS = kaksi tiivistettä)
- **Määrä**: 2 kpl (per ketjupyörä)

**Linkit**:
- 🔗 [SKF 6202-2RS](https://www.skf.com/group/products/rolling-bearings/ball-bearings/deep-groove-ball-bearings/productid-6202-2RS1)
- 🔗 [RS Components - Kuulalaakerit](https://fi.rs-online.com/web/c/bearings-seals/ball-bearings/)
- 🔗 [Bauhaus - Laakerit](https://www.bauhaus.fi/)

**Vaihtoehdot**:
- 6201-2RS (sisähalkaisija 12 mm, pienempi)
- 6203-2RS (ulkohalkaisija 40 mm, isompi)

![Kuulalaakeri 6202-2RS](https://via.placeholder.com/250x250?text=6202-2RS+Laakeri)

---

### 7. Laakeripesät ja hylsyt
**Materiaali**: Alumiini tai teräs
- **Sisähalkaisija**: 35 mm (6202-2RS:n ulkohalkaisija)
- **Kiinnitys**: Pultattu tai hitsattu runkorakenteeseen
- **Määrä**: 2 kpl

**DIY-vaihtoehto**:
- CNC-sorvaus alumiinista
- 3D-tulostus (ABS/PETG) + metallivahvisteet

**Linkit**:
- 🔗 [RS Components - Bearing Housings](https://fi.rs-online.com/web/c/bearings-seals/bearing-housings-accessories/)

---

## Kiinnitykset

### 8. Kiinnityspultit ja mutterit
**Spesifikaatiot**:
- **M8 x 40 mm**: Ketjupyörän kiinnitys (4-6 kpl)
- **M10 x 60 mm**: Vinssin kiinnitys (4 kpl)
- **M6 x 30 mm**: Laakeripesien kiinnitys (8 kpl)
- **Luokitus**: 8.8 tai 10.9 (ruostumaton A4)
- **Aluslevyt**: Lukkojousialuslevy + normaali aluslevy

**Linkit**:
- 🔗 [Biltema - Pulttisarja](https://www.biltema.fi/tyokalut/kiinnitystarvikkeet/)
- 🔗 [Bauhaus - Ruuvit ja pultit](https://www.bauhaus.fi/)

---

### 9. Hitsatut kiinnikkeet porttiin
**Materiaali**: Teräslevyt 5-8 mm
- **Määrä**: 2 kpl per portin sivu (4 kpl yhteensä)
- **Kiinnitys**: Hitsattu portin runkoon tai pultattu
- **Ketjun kiinnitys**: Sokkanasta tai pultti + U-lukko

**DIY-valmistus**:
- Laserleikkaus tai plasmaleikkaus
- Taivutus ja hitsaus

![Ketjun kiinnike](https://via.placeholder.com/300x200?text=Ketjun+Kiinnike)

---

## Suojaus ja kotelointi

### 10. Ketjukotelo
**Materiaali**: Alumiini tai galvanoitu teräslevy (1-2 mm)
- **Pituus**: Ketjun pituuden mukaan (~1500 mm per sivu)
- **Leveys**: 80-100 mm
- **Ominaisuudet**:
  - Valutusreiät pohjassa (Ø6-8mm, 200mm välein)
  - Huoltoluukku (tarkistuksia varten)
  - Tiivistetyt läpiviennit

**Linkit**:
- 🔗 [Bauhaus - Alumiinilevyt](https://www.bauhaus.fi/)
- 🔗 [K-Rauta - Teräslevyt](https://www.k-rauta.fi/)

**DIY-valmistus**:
- Taivutus alumiinilevystä (särmäys)
- Niittaus tai hitsaus

![Ketjukotelo](https://via.placeholder.com/400x250?text=Ketjukotelo)

---

### 11. Tiivisteet ja läpiviennit
**Läpiviennit ketjulle**:
- **Materiaali**: Kumi tai silikoni
- **Toiminto**: Estää veden ja lian pääsyn koteloon

**Linkit**:
- 🔗 [Biltema - Kumitiivisteet](https://www.biltema.fi/)
- 🔗 [RS Components - Cable Glands](https://fi.rs-online.com/web/c/cables-wires/cable-accessories/cable-glands/)

---

### 12. Suojamaali ja korroosiosuoja
**Pintakäsittely**:
- **Pohjamaali**: Sinkkipohjamaali (esim. Tikkurila Rostex)
- **Päällimaali**: Ulkomaalipinnoite (esim. Tikkurila Pika-Teho)
- **Voitelu**: Ketjuöljy tai -rasva (ruostumaton, ei pestävä pois)

**Linkit**:
- 🔗 [Tikkurila - Metalli- ja teollisuusmaalit](https://www.tikkurila.fi/ammattilaiset/tuotteet/metallipinnoitteet)
- 🔗 [Biltema - Ketjuöljy](https://www.biltema.fi/kemia-ja-tarvikkeet/voiteluaineet/)

---

## Työkalut ja tarvikkeet

### 13. Hitsauslaitteet
**Käyttö**: Ketjupyörän hitsaus, kiinnikkeiden valmistus
- **Tyyppi**: MIG/MAG -hitsaus tai puikkohitsaus
- **Materiaali**: Hitsauslanka ER70S-6 (teräkselle)

**Linkit**:
- 🔗 [Biltema - Hitsauslaitteet](https://www.biltema.fi/tyokalut/sahkotyokalut/hitsauslaitteet/)
- 🔗 [Motonet - Hitsaus](https://www.motonet.fi/fi/tuotteita/tyokalut/hitsaus)

---

### 14. Mittaus- ja linjatyökalut
**Tarvittavat työkalut**:
- **Vesivaa**: Linjauksen tarkistus
- **Työntömitta**: Mittatarkkuus ±0.1 mm
- **Kulmamitta**: 90° ja 45° tarkistus
- **Laserlinjatyökalu**: Ketjulinjan tarkistus

**Linkit**:
- 🔗 [Biltema - Mittaustyökalut](https://www.biltema.fi/tyokalut/kasityokalut/mittaustyokalut/)
- 🔗 [Bauhaus - Lasertyökalut](https://www.bauhaus.fi/)

---

### 15. Käsityökalut
**Perustyökalut**:
- **Hylsysarja**: 8-22 mm (pulttien kiristys)
- **Jakoavaimet**: 8-19 mm
- **Leikkurit**: Teräsketjun katkaisu (ketjuleikkuri)
- **Poranterät**: HSS, Ø4-12 mm
- **Kierreleikkuri**: M6, M8, M10 (kierteiden korjaus)

**Linkit**:
- 🔗 [Biltema - Käsityökalut](https://www.biltema.fi/tyokalut/kasityokalut/)
- 🔗 [Motonet - Työkalut](https://www.motonet.fi/fi/tuotteita/tyokalut)

---

## 📊 Komponenttien yhteenveto

| Komponentti | Malli/Tyyppi | Määrä | Arvioitu hinta | Toimittaja |
|-------------|--------------|-------|----------------|------------|
| Vinssi | Biltema 15-510, 1000kg | 1 kpl | 150-250 € | Biltema, Motonet |
| Ketjupyörä | ANSI 40, 15T, d=50-60mm | 1 kpl | 20-40 € | RS Components, Aliexpress |
| Teollisuusketju | ANSI 40, 2670mm | 1 kpl | 30-50 € | SKF, Traxit |
| Ketjun kiristin | Jousikuormitettu rulla | 1 kpl | 20-30 € (DIY) | DIY tai RS Components |
| Kuulalaakerit | 6202-2RS | 2 kpl | 10-20 € | SKF, RS Components |
| Laakeripesät | Alumiini, CNC | 2 kpl | 15-30 € (DIY) | DIY tai RS Components |
| Kiinnityspultit | M8-M10, A4 | 20 kpl | 10-15 € | Biltema, Bauhaus |
| Ketjukotelo | Alumiini 1-2mm | 1 kpl | 30-50 € (DIY) | DIY tai K-Rauta |
| Tiivisteet | Kumi/silikoni | 5 kpl | 5-10 € | Biltema |
| Maali ja suoja | Sinkkipohja + päällysmaali | 1 sarja | 30-50 € | Tikkurila |
| Ketjuöljy | Teollisuusketjuöljy | 1 pullo | 10-15 € | Biltema |
| **YHTEENSÄ** | | | **~330-560 €** | |

---

## 🛠️ Asennusjärjestys

1. **Vinssin asennus**: Kiinnitä vinssi tukevalle alustalle, testaa toiminta
2. **Ketjupyörän hitsaus**: Hitsaa ketjupyörä vinssin rumpuun, tarkista linjaus
3. **Ketjun asennus**: Kiinnitä ketju porttiin molemmilta puolilta
4. **Kiristimen asennus**: Asenna kiristin alaosaan, säädä kireys
5. **Kotelointi**: Asenna ketjukotelo suojaksi
6. **Pintakäsittely**: Maalaa ja suojaa kaikki metalliset osat
7. **Testaus**: Testaa vinssi ja ketjumekanismi kuormalla

---

## 📸 Kuvagalleria

### Asennusesimerkkejä

![Ketjuvinssi-asennus](https://via.placeholder.com/600x400?text=Vinssi+Ketjupyörällä)

![Ketjureitti](https://via.placeholder.com/600x400?text=Ketjureitti+Portilla)

![Kiristin-asennettuna](https://via.placeholder.com/600x400?text=Ketjun+Kiristin)

---

## 🔗 Hyödylliset linkit

### Valmistajat ja jakelijat
- 🔗 [SKF - Ketjut ja laakerit](https://www.skf.com/fi)
- 🔗 [RS Components Suomi](https://fi.rs-online.com/)
- 🔗 [Traxit - Voimansiirtokomponentit](https://www.traxit.fi/)
- 🔗 [Biltema](https://www.biltema.fi/)
- 🔗 [Motonet](https://www.motonet.fi/)
- 🔗 [Bauhaus](https://www.bauhaus.fi/)

### Tekniset tiedot ja standardit
- 🔗 [ANSI Chain Standards](https://www.ansi.org/)
- 🔗 [ISO 08B Roller Chain Specifications](https://www.iso.org/)

### DIY-resurssit
- 🔗 [Instructables - DIY Winch Projects](https://www.instructables.com/circuits/projects/)
- 🔗 [YouTube - Chain Drive Installation](https://www.youtube.com/)

---

**Dokumentin versio**: 1.0  
**Päivitetty**: 26.12.2025  
**Laatija**: GitHub Copilot  
**Projekti**: PorttiAutomaatio
