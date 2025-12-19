# Sähkökaaviot

## Tiedostot

Lisää tähän kansioon:
- [ ] Pääkaavio (12V DC tehokisko)
- [ ] Ohjauskaavio (ESP32 + anturit)
- [ ] 230V AC -kaavio (laturi + sulanpito)
- [ ] Liitäntäkaavio (terminal blocks)
- [ ] Kaapelointi (wire routing)

## Formaatit

**Suositellut:**
- PDF (tulostettava)
- KiCad (.kicad_sch) - avoimen lähdekoodin
- Fritzing (.fzz) - havainnollistava

**Vaihtoehdot:**
- Eagle (.sch)
- EasyEDA
- Käsin piirretty + skannaus

## Sisältö

### 1. Tehokaaavio (12V DC)
```
Akku (12V) ---[Pääsulake 80-100A]---[Pääkatkaisin]---+
                                                      |
                                    +----------------+----------------+
                                    |                |                |
                              [PWM/H-silta]    [DC/DC 12->5V]    [Relekortti]
                                    |                |                |
                                [Vinssi]        [ESP32]       [Lukko, Valot]
```

### 2. Ohjauskaavio (ESP32)
- GPIO-pinnit: PIN_PWM_ENABLE, PIN_DIRECTION, jne.
- Anturien kytkennät: pull-up/pull-down resistors
- Optoeristys relekorttiin
- TVS-diodit suojaukseen

### 3. 230V AC -kaavio
- Verkkovirtaliitäntä
- RCD 30mA
- Laturi 230V AC → 12V DC
- Sulanapitovastus + termostaatti/rele

### 4. Kaapelointi
- Kaapelipaksuudet (mm²)
- Värikoodit
- Liitintyypit
- Reititys

## Turvallisuus

**Tarkistettavaa:**
- ✅ Kaikki 230V AC -osat RCD:n takana
- ✅ Maadoitus kaikissa metallikoteloissa
- ✅ Oikeat kaapelipaksuudet (16mm² vinssille)
- ✅ Sulakkeet oikein mitoitettu
- ✅ E-stop katkaisee virran välittömästi
- ✅ TVS-diodit moottorin napojen yli

---

**Huom**: Lisää kaaviot ennen GitHubiin pushaamista!
