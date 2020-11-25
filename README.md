# RSJ

Softverska platforma za Rečnik srpskog jezika

## Komponente

### Extractor

Mikroservis za ekstrakciju teksta iz Word i PDF dokumenata, uz mogućnost čuvanja i podatka o rednom broju stranice na kome se svaka reč (ili pasus, blok teksta) nalazi.

### Indexer

Mikroservis za indeksiranje i pretragu:
 * korpusa
 * odrednica

Pretraga podržava istovremenu pretragu po oba pisma (ćirilica i latinica).

### OCR

Mikroservis za prepoznavanje teksta iz skeniranih dokumenata. Podržava oba pisma.

### Backend za rečnik

Django + REST Framework + MySQL backend za evidentiranje rečničkih odrednica.

### Frontend za rečnik

Angular aplikacija za unos rečničkih odrednica.

### Backend za korpus

TBD

### Frontend za korpus

Angular aplikacija za anotaciju teksta iz korpusa.

### Renderer

Komponenta za rendering rečničke odrednice u HTML i PDF.

## Raspored u produkciji

TBD


