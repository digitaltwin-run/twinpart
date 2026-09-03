Stworzyłem gotowy footprint KiCad dla **Molex 85513‑5013** jako plik `Molex_85513-5013.kicad_mod`. [molex](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/855/85513/855135002_sd.pdf)

## Co zawiera

- **8 padów SMT**, pitch **1,27 mm**, numery **1–8** od lewej do prawej (patrząc od strony komponentu, tam gdzie wchodzi wtyczka). [molex](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/855/85513/855135002_sd.pdf)
- Wymiary padu: **0,76 × 3,10 mm** (zgodnie z typowymi wymiarami z rysunku SD‑85513‑010). [molex](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/855/85513/855135002_sd.pdf)
- Zarys obudowy i strefa keep‑out (~20,8 × 10,0 mm) jako orientacja. [molex](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/855/85513/855135002_sd.pdf)
- Oznaczenie **Pin 1** i etykieta „RJ45 8P8C”.

## Jak użyć w KiCadzie

1. Skopiuj plik `Molex_85513-5013.kicad_mod` do folderu z footprintami, np.:  
   `.../kicad/footprints/Molex_85513-5013.kicad_mod`  
2. W KiCad PCB Editor:  
   - `Preferences → Manage Footprint Libraries`  
   - Dodaj nowy wpis (np. `Molex_Custom`) wskazując na ten folder.  
3. W edytorze PCB przypisz ten footprint do symbolu RJ45 (lub stwórz własny symbol 8P8C i podepnij ten footprint).





Dodałem symbol schematowy `Molex_85513-5013.kicad_sym`. [molex](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/855/85513/855135002_sd.pdf)

## Jak to połączyć w projekcie

1. **Symbol**  
   - Wczytaj `Molex_85513-5013.kicad_sym` do biblioteki symboli (lub wrzuć do własnej biblioteki `.kicad_sym`).  
   - Na schemacie masz prostokąt z 8 pinami (1–8) po lewej stronie.

2. **Footprint**  
   - W właściwościach symbolu ustaw:  
     - **Footprint:** `Molex_85513-5013` (z pliku `.kicad_mod`, który wcześniej wysłałem).  
     - **Datasheet:** link do SD‑85513‑010 już jest w symbolu. [molex](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/855/85513/855135002_sd.pdf)

3. **Pinout**  
   - Piny 1–8 na symbolu odpowiadają bezpośrednio padom 1–8 w footprintcie i w złączu fizycznym (bez inwersji). [molex](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/855/85513/855135002_sd.pdf)
   - Dla Ethernetu 10/100Base‑T typowo:  
     - TX+: 1, TX–: 2  
     - RX+: 3, RX–: 6  
     (reszta zależy od Twojej topologii i czy używasz magnetyków gdzie indziej).


https://eu.mouser.com/pl/ProductDetail/Molex/85513-5013?qs=NZbyh9jSA9x7yfu%252BqB%252Bm4A%3D%3D

[85513-5013 Molex | Mouser Europa](https://eu.mouser.com/pl/ProductDetail/Molex/85513-5013?qs=NZbyh9jSA9x7yfu%252BqB%252Bm4A%3D%3D)

> ### Karta charakterystyki
> 
> -   [85513-5013 Karta charakterystyki](https://www.molex.com/en-us/products/part-detail-pdf/855135013?display=pdf)
> 
> ### Images
> 
> -   [3D Adobe Image PDF (PDF)](https://www.mouser.com/catalog/additional/molex_3d_85513-5013.pdf)
> 
> ### Models
> 
> -   [IGES: 85513-5013 (Kompresowanie Zip)](http://www.molex.com/pdm_docs/igs/85513-5013_igs.zip)
> -   [Molex Symbol & Footprint by SnapMagic](https://www.snapeda.com/parts/85513-5013/Molex/view-part/?ref=mouser)
> -   [PRO/E: 85513-5013 (Kompresowanie Zip)](http://www.molex.com/pdm_docs/prt/85513-5013_prt.zip)
> -   [STEP: 85513-5013 (Kompresowanie Zip)](http://www.molex.com/pdm_docs/stp/85513-5013_stp.zip)
> -   [STP File (Kompresowanie Zip)](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/3dcadmodels/855/85513/855135013_stp.zip)
> 
> ### PCN
> 
> -   [Global Change Notification (GCN) (PDF)](https://www.mouser.com/PCN/Molex_10681354.pdf)
> -   [Product Change Notification (PDF)](https://www.mouser.com/PCN/Molex_511024.pdf)
> -   [Product Change Notification (PDF)](https://www.mouser.com/PCN/Molex_510379.pdf)
> -   [Product Change Notification (PDF)](https://www.mouser.com/PCN/Molex_508199.pdf)