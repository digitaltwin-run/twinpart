# digitaltwin-run / twinpart

Centralna biblioteka zweryfikowanych komponentow elektronicznych, modeli 3D STEP, symboli EDA oraz footprintow KiCad dla calego ekosystemu digitaltwin-run (w tym projektow keyboard, mouse, housing-studio oraz maskservice/viewer).

Komponenty sa definiowane zgodnie ze standardem wellmanifest.pcb/component-manifest/v1 i walidowane przez twin_kicad.

---

## Dostepne komponenty

| Identyfikator | Rodzaj | Status | MPN / Producent | Zastosowanie w projektach |
|---|---|---|---|---|
| rj45-molex-85513-5013 | connector | provisional | Molex 85513-5013 | Magistrala klawiatury i paneli kontrolnych |
| rp2040-zero | module | quarantined | Waveshare RP2040-Zero | Modul MCU dla keyboard oraz mouse |
| sw-tact-5.2x5.2 | switch | provisional | Takt-switch 5.2x5.2 mm | Klawiatura panel9 oraz przyciski funkcyjne |
| c-0603 | passive | provisional | Kondensator 0603 SMD | Pasywa odsprzegajace dla MCU i zlaczy |

---

## Uzycie CLI

```bash
# Wypisanie listy dostepnych czesci
twinpart list

# Filtrowanie wg rodzaju lub statusu
twinpart list --kind connector
twinpart list --status provisional

# Szczegolowe informacje o komponencie
twinpart info rj45-molex-85513-5013

# Sprawdzenie integralnosci calej biblioteki czesci
twinpart check

# Instalacja komponentu do projektu docelowego
twinpart install rj45-molex-85513-5013 --target /sciezka/do/projektu/artifacts/pcb

# Bezpieczna wymiana komponentu na PCB (automatyczny rip-up starych kolidujacych sciezek)
twinpart swap /sciezka/do/panel9.kicad_pcb --reference J1 --to-part rj45-molex-85513-5013 --margin 4.0
```

---

## Struktura czesci (parts/)

Kazdy komponent w parts/<kategoria>/<component_id>/ zawiera:
- manifest.json: definicje elektryczna, mechaniczna, mape pinow i sumy kontrolne assetow.
- *.kicad_mod: zweryfikowany footprint KiCad.
- *.kicad_sym: symbol schematowy.
- *.step: model 3D z poprawnie zorientowanymi osiami.
- vendor/: (opcjonalnie) oryginalne pakiety producenta, karty katalogowe PDF i materialy referencyjne.
