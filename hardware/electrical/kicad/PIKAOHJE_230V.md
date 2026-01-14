# 230V AC Kaavion piirtäminen - Pika-ohje

## Aloitus

1. **Avaa 230V arkki:**
   - KiCad:ssa kaksoisklikkaa laatikkoa "230V AC Järjestelmä"
   - Näet tyhjän arkin TODO-tekstillä

2. **Poista TODO-teksti:**
   - Klikkaa tekstiä → Delete

---

## Mitä piirretään

```
230V Verkko → RCD → Laturi → 12V Akku
                 ↓
            Sulatusrele → Vastus
```

---

## Komponentit ja symbolit

### 1️⃣ **230V Verkkoliitäntä** (J1)

**Symboli:** `Connector:Conn_01x03`

**Miten lisätään:**
1. Paina `A` (Add Symbol)
2. Kirjoita: `conn_01x03`
3. Klikkaa `Connector:Conn_01x03`
4. Klikkaa hiirellä vasempaan ylänurkkaan (sijoitus)

**Pinnit:** 3 kpl (L, N, PE)

**Asento:** Pysty, pinnit OIKEALLE →

**Reference:** `J1`  
**Value:** `230V Verkko` (muokkaa painamalla `E`)

---

### 2️⃣ **RCD (Vikavirtasuoja)** (Q1)

**Symboli:** `Device:Fuse` (käytetään sulakkeena, nimetään RCD:ksi)

**Miten lisätään:**
1. Paina `A`
2. Kirjoita: `fuse`
3. Valitse `Device:Fuse`
4. Sijoita J1:n oikealle puolelle

**Pinnit:** 2 kpl (in, out)

**Asento:** Pysty |

**HUOM:** Tarvitset KAKSI kappaletta (L ja N vaiheille)
- Lisää toinen fuse heti ensimmäisen alle
- Reference: `Q1` ja `Q2`
- Value: `RCD 30mA` (muokkaa `E`)

---

### 3️⃣ **Laturi** (PS1)

**Symboli:** `Device:Battery_Cell` (käytetään symbolina)

**Tai parempi:** `Connector:Conn_01x02` (laiturin liitäntä)

**Miten lisätään:**
1. Paina `A`
2. Kirjoita: `conn_01x02`
3. Sijoita RCD:n oikealle

**Pinnit:** 2 kpl (L_out, N_out → akku)

**Asento:** Pysty, pinnit OIKEALLE

**Reference:** `PS1`  
**Value:** `Laturi 230V→12V`

---

### 4️⃣ **Sulatusrele** (K1)

**Symboli:** `Relay:Relay_SPST` tai `Device:Fuse`

**Miten lisätään:**
1. Paina `A`
2. Kirjoita: `relay`
3. Valitse `Relay` (mikä tahansa)
4. Sijoita RCD:n ALAPUOLELLE

**Pinnit:** 2 kpl (kelalle) + 2 kpl (koskettimet)

**Jos ei löydy:** Käytä `Connector:Conn_01x02`

**Reference:** `K1`  
**Value:** `Sulatusrele 230V`

---

### 5️⃣ **Sulanapitokaapeli** (J2)

**Symboli:** `Connector:Conn_01x02`

**Miten lisätään:**
1. Paina `A`
2. `conn_01x02`
3. Sijoita releen oikealle

**Pinnit:** 2 kpl (L, N)

**Reference:** `J2`  
**Value:** `Sulanapitokaapeli 20-30W/m`

---

### 6️⃣ **Maadoitus (PE)**

**Symboli:** Power-symboli

**Miten lisätään:**
1. Paina `P` (Add Power)
2. Kirjoita: `earth`
3. Valitse `Earth` tai `GNDPWR`
4. Sijoita J1:n pin 3 alapuolelle

**Ei referenssiä** (power-symboli)

---

## Kytkentäviivat (Wiring)

### Paina `W` → Piirrä johdot

