# Komponenttilayout - Exporttausohjeet

## Fusion 360 AddIn -layoutin exporttaus

### 1. Aja AddIn Fusion 360:ssa

1. Avaa Fusion 360
2. Scripts and Add-Ins → Add-Ins → "PorttiKomponentit"
3. Run → Layout generoidaan

### 2. Exporttaa PDF-piirustus

**Vaihtoehto A: Drawing (suositeltu)**
```
1. Create → Drawing
2. Valitse layout-body
3. Luo päänäkymä (Top View)
4. Lisää mittoja tarvittaessa
5. Right-click drawing → Export as PDF
6. Tallenna: component-layout.pdf
```

**Vaihtoehto B: Suora exportti**
```
1. File → Export
2. Type: PDF
3. Tallenna: component-layout.pdf
```

### 3. Exporttaa PNG-kuva

```
1. Aseta näkymä Top View:ksi
2. View Cube → Top
3. Fit to screen (F-näppäin)
4. Piilota gridit: Grid-kuvake pois
5. Capture Image: View → Capture Image
6. Tallenna: component-layout.png (PNG, korkea resoluutio)
```

### 4. Exporttaa johdotuskaavio erikseen

Jos haluat johdotukset selkeämmin:
```
1. Piilota bodies: Browser → Bodies → piilota komponentit
2. Näytä vain sketches: Browser → Sketches → näytä wire routes
3. Capture Image → wiring-diagram.png
```

### 5. Kopioi tiedostot projektin

```bash
# Kopioi exportoidut tiedostot
cp ~/Downloads/component-layout.pdf ~/PorttiAutomaatio/hardware/electrical/layouts/
cp ~/Downloads/component-layout.png ~/PorttiAutomaatio/hardware/electrical/layouts/
cp ~/Downloads/wiring-diagram.png ~/PorttiAutomaatio/hardware/electrical/layouts/

# Tai suoraan Fusion 360:sta:
# Save to: ~/PorttiAutomaatio/hardware/electrical/layouts/
```

---

## Mitä tiedostot sisältävät

**component-layout.pdf/png:**
- 200×120mm komponenttilevy
- 18 komponenttiblokkia mitoilla
- Johdotusreitit komponenttien välillä
- Aukot ja läpiviennit

**wiring-diagram.png:**
- Pelkät johdotusreitit
- Helpompi seurata yhteyksiä
- Voidaan tulostaa erilliseksi kytkentäkaavioksi

---

## Vinkkejä

**Parempi visualisointi:**
- Käytä Visual Style: Shaded with Edges
- Lisää Section Analysis jos haluat nähdä läpileikkauksen
- Animoi assembly jos teit liikkuvia osia

**Mittakaavatulostus:**
1. Drawing → 1:1 scale
2. Tulosta A4:lle
3. Käytä layouttia fyysiseen asennukseen

