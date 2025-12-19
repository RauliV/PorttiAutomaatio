# 3D-mallit - Ohjeet

## Fusion 360 -mallin käyttö

**A360-linkki**: https://a360.co/4ql5F3f

### Tiedostojen exporttaus Fusion 360:sta

1. **Avaa design A360:sta**
   - Kopioi linkki: https://a360.co/4ql5F3f
   - Avaa Fusion 360:ssa: File → Open from my computer → Open link

2. **Exporttaa STEP-tiedostot** (suositeltu valmistukseen):
   ```
   File → Export
   - Format: STEP (*.step, *.stp)
   - Refinement: Medium tai High
   - Save to: hardware/mechanical/
   ```

3. **Exporttaa STL-tiedostot** (3D-tulostus):
   ```
   File → Export
   - Format: STL (*.stl)
   - Structure: One file per body
   - Refinement: High
   - Save to: hardware/mechanical/stl/
   ```

4. **Exporttaa PDF-piirustukset**:
   ```
   Luo Drawing → Right-click → Export as PDF
   Save to: hardware/mechanical/drawings/
   ```

## Tarvittavat tiedostot GitHubiin

Exporttaa seuraavat osat erikseen:

### Pääkomponentit
- [ ] Ketjupyörä (hitsattava vinssiin)
- [ ] Kiristin-assembly
- [ ] Laakeripesä + spacers
- [ ] Ketjukotelo
- [ ] Kiinnityslevyt/konsoli
- [ ] ESP32-kotelo (jos suunniteltu)
- [ ] Komponenttilayout-levy (PorttiKomponentit.py:n generoima)

### Piirustukset
- [ ] Assembly-piirustus (yleiskuva)
- [ ] Ketjupyörän piirustus (mitat)
- [ ] Kiristimen piirustus
- [ ] Asennusohjeet kuvina

## Kansiorakenne

```
hardware/mechanical/
├── step/                 # STEP-tiedostot (valmistus)
│   ├── ketjupyora.step
│   ├── kiristin.step
│   ├── laakeripesa.step
│   └── kotelo.step
├── stl/                  # STL-tiedostot (3D-tulostus)
│   ├── kiristin_body.stl
│   ├── kiristin_roller.stl
│   └── kotelo_esp32.stl
├── drawings/             # PDF-piirustukset
│   ├── assembly.pdf
│   ├── ketjupyora.pdf
│   └── installation.pdf
├── images/               # Renderit ja kuvakaappaukset
│   ├── overview.png
│   ├── ketju_detail.png
│   └── assembly_steps.png
└── README.md            # Tämä tiedosto
```

## Mallien päivitys

Jos päivität Fusion 360 -mallia:

1. Tallenna muutokset A360:een
2. Exporttaa päivitetyt tiedostot (STEP/STL)
3. Korvaa vanhat tiedostot `hardware/mechanical/` -kansiossa
4. Päivitä mitat dokumentaatioon (`docs/mekaniikka.md`)
5. Commitoi muutokset:
   ```bash
   git add hardware/mechanical/
   git commit -m "Update: [komponentti] - [muutos]"
   ```

## Valmistusohjeet

### Ketjupyörä
- **Materiaali**: Teräs (S235 tai parempi)
- **Käsittely**: Galvanointi tai maalaus
- **Kiinnitys**: Hitsaus vinssin ulostuloon
- **Toleranssi**: Keskolinjaus ±2mm

### Kiristin
- **Materiaali**: Alumiini tai teräs
- **Jousi**: 50-100N kuormitus
- **Säätövara**: ±50mm
- **Rulla**: Muovipinnoitettu tai laakeroitu

### ESP32-kotelo
- **Materiaali**: ABS tai PETG (3D-tulostus)
- **Tiivistys**: IP54 tai parempi
- **Läpiviennit**: Kaapeleille ja antureille
- **Kiinnitys**: DIN-kisko tai ruuvit

---

**Huom**: Muista lisätä exportoidut tiedostot tähän kansioon ennen GitHubiin pushaamista!