**L-vaihe (ruskea):**
```
J1 pin 1 → Q1 (RCD) → PS1 (Laturi)
         ↓
        Q3 → K1 → J2
```

**N-vaihe (sininen):**
```
J1 pin 2 → Q2 (RCD) → PS1 (Laturi)
         ↓
        Q4 → K1 → J2
```

**PE (kelta-vihreä):**
```
J1 pin 3 → ⏚ (Earth symbol)
```

---

## Labelsit (Signaalien nimet)

**Paina `L` → Lisää nimiö**

Lisää johtoihin:
- `L` (vaihe)
- `N` (nolla)
- `PE` (suojamaa)

**Miten:**
1. Paina `L`
2. Kirjoita: `L`
3. Klikkaa johtoa J1:n pin 1 jälkeen
4. Toista N:lle ja PE:lle

---

## Layout-vinkit

### Asettelu vasemmalta oikealle:

```
J1 (Verkko)  →  RCD  →  PS1 (Laturi)
                 ↓
                K1   →  J2 (Kaapeli)
```

### Välit:
- Komponenttien välissä ~5cm (n. 2 komponentin leveys)
- Pinnien välillä ~1cm

### Kierto:
- Paina `R` kierrättääksesi komponenttia
- Useimmat pystyyn (pinnit vaaka-suunnassa)

---

## Pikakomenot

| Näppäin | Toiminto |
|---------|----------|
| `A` | Lisää komponentti |
| `W` | Piirrä johto |
| `L` | Lisää label (nimi) |
| `P` | Lisää power (GND, +12V...) |
| `E` | Muokkaa (reference, value) |
| `M` | Siirrä |
| `R` | Kierrä 90° |
| `Del` | Poista |
| `Ctrl+Z` | Peru |
| `Ctrl+S` | Tallenna |

---

## Järjestys (suositus)

1. ✅ Lisää KAIKKI komponentit ensin (J1, Q1-Q4, PS1, K1, J2)
2. ✅ Järjestä ne vierekkäin (vasen→oikea)
3. ✅ Lisää PE (earth) symboli
4. ✅ Piirrä johdot (`W`)
5. ✅ Lisää labelit (`L`)
6. ✅ Tallenna (`Ctrl+S`)

---

## Tarkistuslista

- [ ] J1 (230V Verkko) - 3 pinniä
- [ ] Q1-Q4 (RCD) - 4 sulaketta (L_in, L_out, N_in, N_out)
- [ ] PS1 (Laturi) - 2 pinniä
- [ ] K1 (Sulatusrele) - 2-4 pinniä
- [ ] J2 (Sulanapitokaapeli) - 2 pinniä
- [ ] PE (⏚) maadoitus
- [ ] Kaikki johdot kytketty
- [ ] Labelit: L, N, PE
- [ ] Tallennettu

---

## Ongelmia?

**"En löydä symbolia":**
→ Kirjoita vain osa nimestä, esim. "conn" löytää kaikki liittimet

**"Johto ei yhdisty":**
→ Klikkaa TARKALLEEN pinnin päähän (näkyy vihreä ympyrä)

**"Komponentti väärässä asennossa":**
→ Paina `R` (Rotate) ennen kuin klikkaat sijoitukseen

**"En muista komentoa":**
→ Oikea klikkaus → Tool menu

---

## Valmis!

Kun olet piirtänyt kaiken:

1. **Tallenna:** `Ctrl+S`
2. **Sulje:** Palaa takaisin päänäkymään
3. **Vie PDF:** Aja terminaalissa:
   ```bash
   cd ~/PorttiAutomaatio/hardware/electrical/kicad
   ./export_schematics.py
   ```

PDF löytyy: `exports/230v_ac.pdf`

---

**Aikaa menee:** ~15-30 min ensimmäisellä kerralla

**Seuraavat arkit:** 12V DC ja ESP32 samalla tavalla! 🚀
