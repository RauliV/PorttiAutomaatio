
# PorttiKomponentit – Layout‑automaation dokumentaatio

## 📑 Sisällysluettelo
- [1. Järjestelmän yleiskuvaus](#1-järjestelmän-yleiskuvaus)
- [2. Add‑inin arkkitehtuuri](#2-add-inin-arkkitehtuuri)
- [3. JSON‑konfiguraation rakenne](#3-json-konfiguraation-rakenne)
- [4. Fusion 360 ‑parametrit](#4-fusion-360--parametrit)
- [5. Layoutin generoinnin työvaiheet](#5-layoutin-generoinnin-työvaiheet)
- [6. Lohkojen sijoittelu ja logiikka](#6-lohkojen-sijoittelu-ja-logiikka)
- [7. Kaapelireitit ja läpiviennit](#7-kaapelireitit-ja-läpiviennit)
- [8. Kiinnitysreiät](#8-kiinnitysreiät)
- [9. Add‑inin käyttö ja asennus](#9-add-inin-käyttö-ja-asennus)
- [10. Laajennettavuus ja jatkokehitys](#10-laajennettavuus-ja-jatkokehitys)

---

## 1. Järjestelmän yleiskuvaus

**PorttiKomponentit** on Fusion 360 ‑add‑in, joka generoi sähkö‑ ja ohjausjärjestelmän layoutin täysin automaattisesti.  
Järjestelmä perustuu **JSON‑konfiguraatioon**, joka määrittelee:

- Testilevyn mitat  
- Lohkojen mitat ja sijainnit  
- Kaapelireitit  
- Läpivientien mitat  
- Kiinnitysreiät  

Add‑in luo **aina täysin uuden layoutin**, eikä päivitä vanhaa.

---

## 2. Add‑inin arkkitehtuuri

### Kansiorakenne

```text
PorttiKomponentit/
 ├── manifest.json
 ├── main.py
 ├── layout_config.json
 └── Resources/
      ├── icon_24.png
      └── icon_32.png
```

### Tiedostojen roolit

| Tiedosto | Kuvaus |
|---------|--------|
| manifest.json | Add‑inin metatiedot ja pääskriptin nimi |
| main.py | Koko automaation logiikka |
| layout_config.json | Konfiguraatiotiedosto layoutille |
| Resources/ | Toolbar‑painikkeen ikonit |

---

## 3. JSON‑konfiguraation rakenne

JSON sisältää kaiken layoutin määrittelyyn tarvittavan tiedon.

### Rakenne

```json
{
  "plate": { ... },
  "slots": { ... },
  "mount_holes": { ... },
  "blocks": [ ... ],
  "routes": [ ... ]
}
```

### plate – Testilevyn mitat

```json
"plate": {
  "width": 120,
  "height": 60,
  "thickness": 2
}
```

### slots – Läpivientien mitat

```json
"slots": {
  "width": 6,
  "height": 3
}
```

### mount_holes – Kiinnitysreiät

```json
"mount_holes": {
  "diameter": 5,
  "offset": 8,
  "count": 4,
  "pattern": "corners"
}
```

### blocks – Lohkot

```json
{
  "name": "Akku",
  "param_name": "akku",
  "width": 40,
  "height": 20,
  "thickness": 3,
  "x_rel": -0.35,
  "y_rel": 0.35
}
```

### routes – Kaapelireitit

```json
["Akku", "Pääsulake"]
```

---

## 4. Fusion 360 ‑parametrit

Add‑in luo automaattisesti seuraavat parametrit:

### Levyn parametrit
- `plate_width`
- `plate_height`
- `plate_thickness`

### Läpivientien parametrit
- `slot_width`
- `slot_height`

### Kiinnitysreiät
- `mount_hole_diameter`
- `mount_hole_offset`

### Lohkoparametrit
Jokaiselle lohkolle:

- `<param_name>_width`
- `<param_name>_height`
- `<param_name>_thickness`

Esimerkki:

```text
esp32_width
esp32_height
esp32_thickness
```

---

## 5. Layoutin generoinnin työvaiheet

Add‑in suorittaa seuraavat vaiheet:

1. Lataa JSON‑konfiguraation  
2. Luo Fusion‑parametrit  
3. Tyhjentää mallin (bodyt ja sketsit)  
4. Luo Testilevyn  
5. Etsii levyn yläpinnan  
6. Luo lohkot JSONin mukaan  
7. Laskee lohkojen keskikohdat  
8. Piirtää kaapelireitit  
9. Luo läpiviennit reittien keskikohtiin  
10. Luo kiinnitysreiät  
11. Nimeää featuret timelineen  
12. Sovittaa näkymän  

---

## 6. Lohkojen sijoittelu ja logiikka

Lohkot sijoitetaan suhteellisilla koordinaateilla:

- `x_rel` = suhteellinen sijainti levyn leveydestä  
- `y_rel` = suhteellinen sijainti levyn korkeudesta  

Keskipiste lasketaan:

```text
x = x_rel * plate_width
y = y_rel * plate_height
```

Lohko extrudoidaan ylöspäin levyn pinnasta.

---

## 7. Kaapelireitit ja läpiviennit

### Kaapelireitit
- Piirretään suorina viivoina lohkojen keskikohtien välille  
- Ovat omassa sketsissään  

### Läpiviennit
- Jokaisen reitin keskikohtaan luodaan suorakulmainen slot  
- Slotin mitat tulevat JSONista  
- Slotit leikataan läpi levyn  

---

## 8. Kiinnitysreiät

Kiinnitysreiät määritellään JSONissa:

- halkaisija  
- offset  
- määrä  
- pattern (tällä hetkellä: corners)

Add‑in luo reiät:

- levyn neljään kulmaan  
- offset‑etäisyydelle reunoista  
- läpivientileikkauksena  

---

## 9. Add‑inin käyttö ja asennus

### Asennus
1. Kopioi kansio Fusionin AddIns‑hakemistoon  
2. Avaa Fusion → Tools → Scripts and Add‑ins  
3. Valitse add‑in → Run  
4. Toolbarissa näkyy painike

### Käyttö
- Paina toolbar‑painiketta  
- Add‑in generoi layoutin alusta  
- Kaikki perustuu JSON‑tiedostoon  

---

## 10. Laajennettavuus ja jatkokehitys

Järjestelmä on suunniteltu laajennettavaksi:

- Useita JSON‑profiileja  
- Komponenttien rotaatio  
- Spline‑muotoiset kaapelireitit  
- 3D‑komponenttien tuonti lohkojen tilalle  
- UI‑parametripaneeli Fusionissa  
- Layoutin päivitystila (ei vain uudelleenluonti)  
