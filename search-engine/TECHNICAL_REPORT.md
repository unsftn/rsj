# Pretraživač korpusa srpskog jezika -- tehnički izveštaj

## Sadržaj

1. [Uvod](#1-uvod)
2. [Pregled sistema](#2-pregled-sistema)
3. [Struktura projekta](#3-struktura-projekta)
4. [Osnovna biblioteka: search-engine](#4-osnovna-biblioteka-search-engine)
   - 4.1 [Trie struktura podataka](#41-trie-struktura-podataka)
   - 4.2 [Tokenizer](#42-tokenizer)
   - 4.3 [SearchEngine -- pretraživač dokumenata](#43-searchengine----pretraživač-dokumenata)
   - 4.4 [Morfološki rečnik](#44-morfološki-rečnik)
   - 4.5 [Odrednice rečnika](#45-odrednice-rečnika)
   - 4.6 [Naslovi publikacija](#46-naslovi-publikacija)
   - 4.7 [Obrada teksta i transliteracija](#47-obrada-teksta-i-transliteracija)
5. [REST API server: search-api](#5-rest-api-server-search-api)
6. [CLI alat: search-cli](#6-cli-alat-search-cli)
7. [Baza podataka i indeksiranje](#7-baza-podataka-i-indeksiranje)
8. [Serijalizacija i perzistencija](#8-serijalizacija-i-perzistencija)
9. [Konkurentnost i bezbednost niti](#9-konkurentnost-i-bezbednost-niti)
10. [Docker i produkcijsko okruženje](#10-docker-i-produkcijsko-okruženje)
11. [Performanse](#11-performanse)
12. [Testiranje](#12-testiranje)
13. [Istorija razvoja](#13-istorija-razvoja)
14. [Zaključak](#14-zaključak)

---

## 1. Uvod

Ovaj dokument opisuje arhitekturu, implementaciju i funkcionisanje sistema za pretraživanje
korpusa srpskog jezika, razvijenog u programskom jeziku Rust. Sistem je deo projekta Rečnika
savremenog srpskog jezika (RSSJ) Matice srpske i obezbeđuje sledeće funkcionalnosti:

- pretraživanje punog teksta sa isticanjem pogodaka,
- prefiksno i sufiksno pretraživanje reči,
- morfološki rečnik sa gramatičkim oblicima reči,
- pretraživanje odrednica rečnika,
- pretraživanje naslova publikacija,
- REST API za integraciju sa veb aplikacijama,
- uvoz podataka iz MySQL baza (rečnik i korpus).

Sistem je napisan kao zamena za prethodnu Python implementaciju, sa ciljem značajnog poboljšanja
performansi: brže indeksiranje, brže pretraživanje, manji utrošak memorije i kraće vreme
pokretanja servera.

---

## 2. Pregled sistema

Sistem se sastoji od tri Rust crate-a organizovanih u Cargo workspace:

```
┌─────────────────────────────────────────────────────────┐
│                    Cargo Workspace                      │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  search-cli  │  │  search-api  │  │               │  │
│  │  (binarni)   │  │  (binarni)   │  │               │  │
│  │              │  │              │  │               │  │
│  │  Clap CLI    │  │  Axum HTTP   │  │               │  │
│  │  MySQL uvoz  │  │  REST API    │  │               │  │
│  └──────┬───────┘  └──────┬───────┘  │               │  │
│         │                 │          │ search-engine │  │
│         │    zavisnost    │          │ (biblioteka)  │  │
│         └────────────────►│◄─────────│               │  │
│                           │          │  Trie, Engine │  │
│                           ▼          │  Morphology   │  │
│                    ┌──────────────┐  │  Odrednica    │  │
│                    │search-engine │  │  Naslov       │  │
│                    │  (lib.rs)    │◄─┤  text_utils   │  │
│                    └──────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**search-engine** je osnovna biblioteka bez spoljnih zavisnosti osim fajl sistema. Sadrži četiri
nezavisna engine-a za pretraživanje, svaki sa sopstvenim trie indeksom i bincode serijalizacijom.

**search-api** je HTTP server zasnovan na Axum radnom okviru koji izlaže funkcionalnosti
biblioteke kroz REST API endpointe.

**search-cli** je alat komandne linije zasnovan na Clap radnom okviru, namenjen upravljanju
indeksima i uvozu podataka iz MySQL baza podataka.

---

## 3. Struktura projekta

```
search-engine/                      # koren workspace-a
├── Cargo.toml                      # konfiguracija workspace-a
├── Cargo.lock                      # zaključane verzije zavisnosti
├── Dockerfile                      # višefazna Docker slika
├── docker-compose.yml              # Docker Compose konfiguracija
├── build.sh                        # skripta za izgradnju
├── reindex.sh                      # skripta za reindeksiranje
├── entrypoint.sh                   # Docker ulazna tačka
├── CHANGELOG.md                    # dnevnik promena
├── search_index/                   # direktorijum za binarne indekse
│   ├── search_index.bin            # indeks punog teksta
│   ├── morphology.bin              # morfološki rečnik
│   ├── odrednica.bin               # odrednice rečnika
│   └── naslov.bin                  # naslovi publikacija
│
├── search-engine/                  # osnovna biblioteka
│   ├── Cargo.toml
│   └── src/
│       ├── lib.rs                  # javni API i tip greške
│       ├── trie.rs                 # trie struktura podataka
│       ├── tokenizer.rs            # tokenizacija teksta
│       ├── engine.rs               # pretraživač dokumenata
│       ├── morphology.rs           # tipovi za morfologiju
│       ├── morphology_engine.rs    # morfološki pretraživač
│       ├── odrednica.rs            # tip za odrednice
│       ├── odrednica_engine.rs     # pretraživač odrednica
│       ├── naslov.rs               # tip za naslove
│       ├── naslov_engine.rs        # pretraživač naslova
│       └── text_utils.rs           # transliteracija i obrada
│
├── search-api/                     # REST API server
│   ├── Cargo.toml
│   └── src/
│       └── main.rs                 # Axum server sa endpointima
│
└── search-cli/                     # CLI alat
    ├── Cargo.toml
    └── src/
        └── main.rs                 # Clap komande i MySQL uvoz
```

### Zavisnosti

Workspace definiše zajedničke zavisnosti u korenskom `Cargo.toml`:

| Zavisnost | Verzija | Namena |
|-----------|---------|--------|
| serde | 1.0 | Serijalizacija/deserijalizacija |
| serde_json | 1.0 | JSON format |
| bincode | 1.3 | Binarna serijalizacija |
| axum | 0.7 | HTTP radni okvir |
| tokio | 1.35 | Asinhroni runtime |
| tower-http | 0.5 | CORS, trace middleware |
| mysql | 25.0 | MySQL konektor |
| clap | 4.5 | Parsiranje argumenata CLI |
| regex | 1.10 | Regularni izrazi |
| anyhow | 1.0 | Obrada grešaka (aplikacioni nivo) |
| thiserror | 1.0 | Obrada grešaka (bibliotečki nivo) |
| tracing | 0.1 | Strukturirano logovanje |
| chrono | 0.4 | Rad sa datumima |
| flate2 | 1.0 | Kompresija |
| sysinfo | 0.30 | Sistemske informacije |

---

## 4. Osnovna biblioteka: search-engine

Biblioteka `search-engine` je srce sistema. Njen javni API je definisan u `lib.rs`:

```rust
pub mod trie;
pub mod engine;
pub mod tokenizer;
pub mod morphology;
pub mod morphology_engine;
pub mod odrednica;
pub mod odrednica_engine;
pub mod naslov;
pub mod naslov_engine;
pub mod text_utils;
```

Definisan je i zajednički tip greške:

```rust
#[derive(Debug, thiserror::Error)]
pub enum SearchError {
    Io(#[from] std::io::Error),
    Serialization(#[from] bincode::Error),
    InvalidQuery(String),
    DocumentNotFound(i32),
}
```

### 4.1 Trie struktura podataka

Trie (prefiksno stablo) je osnovna struktura podataka za indeksiranje reči. Implementiran je u
modulu `trie.rs`.

#### Definicija čvora

```rust
pub struct TrieNode {
    pub children: HashMap<char, Box<TrieNode>>,
    pub doc_ids: Vec<i32>,
    pub positions: Vec<i32>,
    pub is_end_of_word: bool,
}
```

Svaki čvor sadrži:
- **children** -- mapa dece indeksirana po Unicode karakteru,
- **doc_ids** i **positions** -- paralelni vektori koji čuvaju parove (ID dokumenta, pozicija tokena),
- **is_end_of_word** -- označava da li je čvor kraj validne reči.

#### Vizuelna predstava trie strukture

Primer za reči "pas", "pad", "pauk":

```
              (koren)
                │
                p
                │
                a
               / \
              s   d       u
              │   │       │
             [*]  [*]     k
                          │
                         [*]

[*] = is_end_of_word = true, sa listom (doc_id, position)
```

U ovom primeru:
- Putanja `p → a → s` vodi do čvora koji označava kraj reči "pas"
- Putanja `p → a → d` vodi do čvora koji označava kraj reči "pad"
- Putanja `p → a → u → k` vodi do čvora koji označava kraj reči "pauk"

Zajedničke prefikse dele isti čvorovi, što štedi memoriju.

#### Operacije nad trie strukturom

**Umetanje reči** (`insert_word`): Prolazi se kroz stablo karakter po karakter, kreirajući
nove čvorove po potrebi. Na kraju reči, čvor se označava sa `is_end_of_word = true` i dodaju
se ID dokumenta i pozicija tokena.

**Tačno pretraživanje** (`search_word`): Prolazi se niz stablo prateći karaktere reči. Ako
se stigne do kraja reči i čvor je označen kao kraj reči, vraćaju se svi parovi
`(doc_id, position)`.

**Prefiksno pretraživanje** (`collect_words`): Prvo se navigira do čvora koji odgovara
prefiksu, a zatim se rekurzivnim obilaskom podstabla prikupljaju sve reči koje počinju tim
prefiksom.

**Prikupljanje svih pozicija** (`collect_all_positions`): Rekurzivno prikuplja sve parove
`(doc_id, position)` iz datog čvora i svih njegovih potomaka. Koristi se za sufiksno
pretraživanje.

**Brojanje vokabulara** (`count_vocabulary`): Rekurzivno broji koliko čvorova u stablu je
označeno kao kraj reči.

#### Složenost operacija

| Operacija | Vremenska složenost |
|-----------|-------------------|
| Umetanje | O(m), m = dužina reči |
| Tačno pretraživanje | O(m) |
| Prefiksno pretraživanje | O(m + k), k = broj rezultata |
| Brojanje vokabulara | O(n), n = ukupan broj čvorova |

#### Upravljanje memorijom u trie strukturi

Trie struktura ilustruje nekoliko ključnih koncepata Rust-ovog sistema vlasništva
(ownership) i upravljanja memorijom.

**Box<TrieNode> i vlasništvo nad čvorovima potomcima**

Polje `children` ima tip `HashMap<char, Box<TrieNode>>`. Korišćenje `Box<T>` ovde
je neophodno iz dva razloga:

1. **Rekurzivna veličina tipa**: `TrieNode` sadrži `HashMap` čije vrednosti su
   opet `TrieNode`. Bez indirekcije, kompajler ne bi mogao da odredi veličinu
   strukture u vreme kompajliranja, jer bi ona bila beskonačno rekurzivna.
   `Box<T>` alocira podatke na heap-u i čuva samo pokazivač fiksne veličine
   (8 bajtova na 64-bitnoj platformi).

2. **Semantika vlasništva**: Svaki roditelj je isključivi vlasnik svojih potomaka.
   Kada se roditelj oslobodi iz memorije (drop), automatski se poziva destruktor
   za svako dete, koje onda rekurzivno oslobađa svoju decu. Nema potrebe za
   ručnim upravljanjem memorijom niti za garbage collector-om.

```
Vlasništvo u trie stablu:

  TrieNode (koren)                    ← vlasnik svih direktnih potomaka
    │
    ├── 'p' → Box<TrieNode>          ← Box poseduje heap-alocirani čvor
    │           │
    │           └── 'a' → Box<TrieNode>
    │                       │
    │                       ├── 's' → Box<TrieNode>
    │                       └── 'd' → Box<TrieNode>
    │
    └── 'k' → Box<TrieNode>
                │
                └── ...

Kada se koren oslobodi (drop):
  1. HashMap poziva drop za svaki Box<TrieNode>
  2. Svaki Box<TrieNode> poziva drop za svoj TrieNode
  3. Taj TrieNode poziva drop za svoj HashMap
  4. Rekurzivno do listova

  → celo stablo se automatski oslobađa, bez curenja memorije
```

**Menjajuća referenca (&mut self) pri umetanju**

Metoda `insert_word` zahteva `&mut self` -- ekskluzivnu menjajuću referencu.
Rust-ov borrow checker garantuje da u trenutku umetanja niko drugi ne čita
niti piše po stablu:

```rust
pub fn insert_word(&mut self, word: &str, doc_id: i32, position: i32) {
    let mut node = self;                    // &mut self → menjajuća referenca na koren
    for ch in word.chars() {
        node = node.children
            .entry(ch)
            .or_insert_with(|| Box::new(TrieNode::new()));
            // ↑ entry API: ako ključ ne postoji, kreira novi Box<TrieNode>
            //   vraća &mut Box<TrieNode>, automatski dereferencira u &mut TrieNode
    }
    node.is_end_of_word = true;
    node.add_position(doc_id, position);
}
```

Ovo je primer Rust-ove garancije "aliasing XOR mutability": u svakom trenutku,
podatak ili ima jednu menjajuću referencu (&mut), ili proizvoljno mnogo
nepromenljivih referenci (&), ali nikada oboje istovremeno.

**Nepromenljiva referenca (&self) pri pretraživanju**

Metode pretraživanja koriste `&self`, što omogućava da više niti istovremeno
čita stablo:

```rust
pub fn search_word(&self, word: &str) -> Option<Vec<(i32, i32)>> {
    let mut node = self;                    // &self → nepromenljiva referenca
    for ch in word.chars() {
        match node.children.get(&ch) {      // get vraća Option<&Box<TrieNode>>
            Some(child) => node = child,    // automatski deref Box → &TrieNode
            None => return None,
        }
    }
    // ...
}
```

Razlika između `insert_word(&mut self)` i `search_word(&self)` je ono što
omogućava konkurentno čitanje u API serveru (poglavlje 9).

**Vec<i32> i alokacija na heap-u**

Polja `doc_ids` i `positions` su tipa `Vec<i32>`. `Vec` alocira niz na heap-u
sa kapacitetom koji se udvostručuje po potrebi (amortizovano O(1) dodavanje).
Svaki `TrieNode` poseduje svoje vektore; kada se čvor oslobodi, oslobađa se
i memorija vektora.

```
Memorijski raspored jednog TrieNode:

Stack (ili unutar Box na heap-u):
┌──────────────────────────────────┐
│ children: HashMap<char, Box<...>>│ → heap: hash tabela + Box-ovi
│ doc_ids:  Vec<i32>               │ → heap: [1, 3, 7, 12, ...]
│ positions: Vec<i32>              │ → heap: [0, 5, 2, 8, ...]
│ is_end_of_word: bool             │   (1 bajt, inline)
└──────────────────────────────────┘
        │
        └── Ukupno na stack-u: 3 pokazivača + metadata = ~72 bajta
            Podaci na heap-u: varijabilno, zavisi od broja dece i pozicija
```

**Clone i duboko kopiranje**

`TrieNode` implementira `Clone` (preko `#[derive(Clone)]`). Poziv `clone()`
kreira duboku kopiju celog podstabla -- svaki `Box`, svaki `HashMap`, svaki
`Vec` se rekurzivno kopira. Ovo je skupo za velika stabla i koristi se samo
pri serijalizaciji (gde se kreira `SerializableEngine` -- videti poglavlje 8).

### 4.2 Tokenizer

Tokenizer je implementiran u modulu `tokenizer.rs` i koristi regularni izraz `\b\w+\b` za
izdvajanje reči iz teksta.

```rust
pub struct Tokenizer {
    word_pattern: Regex,
}
```

Tokenizer pruža tri metode:

1. **`tokenize`** -- vraća vektor lowercase reči:
   ```
   "Brz, smeđ lisac." → ["brz", "smeđ", "lisac"]
   ```

2. **`tokenize_with_positions`** -- vraća parove (reč, bajt pozicija):
   ```
   "Brz lisac" → [("brz", 0), ("lisac", 4)]
   ```

3. **`tokenize_offsets`** -- vraća kompaktne parove `(u32, u16)` sa bajtovskim početkom
   i dužinom svakog tokena. Ovi podaci se keširaju po dokumentu radi efikasnog generisanja
   fragmenata bez ponovnog parsiranja teksta.

```
Ulaz: "Danas je lep dan."

tokenize:
  → ["danas", "je", "lep", "dan"]

tokenize_offsets:
  → [(0, 5), (6, 2), (9, 3), (13, 3)]
       │  │   │  │    │  │    │   │
       │  └─dužina    │  └─dužina
       └─početak      └─početak
```

Sve metode rade sa Unicode karakterima, što je neophodno za ispravnu tokenizaciju
srpskog teksta koji može biti na ćirilici ili latinici.

### 4.3 SearchEngine -- pretraživač dokumenata

`SearchEngine` je centralni deo sistema za pretraživanje punog teksta, implementiran u
`engine.rs`.

#### Struktura

```rust
pub struct SearchEngine {
    forward_trie: TrieNode,                          // prefiksno pretraživanje
    reverse_trie: TrieNode,                          // sufiksno pretraživanje
    documents: HashMap<i32, String>,                 // sadržaj dokumenata
    doc_metadata: HashMap<i32, DocumentMetadata>,    // metapodaci
    token_offsets: HashMap<i32, Vec<(u32, u16)>>,    // keširani ofseti
    tokenizer: Tokenizer,                            // instanca tokenizera
}
```

Koriste se dva trie stabla:
- **forward_trie** za prefiksno i tačno pretraživanje,
- **reverse_trie** za sufiksno pretraživanje (reči se čuvaju obrnute).

```
Reč "kuća" u forward_trie:     Reč "kuća" u reverse_trie:
    k → u → ć → a [*]              a → ć → u → k [*]

Sufiksno pretraživanje za "ća":
    reverse_trie: navigacija po "ać" → prikupljanje potomaka
```

#### Dodavanje dokumenta

Metoda `add_document` prima ID dokumenta, tekst i metapodatke. Tok obrade:

```
Ulazni tekst: "Lepa kuća stoji na brdu."
                │
                ▼
         ┌─────────────┐
         │  Tokenizer  │
         └──────┬──────┘
                │
    ["lepa", "kuća", "stoji", "na", "brdu"]
         pozicije: 0, 1, 2, 3, 4
                │
                ├──────────────────────────┐
                ▼                          ▼
    ┌──────────────────┐      ┌──────────────────────┐
    │   forward_trie   │      │    reverse_trie      │
    │ insert("lepa",   │      │ insert("apel",       │
    │   doc_id, 0)     │      │   doc_id, 0)         │
    │ insert("kuća",   │      │ insert("aćuk",       │
    │   doc_id, 1)     │      │   doc_id, 1)         │
    │ ...              │      │ ...                  │
    └──────────────────┘      └──────────────────────┘
                │
                ▼
    ┌───────────────────────────────────┐
    │ Čuvanje u documents, doc_metadata │
    │ i token_offsets mapama            │
    └───────────────────────────────────┘
```

#### Frazno pretraživanje

Metoda `search_phrase` implementira pretraživanje celih fraza sa isticanjem pogodaka.

Algoritam se odvija u nekoliko koraka:

**Korak 1: Tokenizacija upita**

```
Upit: "lepa kuća" → ["lepa", "kuća"]
```

**Korak 2: Pronalaženje pozicija svake reči**

```
search_word("lepa")  → [(doc_1, 0), (doc_2, 5), (doc_3, 12)]
search_word("kuća")  → [(doc_1, 1), (doc_2, 8), (doc_3, 13)]
```

**Korak 3: Presek dokumenata**

Pronalaze se dokumenti koji sadrže SVE reči iz fraze:

```
docs_per_word[0] = {doc_1, doc_2, doc_3}
docs_per_word[1] = {doc_1, doc_2, doc_3}
presek = {doc_1, doc_2, doc_3}
```

**Korak 4: Provera uzastopnosti pozicija** (`find_phrase_matches`)

Za svaku poziciju prve reči u kandidat dokumentu, proverava se da li naredne reči
zauzimaju uzastopne pozicije:

```
doc_1: "lepa" na poziciji 0, "kuća" na poziciji 1
       pozicija 0 + 1 = 1 ✓ → fraza pronađena na poziciji 0

doc_2: "lepa" na poziciji 5, "kuća" na poziciji 8
       pozicija 5 + 1 = 6 ≠ 8 ✗ → nema podudaranja
```

**Korak 5: Generisanje fragmenata**

Sistem podržava dva režima generisanja fragmenata:

- **"word" režim** (`generate_word_fragments`): Generiše fragmente fiksne dužine
  (meren brojem reči) oko pronađene fraze.
- **"sentence" režim** (`generate_sentence_fragments`): Generiše cele rečenice
  koje sadrže pogodak.

U oba režima, preklapajući fragmenti se spajaju metodom `merge_overlapping_ranges`.

#### Isticanje pogodaka

Pronađene fraze se obeležavaju markerima `***`:

```
Ulaz: "Stara lepa kuća stoji na brdu."
Upit: "lepa kuća"

Izlaz (word režim, fragment_size=10):
  "Stara ***lepa kuća*** stoji na brdu."

Izlaz (sentence režim):
  "Stara ***lepa kuća*** stoji na brdu."
```

Ako je fragment deo većeg teksta, dodaju se elipse:

```
"... stara ***lepa kuća*** stoji ..."
```

#### Spajanje preklapajućih fragmenata

Kada više pogodaka u istom dokumentu generiše bliske fragmente, oni se spajaju:

```
Pre spajanja:
  Fragment 1: pozicije [3..8], pogodak na poziciji 5
  Fragment 2: pozicije [6..11], pogodak na poziciji 9

Posle spajanja:
  Fragment: pozicije [3..11], pogoci na pozicijama 5 i 9
```

Algoritam sortira opsege po početnoj poziciji i spaja ih ako se preklapaju:

```rust
fn merge_overlapping_ranges(ranges) -> merged:
    sortiraj ranges po start poziciji
    za svaki opseg:
        ako se preklapa sa prethodnim:
            proširi prethodni opseg
            spoj liste pogodaka
        inače:
            dodaj kao novi opseg
```

#### Pretraživanje po više reči (OR režim)

Metoda `search_words` implementira pretraživanje sa logičkim ILI -- dokument se
vraća ako sadrži bilo koju od zadatih reči:

```
Ulaz: words = ["kuća", "brod", "selo"]

Za svaku reč: prikupi (doc_id, position)
Grupiši po doc_id
Za svaki dokument: generiši fragmente
```

Za razliku od fraznog pretraživanja, ovde se ne zahteva uzastopnost pozicija.

#### Prefiksno i sufiksno pretraživanje

**Prefiksno pretraživanje** (`prefix_search`): Navigira do čvora u forward_trie
koji odgovara prefiksu, a zatim prikuplja sve reči iz podstabla.

```
prefix_search("ku") → ["kuća", "kum", "kupiti", "kurjak", ...]
```

**Sufiksno pretraživanje reči** (`suffix_word_search`): Koristi reverse_trie.
Sufiks se obrne i tretira kao prefiks u obrnutom stablu:

```
suffix_word_search("ća")
  → obrni: "ać"
  → navigiraj u reverse_trie do "ać"
  → prikupi potomke
  → obrni nazad: ["kuća", "voća", "noća", ...]
```

**Sufiksno pretraživanje pozicija** (`suffix_search`): Isto kao gore, ali
vraća parove `(doc_id, position)` umesto reči. Aktivira se prefiksom `~` u upitu:

```
search_word("~nja") → pozicije svih reči koje se završavaju na "nja"
```

#### Upravljanje memorijom u SearchEngine

`SearchEngine` je struktura koja poseduje sve svoje podatke bez deljenja -- ovo je
tipičan Rust obrazac vlasništva gde jedna struktura ima isključivu kontrolu nad
celokupnim stanjem.

**Vlasništvo nad podacima**

```rust
pub struct SearchEngine {
    forward_trie: TrieNode,                          // vlasnik (ne Box, ne Arc)
    reverse_trie: TrieNode,                          // vlasnik
    documents: HashMap<i32, String>,                 // vlasnik svih stringova
    doc_metadata: HashMap<i32, DocumentMetadata>,    // vlasnik metapodataka
    token_offsets: HashMap<i32, Vec<(u32, u16)>>,    // vlasnik keširanih ofseta
    tokenizer: Tokenizer,                            // vlasnik (sadrži Regex)
}
```

Sva polja su u direktnom vlasništvu -- bez `Rc`, `Arc` ili sirovih pokazivača.
To znači da kada se `SearchEngine` oslobodi iz memorije, automatski se oslobađaju
oba trie stabla, svi dokumenti, svi metapodaci i svi keširani ofseti.

```
Dijagram vlasništva SearchEngine:

SearchEngine
  │
  ├── forward_trie: TrieNode ──────► heap: celo stablo čvorova
  │                                   (Box<TrieNode> rekurzivno)
  │
  ├── reverse_trie: TrieNode ──────► heap: obrnuto stablo čvorova
  │
  ├── documents: HashMap ──────────► heap: hash tabela
  │     │                              │
  │     ├── key: 1 → String ──────────► heap: "Lepa kuća stoji..."
  │     ├── key: 2 → String ──────────► heap: "Brod plovi..."
  │     └── ...
  │
  ├── doc_metadata: HashMap ───────► heap: hash tabela
  │     └── key: 1 → DocumentMetadata
  │                    ├── title: Option<String> ──► heap: "Naslov"
  │                    └── author: Option<String> ─► heap: "Autor"
  │
  ├── token_offsets: HashMap ──────► heap: hash tabela
  │     └── key: 1 → Vec<(u32,u16)> ─► heap: [(0,5),(6,2),...]
  │
  └── tokenizer: Tokenizer
        └── word_pattern: Regex ───► heap: kompajlirani automat
```

**Prenos vlasništva (move semantika) u add_document**

Potpis metode `add_document` jasno pokazuje transfer vlasništva:

```rust
pub fn add_document(&mut self, doc_id: i32, text: String, metadata: DocumentMetadata) {
```

Parametri `text: String` i `metadata: DocumentMetadata` primaju se po vrednosti,
što znači da pozivalac predaje vlasništvo nad tim podacima. Nakon poziva,
pozivalac više ne može koristiti te vrednosti -- kompajler to garantuje
u vreme kompajliranja:

```rust
let tekst = String::from("Lepa kuća stoji na brdu.");
let meta = DocumentMetadata { title: Some("Naslov".into()), author: None };

engine.add_document(1, tekst, meta);

// tekst i meta su sada "moved" -- sledeća linija bi izazvala grešku kompajlera:
// println!("{}", tekst);  // GREŠKA: value used after move
```

Unutar metode, `text` se premešta (move) u `documents` HashMap, a `metadata` u
`doc_metadata` HashMap. Nema kopiranja podataka -- samo se prenosi vlasništvo
nad heap-alociranim memorijskim blokovima.

**Pozajmljivanje (borrowing) pri pretraživanju**

Metode pretraživanja uzimaju nepromenljivu referencu na engine (`&self`) i
na ulazni string (`&str`):

```rust
pub fn search_phrase(&self, phrase: &str, fragment_size: usize, mode: &str) 
    -> Result<Vec<SearchResult>>
```

`&self` je pozajmica (borrow) -- pozivalac zadržava vlasništvo nad engine-om,
a metoda dobija samo privremeni pristup za čitanje. `&str` je pozajmica stringa --
metoda ne preuzima vlasništvo nad upitom.

Povratni tip `Vec<SearchResult>` je u vlasništvu pozivaoca -- engine kreira
nove stringove za fragmente (sa `***` markerima) i pozivalac preuzima vlasništvo
nad njima. Originalni tekstovi dokumenata u engine-u ostaju netaknuti.

**Životni vek (lifetime) referenci u generisanju fragmenata**

Metoda `get_document` vraća pozajmljenu referencu na uskladišteni tekst:

```rust
pub fn get_document(&self, doc_id: i32) -> Option<&String> {
    self.documents.get(&doc_id)
}
```

Vraćena referenca `&String` ima implicitni životni vek vezan za `&self`:
referenca je validna sve dok pozajmica `self`-a traje. Kompajler
sprečava korišćenje te reference nakon što engine prestane da postoji
ili bude menjajuće pozajmljen.

Interno, metode `generate_word_fragments` i `generate_sentence_fragments`
koriste sličan obrazac:

```rust
fn generate_word_fragments(&self, doc_id: i32, ...) -> Vec<String> {
    let text = match self.documents.get(&doc_id) {
        Some(t) => t,           // t: &String, pozajmica iz HashMap-a
        None => return Vec::new(),
    };

    let offsets: &[(u32, u16)] = match self.token_offsets.get(&doc_id) {
        Some(cached) => cached, // cached: &Vec<(u32,u16)>, pozajmica
        None => { ... }
    };

    // text i offsets su reference -- čitamo iz engine-ovih podataka
    // bez kopiranja, ali kreiramo NOVE stringove za fragmente
    let mut fragment_text = text[start..end].trim().to_string();
    //                                              ^^^^^^^^^^^
    //                      to_string() kreira novu alokaciju na heap-u
    // ...
}
```

Ovo je karakterističan Rust obrazac: čitaj pozajmljene podatke, ali
kreiraj novi vlasnik za izlaz. Podaci u engine-u se nikada ne modifikuju
tokom pretraživanja.

**Privremene alokacije u find_phrase_matches**

Frazno pretraživanje kreira privremene kolekcije koje se automatski
oslobađaju na kraju oblasti vidljivosti (scope):

```rust
let mut word_positions: Vec<Vec<(i32, i32)>> = Vec::new();
let mut docs_per_word: Vec<HashSet<i32>> = Vec::new();
// ↑ privremene kolekcije -- žive do kraja search_phrase metode

let mut candidate_docs = docs_per_word[0].clone();
for docs in &docs_per_word[1..] {
    candidate_docs = candidate_docs.intersection(docs).copied().collect();
    // ↑ svaka iteracija kreira novi HashSet; prethodni se automatski oslobađa
}
```

Rust-ov determistički destruktor (RAII obrazac) garantuje da se privremene
alokacije oslobode čim izađu iz oblasti vidljivosti, bez čekanja na
garbage collector ciklus. Ovo je posebno važno za servere sa dugim vremenom
rada, jer sprečava postepeno curenje memorije.

**String u documents vs &str u tokenize**

Mapa `documents` čuva `String` (vlasničku varijantu), dok tokenizer
prima `&str` (pozajmljenu varijantu):

```
documents: HashMap<i32, String>
                         ^^^^^^ heap-alocirani string, engine je vlasnik

tokenizer.tokenize(&text)
                   ^^^^^ &str, referenca na sadržaj String-a
                         → nema kopiranja celog teksta
                         → tokenizer čita iz tuđe memorije
```

Ovo je efikasno jer se tekst dokumenta čuva samo jednom (u `documents` mapi),
a tokenizer samo referiše na njega. Metoda `tokenize` pak kreira nove
`String` objekte za svaki token (jer ih pretvara u lowercase), ali to
je neizbežno jer se normalizovani oblik razlikuje od originala.

### 4.4 Morfološki rečnik

Morfološki rečnik čuva reči sa njihovim gramatičkim oblicima i omogućava pretraživanje
po proizvoljnom obliku reči. Implementiran je u modulima `morphology.rs` i
`morphology_engine.rs`.

#### Tipovi reči

Enum `WordType` definiše sve podržane vrste reči, uključujući srpske i engleske nazive:

| Srpski naziv | Enum varijanta | Engleski ekvivalent |
|-------------|---------------|-------------------|
| Imenica | `Imenica` | Noun |
| Glagol | `Glagol` | Verb |
| Pridev | `Pridev` | Adjective |
| Prilog | `Prilog` | Adverb |
| Zamenica | `Zamenica` | Pronoun |
| Predlog | `Predlog` | Preposition |
| Veznik | `Veznik` | Conjunction |
| Uzvik | `Uzvik` | Interjection |
| Rečca | `Recca` | Particle |
| Broj | `Broj` | Numeral |

Postoji i `Other(String)` varijanta za neprepoznate vrste.

#### MorphologyTrieNode

Za razliku od `TrieNode` koji čuva pozicije tokena, `MorphologyTrieNode` čuva ID-ove reči:

```rust
pub struct MorphologyTrieNode {
    pub children: HashMap<char, Box<MorphologyTrieNode>>,
    pub word_ids: Vec<i32>,
}
```

#### WordEntry

Svaka reč u morfološkom rečniku je predstavljena strukturom `WordEntry`:

```rust
pub struct WordEntry {
    pub id: i32,
    pub original_id: Option<i32>,    // ID iz izvorne baze podataka
    pub base_form: String,           // osnovni oblik (lema)
    pub word_type: WordType,         // vrsta reči
    pub forms: Vec<String>,          // svi gramatički oblici
}
```

#### MorphologyEngine

Engine koristi dva trie stabla -- direktno za prefiksno pretraživanje i obrnuto za sufiksno:

```rust
pub struct MorphologyEngine {
    trie: MorphologyTrieNode,           // prefiksno/tačno pretraživanje
    suffix_trie: MorphologyTrieNode,    // sufiksno pretraživanje
    words: HashMap<i32, WordEntry>,     // svi unosi
    next_id: i32,                       // sledeći slobodan ID
}
```

#### Dijagram odnosa u morfološkom sistemu

```
                ┌───────────────┐
                │  WordEntry    │
                │  id: 1        │
                │  base: "kuća" │
                │  type: Imenica│
                │  forms: [     │
                │    "kuća",    │
                │    "kuće",    │
                │    "kući",    │
                │    "kuću",    │
                │    "kućo",    │
                │    "kućom",   │
                │    "kuće",    │
                │    "kuća",    │
                │    ...        │
                │  ]            │
                └──────┬────────┘
                       │
           svaki oblik se umeće u trie
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
     trie["kuća"]  trie["kuće"]  trie["kući"]  ...
       word_ids: [1]  word_ids: [1]  word_ids: [1]
```

#### Pretraživanje po obliku

Kad korisnik traži oblik "kući", MorphologyEngine:

1. Navigira u trie do čvora "kući"
2. Čita `word_ids` → `[1]`
3. Traži `words[1]` → `WordEntry { base_form: "kuća", ... }`
4. Vraća ceo `WordEntry` sa svim oblicima

Ovo omogućava pretragu po bilo kom padežu, licu ili broju i dobijanje
osnovnog oblika i svih ostalih oblika te reči.

#### Sufiksno pretraživanje

Za pretragu po nastavku (npr. svi glagoli na "-ati"):

```
search_by_suffix("ати")
  → obrni: "ита"
  → navigiraj u suffix_trie
  → prikupi sve word_ids
  → vrati odgovarajuće WordEntry zapise

Rezultat: ["читати", "писати", "певати", ...]
```

### 4.5 Odrednice rečnika

Modul za odrednice (`odrednica.rs` i `odrednica_engine.rs`) omogućava pretraživanje
odrednica iz rečničke baze podataka.

#### Struktura OdrednicaEntry

```rust
pub struct OdrednicaEntry {
    pub id: i32,                     // interni ID
    pub original_id: i32,            // ID iz baze podataka
    pub rec: String,                 // odrednica (reč)
    pub varijante: Vec<String>,      // sve varijante za pretragu
    pub vrsta: i32,                  // vrsta odrednice
    pub rbr_homonima: Option<i32>,   // redni broj homonima
    pub ociscena_rec: String,        // oblik za sortiranje
}
```

#### OdrednicaEngine

```rust
pub struct OdrednicaEngine {
    trie: MorphologyTrieNode,               // prefiksno pretraživanje
    entries: HashMap<i32, OdrednicaEntry>,   // svi zapisi
    next_id: i32,
}
```

Ključna razlika u odnosu na morfološki rečnik je u načinu dodavanja zapisa.
Metoda `add_entry` u trie umeće sve varijante odrednice, a ne samo gramatičke oblike:

```
Odrednica "млеко":
  varijante: ["млеко", "млијеко", "mleko", "mlijeko"]

Svaka varijanta se umeće u trie:
  trie["млеко"] → entry_id
  trie["млијеко"] → entry_id
  trie["mleko"] → entry_id
  trie["mlijeko"] → entry_id
```

Varijante obuhvataju:
- originalni oblik (ćirilica),
- ijekavsku varijantu (ako postoji),
- latiničnu transliteraciju svakog oblika,
- ekspandirane oblike sa zagradama (npr. "бе(с)крајан" → "бекрајан" i "бескрајан").

#### Podrška za homonime

Homonimi su reči istog oblika ali različitog značenja. Sistem ih razlikuje pomoću
polja `rbr_homonima`:

```
коса¹ (kosa - deo tela)   → rbr_homonima: 1
коса² (kosa - alat)       → rbr_homonima: 2
```

Pretraga po prefiksu "кос" vraća obe odrednice.

### 4.6 Naslovi publikacija

Modul za naslove (`naslov.rs` i `naslov_engine.rs`) indeksira publikacije iz korpusa.

#### Struktura NaslovEntry

```rust
pub struct NaslovEntry {
    pub id: i32,              // interni ID
    pub original_id: i32,     // ID iz baze podataka
    pub skracenica: String,   // skraćenica publikacije
    pub opis: String,         // pun opis (autor: naslov)
    pub potkorpus: String,    // naziv potkorpusa
}
```

#### NaslovEngine

```rust
pub struct NaslovEngine {
    trie: MorphologyTrieNode,
    entries: HashMap<i32, NaslovEntry>,
    next_id: i32,
}
```

Prilikom dodavanja zapisa, tekst opisa i skraćenice se tokenizuje po razmacima,
svaka reč se čisti od interpunkcije i umeće u trie:

```
Ulaz:
  skracenica: "Андрић"
  opis: "Андрић, Иво: На Дрини ћуприја Andrić, Ivo: Na Drini ćuprija"

Reči u trie-u:
  "андрић" → entry_id
  "иво" → entry_id
  "на" → entry_id
  "дрини" → entry_id
  "ћуприја" → entry_id
  "andrić" → entry_id
  "ivo" → entry_id
  ...
```

Ovaj pristup omogućava pretragu po bilo kojoj reči iz opisa ili skraćenice,
uključujući i latiničnu varijantu.

### 4.7 Obrada teksta i transliteracija

Modul `text_utils.rs` sadrži funkcije specifične za srpski jezik.

#### Transliteracija ćirilice u latinicu

Funkcija `cyr_to_lat` pretvara tekst sa srpske ćirilice u latinicu:

```
"абсурд" → "absurd"
"Београд" → "Beograd"
"љубав" → "ljubav"
"Њујорк" → "Njujork"
```

Algoritam prvo obrađuje dvoslovne grupe (digrafe):

| Ćirilica | Latinica |
|----------|---------|
| Љ | Lj |
| Њ | Nj |
| Џ | Dž |
| љ | lj |
| њ | nj |
| џ | dž |

Zatim zamenjuje jednoslovna preslikavanja (А→A, Б→B, В→V, Г→G, Д→D, itd.).

#### Uklanjanje interpunkcije

Funkcija `remove_punctuation` zadržava samo Unicode slova i razmake:

```
"а̀бсурд" → "абсурд"    (akcentni znak uklonjen)
"hello-world" → "helloworld"
"реч." → "реч"
```

#### Ekspanzija zagrada

Funkcija `expand_parentheses` generiše varijante za reči sa opcionalnim delovima u zagradama:

```
"бе(с)крајан" → ["бекрајан", "бескрајан"]
"(не)могућ" → ["могућ", "немогућ"]
```

#### Priprema varijanti

Funkcija `prepare_variants` kombajnuje sve prethodno opisane operacije za generisanje
kompletne liste pretraživih varijanti jedne odrednice:

```
Ulaz:
  rec: "млеко"
  ijekavski: "млијеко"
  variant_texts: []

Tok obrade:
  1. Sirove varijante: ["млеко", "млијеко"]
  2. Ekspanzija zagrada: (nema promena)
  3. Uklanjanje interpunkcije: (nema promena)
  4. Dodavanje latiničnih varijanti: ["млеко", "млијеко", "mleko", "mlijeko"]

Izlaz: ["млеко", "млијеко", "mleko", "mlijeko"]
```

---

## 5. REST API server: search-api

Server je implementiran u `search-api/src/main.rs` koristeći Axum radni okvir.

### Stanje aplikacije

Sva četiri engine-a se drže u zajedničkoj strukturi `AppState`:

```rust
#[derive(Clone)]
struct AppState {
    engine: Arc<RwLock<SearchEngine>>,
    morphology: Arc<RwLock<MorphologyEngine>>,
    odrednica: Arc<RwLock<OdrednicaEngine>>,
    naslov: Arc<RwLock<NaslovEngine>>,
}
```

Svaki engine je obmotan u `Arc<RwLock<...>>` za konkurentan pristup (detaljnije u
poglavlju 9).

### Pokretanje servera

Prilikom pokretanja, server:

1. Inicijalizuje tracing sistem (logovanje),
2. Učitava svaki indeks iz binarnog fajla (ako postoji),
3. Kreira `AppState` sa svim engine-ima,
4. Registruje rute i middleware (CORS),
5. Pokreće HTTP listener.

```
Tok pokretanja:

  ┌───────────────────────┐
  │ Čitanje env varijabli │
  │ INDEX_PATH            │
  │ MORPHOLOGY_PATH       │
  │ ODREDNICA_PATH        │
  │ NASLOV_PATH           │
  │ HOST, PORT            │
  └─────────┬─────────────┘
            │
  ┌─────────▼───────────┐
  │ Učitavanje indeksa  │
  │ (deserijalizacija   │
  │  bincode formata)   │
  └─────────┬───────────┘
            │
  ┌─────────▼────────────┐
  │ Kreiranje AppState   │
  │ sa Arc<RwLock<...>>  │
  └─────────┬────────────┘
            │
  ┌─────────▼───────────┐
  │ Registracija ruta   │
  │ + CORS middleware   │
  └─────────┬───────────┘
            │
  ┌─────────▼────────────┐
  │ TcpListener::bind()  │
  │ axum::serve()        │
  └──────────────────────┘
```

Ako neki indeks ne postoji ili ne može da se učita, server startuje sa praznim
engine-om za taj indeks.

### Tabela API endpointa

| Metoda | Putanja | Opis |
|--------|---------|------|
| GET | `/` | Osnovna provera |
| GET | `/health` | Status servera |
| GET | `/health/detailed` | Detaljne statistike |
| GET | `/stats` | Statistike indeksa |
| POST | `/search` | Frazno pretraživanje |
| POST | `/search/multi` | Pretraživanje po više reči |
| GET | `/prefix/:prefix` | Prefiksno pretraživanje |
| GET | `/suffix/:suffix` | Sufiksno pretraživanje |
| GET | `/document/:id` | Dohvatanje dokumenta |
| GET | `/morphology/form/:form` | Pretraga morfologije po obliku |
| GET | `/morphology/prefix/:prefix` | Prefiksna pretraga morfologije |
| GET | `/morphology/suffix/:suffix` | Sufiksna pretraga morfologije |
| GET | `/morphology/stats` | Statistike morfologije |
| GET | `/odrednica/prefix/:prefix` | Prefiksna pretraga odrednica |
| GET | `/odrednica/stats` | Statistike odrednica |
| GET | `/naslov/prefix/:prefix` | Prefiksna pretraga naslova |
| GET | `/naslov/:id` | Dohvatanje naslova po ID-u |
| GET | `/naslov/stats` | Statistike naslova |

### Primeri zahteva i odgovora

#### Frazno pretraživanje

Zahtev:
```json
POST /search
{
    "phrase": "lepa kuća",
    "fragment_size": 20,
    "mode": "word"
}
```

Odgovor:
```json
{
    "query": "lepa kuća",
    "results": [
        {
            "doc_id": 42,
            "metadata": {
                "title": "Primer teksta",
                "author": null
            },
            "fragments": [
                "... stara ***lepa kuća*** stoji na ..."
            ]
        }
    ],
    "total_matches": 1,
    "execution_time_ms": 2.5
}
```

#### Pretraživanje po više reči

Zahtev:
```json
POST /search/multi
{
    "words": ["kuća", "brod", "selo"],
    "fragment_size": 20,
    "mode": "word"
}
```

Odgovor: ista struktura kao frazno pretraživanje, ali se vraćaju dokumenti koji
sadrže bilo koju od zadatih reči.

#### Prefiksno pretraživanje

```
GET /prefix/ku?limit=5
```

Odgovor:
```json
{
    "prefix": "ku",
    "matches": ["kuća", "kupiti", "kum", "kurjak", "kuvati"],
    "total_matches": 5
}
```

#### Morfološka pretraga po obliku

```
GET /morphology/form/kući
```

Odgovor:
```json
{
    "form": "kući",
    "results": [
        {
            "id": 1,
            "original_id": 42,
            "base_form": "kuća",
            "word_type": "imenica",
            "forms": ["kuća", "kuće", "kući", "kuću", "kućom", ...]
        }
    ],
    "total_matches": 1
}
```

### CORS konfiguracija

Server dozvoljava zahteve sa bilo kog porekla:

```rust
CorsLayer::new()
    .allow_origin(Any)
    .allow_methods(Any)
    .allow_headers(Any)
```

---

## 6. CLI alat: search-cli

CLI alat pruža sledeće komande:

### Komande za upravljanje indeksom

| Komanda | Opis |
|---------|------|
| `add` | Dodaje dokument u indeks iz fajla |
| `save` | Čuva indeks na disk |
| `load` | Učitava indeks sa diska |
| `stats` | Prikazuje statistike indeksa |

### Komande za uvoz iz baze

| Komanda | Opis |
|---------|------|
| `reindex` | Reindeksira dokumente iz MySQL baze (korpus) |
| `morph-import` | Uvozi morfološki rečnik iz MySQL baze |
| `odr-import` | Uvozi odrednice iz MySQL baze |
| `naslov-import` | Uvozi naslove publikacija iz MySQL baze |
| `import-all` | Izvršava sve uvozne operacije iz obe baze |

### Komande za morfologiju

| Komanda | Opis |
|---------|------|
| `morph-add` | Ručno dodaje reč u morfološki rečnik |
| `morph-stats` | Prikazuje statistike morfološkog rečnika |
| `morph-search` | Pretražuje reči po obliku |
| `morph-prefix` | Prefiksna pretraga morfologije |

### Komande za odrednice i naslove

| Komanda | Opis |
|---------|------|
| `odr-stats` | Prikazuje statistike odrednica |
| `naslov-stats` | Prikazuje statistike naslova |

### Primer korišćenja

```bash
# Dodavanje dokumenta
./search-cli add --id 1 --file tekst.txt --title "Naslov"

# Reindeksiranje iz baze
./search-cli reindex \
    --host localhost --database korpus \
    --user root --password lozinka \
    --output search_index/search_index.bin --force

# Uvoz svih indeksa
./search-cli import-all \
    --recnik-host recnik-mysql \
    --korpus-host korpus-mysql \
    --force --output-dir search_index
```

---

## 7. Baza podataka i indeksiranje

### Šema baze podataka

Sistem radi sa dve MySQL baze podataka:

#### Baza "korpus"

Koristi se za:
- indeks punog teksta (tabele `publikacije_publikacija` i `publikacije_tekstpublikacije`),
- morfološki rečnik (tabele `reci_*`),
- naslove publikacija.

Ključne tabele za pretraživanje punog teksta:

```
publikacije_publikacija
├── id (INT, PK)
├── naslov (VARCHAR)
├── skracenica (VARCHAR)
├── potkorpus_id (INT, FK)
└── ...

publikacije_tekstpublikacije
├── id (INT, PK)
├── publikacija_id (INT, FK)
├── redni_broj (INT)
└── tekst (TEXT)

publikacije_autor
├── publikacija_id (INT, FK)
├── prezime (VARCHAR)
├── ime (VARCHAR)
└── redni_broj (INT)

publikacije_potkorpus
├── id (INT, PK)
└── naziv (VARCHAR)
```

Tabele za morfologiju (po vrsti reči):

```
reci_imenica                reci_glagol              reci_pridev
├── id                      ├── id                   ├── id
├── nomjed                  ├── infinitiv            ├── lema
├── genjed                  ├── gpp (gl.pr.prošli)   ├── mk... (muški padežni oblici)
├── datjed                  ├── gps (gl.pr.sadašnji) ├── mn... (ženski padežni oblici)
├── akujed                  ├── rgp_mj (radni gl.    ├── mo... (srednji padežni oblici)
├── vokjed                  │   pridev, m.rod, jed.) ├── ...
├── insjed                  ├── ...                  └── ...
├── lokjed                  ├── gpp2
├── nommno                  └── ...
├── genmno
├── datmno                  reci_oblikglagola
├── akumno                  ├── glagol_id (FK)
├── vokmno                  ├── jd1, jd2, jd3
├── insmno                  ├── mn1, mn2, mn3
└── lokmno                  └── ...

reci_varijantaimenice       reci_varijanteglagola
├── imenica_id (FK)         ├── oblik_glagola_id (FK)
├── nomjed, genjed, ...     └── varijanta
└── (isti padežni oblici)

reci_prilog    reci_zamenica    reci_predlog    reci_veznik
├── id         ├── id           ├── id          ├── id
├── pozitiv    ├── nomjed       └── tekst       └── tekst
├── komparativ ├── genjed
└── superlativ ├── datjed       reci_uzvik      reci_recca
               ├── akujed       ├── id          ├── id
               ├── vokjed       └── tekst       └── tekst
               ├── insjed
               └── lokjed       reci_broj
                                ├── id
               reci_varijantazamenice ├── nomjed, ...
               ├── zamenica_id (FK)  └── lokmno
               └── nomjed, ...

               reci_varijantaprideva
               ├── pridev_id (FK)
               └── (padežni oblici po rodu)
```

#### Baza "recnik"

Koristi se za odrednice rečnika:

```
odrednice_odrednica
├── id (INT, PK)
├── rec (VARCHAR)           -- odrednica
├── ijekavski (VARCHAR)     -- ijekavska varijanta
├── vrsta (INT)             -- vrsta odrednice
├── rbr_homonima (INT)      -- redni broj homonima
└── sortable_rec (VARCHAR)  -- normalizovani oblik za sortiranje

odrednice_varijantaodrednice
├── odrednica_id (INT, FK)
├── tekst (VARCHAR)         -- varijanta
├── ijekavski (VARCHAR)     -- ijekavska varijanta varijante
└── redni_broj (INT)        -- redosled
```

### Tok uvoza podataka

Komanda `import-all` izvršava četiri koraka redom:

```
┌───────────────────────────────────────────────┐
│              import-all                       │
│                                               │
│  Korak 1: morphology import (korpus DB)       │
│  ├── Čita iz reci_imenica, reci_glagol, ...   │
│  ├── Uključuje varijante iz reci_varijanta*   │
│  └── Čuva u morphology.bin                    │
│                                               │
│  Korak 2: odrednica import (recnik DB)        │
│  ├── Čita iz odrednice_odrednica              │
│  ├── Dohvata varijante iz odrednice_varijanta │
│  ├── Poziva prepare_variants() za svaku       │
│  └── Čuva u odrednica.bin                     │
│                                               │
│  Korak 3: naslov import (korpus DB)           │
│  ├── Čita iz publikacije_publikacija          │
│  ├── Dohvata autore iz publikacije_autor      │
│  ├── Pravi opis = "Autor: Naslov"             │
│  ├── Dodaje latiničnu transliteraciju         │
│  └── Čuva u naslov.bin                        │
│                                               │
│  Korak 4: full-text reindex (korpus DB)       │
│  ├── Čita dokumente iz publikacije_publikacija│
│  ├── Spaja tekstove iz publikacije_tekstpubl. │
│  └── Čuva u search_index.bin                  │
└───────────────────────────────────────────────┘
```

### Detaljni tok uvoza morfologije

Za svaku vrstu reči, uvoz se odvija po istom obrascu:

```
Imenice:
  1. SELECT id, nomjed, genjed, ... FROM reci_imenica
  2. Za svaki red:
     a. base_form = nomjed (nominativ jednine)
     b. forms = svi neprazni padežni oblici (bez duplikata)
     c. SELECT ... FROM reci_varijantaimenice WHERE imenica_id = ?
     d. Dodaj oblike iz varijanti
     e. engine.add_word_with_original_id(original_id, base_form, Imenica, forms)

Glagoli:
  1. SELECT id, infinitiv, gpp, gps, rgp_mj, ... FROM reci_glagol
  2. Za svaki red:
     a. base_form = infinitiv
     b. forms = infinitiv + gpp + gps + svi radni/trpni glagolski pridevi
     c. SELECT ... FROM reci_oblikglagola WHERE glagol_id = ?
     d. Za svaki oblik: dodaj jd1, jd2, jd3, mn1, mn2, mn3
     e. SELECT varijanta FROM reci_varijanteglagola WHERE oblik_glagola_id = ?
     f. Dodaj varijante oblika
     g. engine.add_word_with_original_id(...)

Pridevi:
  1. SELECT * FROM reci_pridev
  2. base_form = lema
  3. forms = svi stupci čiji naziv počinje sa mk, mn, mo, ms, sk, sp, ss, zk, zp, zs
  4. + varijante iz reci_varijantaprideva

Ostale vrste (prilog, zamenica, predlog, veznik, uzvik, rečca, broj):
  Slična logika sa odgovarajućim tabelama
```

---

## 8. Serijalizacija i perzistencija

Svi engine-i koriste istu strategiju serijalizacije zasnovanu na bincode formatu.

### Obrazac serijalizacije

Svaki engine ima pomoćnu strukturu `Serializable*Engine` koja implementira
`Serialize` i `Deserialize`:

```rust
// Primer za SearchEngine
#[derive(Serialize, Deserialize)]
struct SerializableEngine {
    forward_trie: TrieNode,
    reverse_trie: TrieNode,
    documents: HashMap<i32, String>,
    doc_metadata: HashMap<i32, DocumentMetadata>,
    token_offsets: HashMap<i32, Vec<(u32, u16)>>,
}
```

Razlog za pomoćnu strukturu: sam engine sadrži `Tokenizer` koji koristi kompajlirani
`Regex` -- taj tip ne implementira `Serialize`. Pomoćna struktura izuzima neserijalzabilna
polja, a prilikom deserijalizacije se ona ponovo kreiraju.

### Čuvanje i učitavanje

```
Čuvanje (save):
  Engine → SerializableEngine → bincode::serialize_into → BufWriter → File

Učitavanje (load):
  File → BufReader → bincode::deserialize_from → SerializableEngine → Engine
                                                 (+ rekonstrukcija Tokenizer-a)
```

### Fajlovi indeksa

| Fajl | Engine | Podrazumevana putanja |
|------|--------|-----------------------|
| `search_index.bin` | SearchEngine | `search_index/search_index.bin` |
| `morphology.bin` | MorphologyEngine | `search_index/morphology.bin` |
| `odrednica.bin` | OdrednicaEngine | `search_index/odrednica.bin` |
| `naslov.bin` | NaslovEngine | `search_index/naslov.bin` |

Putanje se konfigurišu putem varijabli okruženja:
- `INDEX_PATH` za indeks pretraživanja
- `MORPHOLOGY_PATH` za morfološki rečnik
- `ODREDNICA_PATH` za odrednice
- `NASLOV_PATH` za naslove

### Napomena o veličini steka

Duboke trie strukture sa velikim brojem dokumenata (100k+) mogu izazvati prekoračenje
steka tokom serijalizacije. Rešenje je pokretanje sa povećanom veličinom steka:

```bash
RUST_MIN_STACK=33554432 ./search-cli reindex ...
```

---

## 9. Konkurentnost i bezbednost niti

Rust-ov sistem tipova pruža garancije bezbednosti konkurentnog pristupa u vreme kompajliranja,
bez runtime troškova. Ovaj odeljak detaljno opisuje kako sistem za pretraživanje koristi
te garancije.

### 9.1 Koncept Send i Sync trait-ova

Rust koristi dva marker trait-a za kontrolu konkurentnog pristupa:

- **`Send`**: Tip se može bezbedno premestiti (move) iz jedne niti u drugu.
- **`Sync`**: Tip se može bezbedno deliti (putem referenci) između niti.

```
Tip T je Sync ako i samo ako je &T Send.
Drugim rečima: ako je referenca na T bezbedna za slanje u drugu nit,
onda je T bezbedan za deljenje.
```

Ovi trait-ovi se automatski implementiraju za većinu tipova. Na primer,
`TrieNode` je `Send + Sync` jer sva njegova polja (`HashMap`, `Vec<i32>`, `bool`)
su `Send + Sync`. Kompajler ovo proverava rekurzivno.

`SearchEngine` je `Send` (može se premestiti u drugu nit), ali pristup iz više
niti zahteva eksplicitnu sinhronizaciju, jer sadrži menjajuće stanje.

### 9.2 Arc<RwLock<T>> obrazac

API server koristi kompozitni omotač `Arc<RwLock<T>>` za svaki engine:

```rust
type SharedEngine = Arc<RwLock<SearchEngine>>;
type SharedMorphology = Arc<RwLock<MorphologyEngine>>;
type SharedOdrednica = Arc<RwLock<OdrednicaEngine>>;
type SharedNaslov = Arc<RwLock<NaslovEngine>>;
```

Svaki sloj ovog omotača ima specifičnu ulogu u upravljanju memorijom i konkurentnošću:

#### Arc (Atomically Reference Counted)

`Arc<T>` je pametni pokazivač sa atomskim brojačem referenci. Omogućava da
više vlasnika deli iste podatke:

```
                    ┌─────────────────────────────┐
                    │         Arc internals        │
                    │  strong_count: AtomicUsize   │──── atomski brojač
                    │  weak_count: AtomicUsize     │
                    │  data: RwLock<SearchEngine>  │──── stvarni podaci
                    └─────────────────────────────┘
                        ▲           ▲           ▲
                        │           │           │
                   Arc::clone   Arc::clone   Arc::clone
                        │           │           │
                   ┌────┴──┐   ┌───┴───┐   ┌──┴────┐
                   │Task 1 │   │Task 2 │   │Task 3 │
                   │(handler)│  │(handler)│  │(handler)│
                   └────────┘  └────────┘  └────────┘
```

Svaki poziv `Arc::clone()` ne kopira podatke -- samo atomski inkrementira
brojač referenci. Ovo je operacija od jednog CPU ciklusa. Kada poslednji
`Arc` izađe iz oblasti vidljivosti, brojač padne na nulu i podaci se
oslobađaju.

Razlika između `Arc` i `Rc` (nebezbedan za niti):
- `Rc` koristi obični brojač -- nije `Send`, ne može se koristiti između niti.
- `Arc` koristi atomski brojač (`AtomicUsize`) -- jeste `Send + Sync`.

U kontekstu Axum servera, `AppState` se klonira za svaki obrađivač zahteva
(handler). Pošto `AppState` sadrži samo `Arc` pokazivače, kloniranje je
jeftino -- kopiraju se samo pokazivači (4 × 8 bajtova), ne cele strukture podataka.

```rust
#[derive(Clone)]          // Clone klonira samo Arc pokazivače
struct AppState {
    engine: Arc<RwLock<SearchEngine>>,       // 8 bajtova (pokazivač)
    morphology: Arc<RwLock<MorphologyEngine>>, // 8 bajtova
    odrednica: Arc<RwLock<OdrednicaEngine>>,   // 8 bajtova
    naslov: Arc<RwLock<NaslovEngine>>,         // 8 bajtova
}
```

#### RwLock (Read-Write Lock)

`RwLock<T>` obezbeđuje sledeća pravila pristupa u runtime-u, analogna
Rust-ovim pravilima pozajmljivanja u vreme kompajliranja:

| Kompajlersko pravilo | RwLock ekvivalent |
|---------------------|-------------------|
| Proizvoljan broj `&T` referenci | `rwlock.read()` -- više čitalaca istovremeno |
| Tačno jedna `&mut T` referenca | `rwlock.write()` -- jedan ekskluzivni pisac |
| Nikada `&T` i `&mut T` istovremeno | `read()` blokira ako postoji `write()` i obrnuto |

```
Scenariji konkurentnog pristupa:

Scenario 1: Tri istovremena čitalačka zahteva (DOZVOLJENO)
  Thread A: rwlock.read() → RwLockReadGuard → čita engine → drop guard
  Thread B: rwlock.read() → RwLockReadGuard → čita engine → drop guard
  Thread C: rwlock.read() → RwLockReadGuard → čita engine → drop guard
  ↑ Sva tri su aktivna istovremeno, bez blokiranja

Scenario 2: Čitalac i pisac (SERIJALIZOVANO)
  Thread A: rwlock.read()  → čita engine → drop guard
  Thread B: rwlock.write() → BLOKIRAN dok A ne završi
                           → dobija ekskluzivni pristup → piše → drop guard

Scenario 3: Dva pisca (SERIJALIZOVANO)
  Thread A: rwlock.write() → piše u engine → drop guard
  Thread B: rwlock.write() → BLOKIRAN dok A ne završi → piše → drop guard
```

#### RAII zaključavanje putem guard objekata

`RwLock::read()` vraća `RwLockReadGuard` -- RAII stražar objekat koji automatski
otpušta zaključavanje kada izađe iz oblasti vidljivosti:

```rust
async fn search(State(state): State<AppState>, Json(req): Json<SearchRequest>)
    -> Result<Json<SearchResponse>, (StatusCode, String)>
{
    let engine = state.engine.read().unwrap();
    //  ^^^^^^                 ^^^^
    //  RwLockReadGuard        Zaključavanje uspešno
    //  (stražar objekat)

    let results = engine.search_phrase(&req.phrase, req.fragment_size, &req.mode)
        .map_err(|e| (StatusCode::BAD_REQUEST, e.to_string()))?;
    //  ↑ engine je i dalje zaključan za čitanje

    // ... kreiranje odgovora ...

    Ok(Json(response))
    // ← engine (RwLockReadGuard) izlazi iz oblasti vidljivosti
    //   → automatski se poziva drop()
    //   → čitalačko zaključavanje se otpušta
}
```

Guard objekat implementira `Deref<Target=T>`, pa se koristi kao da je
direktna referenca na `SearchEngine`. Automatsko otpuštanje zaključavanja
putem destruktora garantuje da se zaključavanje nikada ne zaboravi
osloboditi, čak i u slučaju ranog povratka (early return) ili greške.

Ovo je konkretna primena RAII (Resource Acquisition Is Initialization) obrasca:
resurs (zaključavanje) se stiče u konstruktoru guard objekta i oslobađa u
destruktoru. Kompajler garantuje da se destruktor uvek pozove.

### 9.3 Vlasništvo podataka između CLI i Engine

U CLI alatu, obrazac vlasništva je drugačiji -- nema deljenja između niti.
Jedna nit poseduje engine i sekvencijalno ga koristi:

```rust
fn cmd_reindex(...) -> anyhow::Result<()> {
    let mut engine = SearchEngine::new();     // ekskluzivno vlasništvo
    
    for (doc_id, title) in documents {
        let text = text_parts.join(" ");      // String u vlasništvu lokalne promenljive
        let metadata = DocumentMetadata { ... };
        engine.add_document(doc_id, text, metadata);
        //                         ^^^^  ^^^^^^^^
        //                         move!  move!
        // text i metadata su sada u vlasništvu engine-a
    }
    
    engine.save(output_path)?;                // &self -- pozajmica za čitanje
    // ← engine izlazi iz oblasti vidljivosti → sve se oslobađa
    Ok(())
}
```

Tok vlasništva u CLI:

```
MySQL upit → Vec<(i32, Option<String>)> → vlasništvo u petlji
                                              │
                text_parts.join(" ")  ────────► String (novi vlasnik)
                                              │
                engine.add_document(id, text, meta)
                                         │     │
                                         move   move
                                         │     │
                engine.documents[id] ◄───┘     │
                engine.doc_metadata[id] ◄──────┘
                
engine.save(path) ─── serijalizacija (&self, samo čita) ──► fajl
    │
    ▼
engine drop ──► forward_trie drop ──► rekurzivno oslobađanje čvorova
             ├► reverse_trie drop ──► rekurzivno oslobađanje čvorova
             ├► documents drop ────► oslobađanje svih String-ova
             ├► doc_metadata drop ─► oslobađanje svih metapodataka
             └► token_offsets drop ► oslobađanje svih Vec-ova
```

### 9.4 Tokio runtime i asinhroni model

Server koristi Tokio asinhroni runtime sa `#[tokio::main]` makroom
(sa `features = ["full"]`), što pokreće višenitni runtime:

```rust
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // ...
    let state = AppState {
        engine: Arc::new(RwLock::new(engine)),
        //      ^^^      ^^^^^^      ^^^^^^
        //      │        │           └── engine preuzima vlasništvo
        //      │        └── RwLock preuzima vlasništvo nad engine-om
        //      └── Arc preuzima vlasništvo nad RwLock-om
        // ...
    };
    
    let app = Router::new()
        .route("/search", post(search))
        // ...
        .with_state(state);     // state se premešta u Router
    //                ^^^^^ move -- Router je sada vlasnik AppState

    axum::serve(listener, app).await?;
    // ← app (i sa njim AppState) živi do gašenja servera
    Ok(())
}
```

Tokio runtime kreira skup niti (thread pool) sa podrazumevano onoliko niti koliko
ima CPU jezgara. Svaki dolazni HTTP zahtev postaje Tokio task koji se raspoređuje
na neku od niti.

```
Tokio Thread Pool:
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Thread 0 │  │ Thread 1 │  │ Thread 2 │  │ Thread 3 │
│          │  │          │  │          │  │          │
│ Task A ──│──│──────────│──│──────────│──│──► search │
│ (search) │  │ Task B   │  │ Task C   │  │  handler │
│          │  │ (prefix) │  │ (morph)  │  │          │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └──────────┘
     │             │             │
     └─────────────┼─────────────┘
                   ▼
     Arc<RwLock<SearchEngine>>     ← deljeni podaci
     (svi task-ovi čitaju istovremeno jer koriste read())
```

Ključna prednost: pošto su svi API handleri samo čitalački (koriste `read()` a ne `write()`),
svi zahtevi se izvršavaju paralelno bez ikakvog blokiranja. `RwLock` u praksi funkcioniše
kao da nema zaključavanja, jer čitalačko zaključavanje ne isključuje druge čitaoce.

### 9.5 Bezbednost u vreme kompajliranja

Rust-ov kompajler odbija da kompajlira kod koji krši pravila konkurentnog pristupa.
Na primer, sledeći pokušaji bi rezultovali greškom kompajlera:

```rust
// GREŠKA: pokušaj slanja SearchEngine (bez Arc) u drugu nit
let engine = SearchEngine::new();
tokio::spawn(async move {
    engine.search_phrase("test", 20, "word");
    //     ← ovo bi radilo, ali...
});
engine.search_phrase("test", 20, "word");
//     ← GREŠKA: engine je premešten (moved) u task iznad

// GREŠKA: pokušaj menjajućeg pristupa iz dve niti
let engine = Arc::new(SearchEngine::new());  // Arc ali bez RwLock
let e2 = engine.clone();
tokio::spawn(async move {
    e2.add_document(1, "test".into(), DocumentMetadata::new());
    // GREŠKA: Arc<SearchEngine> ne daje &mut pristup
    //         jer add_document zahteva &mut self
});
```

Jedini način da se zadovolji kompajler je korišćenje `Arc<RwLock<T>>`, čime se
eksplicitno i bezbedno kontroliše pristup. Kompajler ne dozvoljava
prečice -- ne postoji `unsafe` kod u aplikaciji koji bi zaobišao ove garancije.

### 9.6 Memorijski model bez garbage collector-a

Za razliku od jezika sa garbage collector-om (Java, Go, Python), Rust-ov
deterministički model oslobađanja memorije ima specifične prednosti za
server sa dugim vremenom rada:

```
Java/Go model:                     Rust model:
┌─────────────────────┐            ┌─────────────────────┐
│ Alokacija objekta   │            │ Alokacija objekta   │
│         ...         │            │         ...         │
│ Objekat nekorišćen  │            │ Objekat izlazi iz   │
│ (referenca nestaje) │            │ oblasti vidljivosti  │
│         ...         │            │         │            │
│ GC ciklus           │◄── pauza   │ drop() pozvan       │◄── odmah
│ (stop-the-world)    │            │ memorija oslobođena  │
│ memorija oslobođena │            └─────────────────────┘
└─────────────────────┘
```

Prednosti u kontekstu ovog sistema:

1. **Nema GC pauza**: Za pretraživač koji treba da odgovori za milisekunde,
   eliminacija GC pauza garantuje predvidljivu latenciju.

2. **Determinističko oslobađanje**: `RwLockReadGuard` se oslobađa tačno na
   kraju handler funkcije, ne "nekad kada GC odluči". Zaključavanje se
   drži minimalno potrebno vreme.

3. **Nema fragmentacije heap-a**: Rust-ov alokator (jemalloc ili system)
   radi bez preseljenja objekata, jer nema GC koji bi premeštao žive objekte.

4. **Memorijski otisak**: Pošto se privremene alokacije (rezultati pretrage,
   fragmenti, privremeni vektori) oslobađaju odmah po završetku obrade
   zahteva, memorijski otisak servera ne raste tokom vremena.

---

## 10. Docker i produkcijsko okruženje

### Dockerfile

Koristi se višefazna Docker slika:

```
Faza 1: Builder (rust:1.93)
├── Kopiranje Cargo manifestâ
├── Kopiranje izvornog koda
└── cargo build --release

Faza 2: Runtime (debian:trixie-slim)
├── Instalacija: libssl-dev, ca-certificates, curl
├── Kopiranje binarnih fajlova iz builder faze
├── Kreiranje direktorijuma za indekse
├── Podešavanje env varijabli
├── Health check (curl na /health)
└── Entrypoint: entrypoint.sh
```

### Entrypoint logika

```bash
#!/bin/sh
if [ $# -eq 0 ]; then
  exec search-api          # bez argumenata → pokreni API server
else
  exec search-cli "$@"     # sa argumentima → pokreni CLI alat
fi
```

Ovo omogućava korišćenje istog Docker image-a za oba slučaja:
- `docker run rsj/search-engine` → pokreće API server,
- `docker run rsj/search-engine stats` → pokreće CLI komandu.

### Docker Compose

```yaml
services:
  search-api:
    image: rsj/search-engine
    volumes:
      - search-index:/app/search_index
    environment:
      - INDEX_PATH=/app/search_index/search_index.bin
      - HOST=0.0.0.0
      - PORT=9090
    networks:
      - recnik
```

Ključne konfiguracije:
- **Volume `search-index`**: Bind-mount na lokalni `./search_index` direktorijum,
  čime se indeksi čuvaju van kontejnera.
- **Mreža `recnik`**: Eksterna Docker mreža koja povezuje pretraživač sa MySQL bazama
  i ostalim servisima.
- **Health check**: Provera dostupnosti na `/health` svake 30 sekundi.
- **Restart policy**: `unless-stopped` -- kontejner se automatski restartuje.

### Reindeksiranje u produkciji

Skripta `reindex.sh` pokreće privremeni kontejner koji se povezuje na MySQL baze i
izvršava `import-all`:

```bash
docker run \
  --name cmd-reindex \
  --rm \
  --network recnik \
  -v $(pwd)/search_index:/app/search_index \
  rsj/search-engine \
  import-all --recnik-host recnik-mysql --korpus-host korpus-mysql \
             --force --output-dir /app/search_index
```

Nakon završetka, fajlovi indeksa su ažurirani u `search_index/` direktorijumu.
API server ih preuzima prilikom sledećeg restartovanja.

---

## 11. Performanse

### Poređenje sa Python implementacijom

Prema zabeleženim merenjima iz verzije 1.0.0:

| Metrika | Python | Rust | Poboljšanje |
|---------|--------|------|-------------|
| Brzina indeksiranja | - | - | ~60% brže |
| Brzina pretraživanja | - | - | ~2x brže |
| Utrošak memorije | - | - | 20-30% manje |
| Vreme pokretanja | 5-10s | <1s | 5-10x brže |
| Veličina instalacije | pip + zavisnosti | ~15MB binarni fajl | znatno manje |

### Optimizacije u kodu

**Keširanje ofseta tokena**: `token_offsets` mapa čuva precizne bajtovske pozicije
i dužine svakog tokena po dokumentu. Ovo eliminiše potrebu za ponovnom tokenizacijom
prilikom generisanja fragmenata.

```rust
token_offsets: HashMap<i32, Vec<(u32, u16)>>
//                     │          │     │
//                     │          │     └── dužina tokena (u16 = max 65535 bajtova)
//                     │          └──────── početna pozicija (u32 = max ~4GB)
//                     └─────────────────── ID dokumenta
```

Tip `(u32, u16)` zauzima samo 6 bajtova po tokenu, u odnosu na alternativu čuvanja
celih stringova.

**Spajanje fragmenata**: Algoritam `merge_overlapping_ranges` izbegava dupliranje
teksta kada su pogoci bliski.

**BufReader/BufWriter**: Serijalizacija koristi baferisani I/O za minimiziranje
sistemskih poziva.

---

## 12. Testiranje

### Jedinični testovi

Testovi su organizovani po modulima koristeći Rust-ov `#[cfg(test)]` sistem.

#### Testovi za trie (trie.rs)

| Test | Opis |
|------|------|
| `test_insert_and_search` | Umetanje reči i pretraživanje po tačnom obliku |
| `test_collect_words` | Prikupljanje svih reči iz stabla |

#### Testovi za tokenizer (tokenizer.rs)

| Test | Opis |
|------|------|
| `test_tokenize` | Osnovna tokenizacija sa lowercase |
| `test_tokenize_with_positions` | Tokenizacija sa bajtovskim pozicijama |

#### Testovi za morfologiju (morphology.rs)

| Test | Opis |
|------|------|
| `test_word_type_from_str` | Parsiranje vrste reči iz stringa |
| `test_trie_insert_and_search` | Umetanje i tačno pretraživanje u MorphologyTrieNode |
| `test_trie_prefix_search` | Prefiksno pretraživanje |
| `test_multiple_words_same_form` | Homonimi (ista forma, različite reči) |

#### Testovi za MorphologyEngine (morphology_engine.rs)

| Test | Opis |
|------|------|
| `test_add_and_search_word` | Dodavanje reči i pretraga po osnovnom/izvedenom obliku |
| `test_homonyms` | Rad sa homonimima |
| `test_suffix_search` | Sufiksno pretraživanje (srpski primeri: "ати", "ћа") |
| `test_prefix_search` | Prefiksno pretraživanje |

#### Testovi za OdrednicaEngine (odrednica_engine.rs)

| Test | Opis |
|------|------|
| `test_add_and_search_entry` | Pretraga po ćiriličnom i latiničnom prefiksu |
| `test_homonyms` | Homonimne odrednice (npr. "коса"¹ i "коса"²) |
| `test_search_by_variant` | Pretraga po ijekavskoj i latiničnoj varijanti |
| `test_get_entry` | Dohvatanje odrednice po ID-u |
| `test_stats` | Statistike po vrstama |
| `test_empty_prefix_search` | Pretraga sa nepostojećim prefiksom |

#### Testovi za NaslovEngine (naslov_engine.rs)

| Test | Opis |
|------|------|
| `test_add_and_search` | Pretraga po reči iz opisa i skraćenice |
| `test_no_results` | Pretraga bez rezultata |
| `test_multiple_entries` | Pretraga sa više publikacija |
| `test_get_entry_by_original_id` | Dohvatanje po izvornom ID-u |
| `test_stats` | Provera statistika |

#### Testovi za text_utils (text_utils.rs)

| Test | Opis |
|------|------|
| `test_remove_punctuation` | Uklanjanje interpunkcije i akcentnih znakova |
| `test_cyr_to_lat` | Transliteracija ćirilice u latinicu |
| `test_expand_parentheses` | Ekspanzija opcionalnih delova u zagradama |
| `test_prepare_variants` | Kompletna priprema varijanti |
| `test_prepare_variants_with_ijekavski` | Varijante sa ijekavskim oblicima |

### Pokretanje testova

```bash
# Svi testovi
cargo test

# Testovi jednog crate-a
cargo test -p search-engine

# Konkretan test
cargo test -p search-engine test_suffix_search
```

---

## 13. Istorija razvoja

Sistem se razvijao kroz nekoliko verzija, dokumentovanih u `CHANGELOG.md`:

### Verzija 1.0.0 (17. oktobar 2025.)

Inicijalno izdanje sa osnovnim funkcionalnostima:
- Trie-bazirano pretraživanje punog teksta
- Forward i reverse trie za prefiksno/sufiksno pretraživanje
- Frazno pretraživanje sa isticanjem pogodaka
- REST API (Axum) i CLI (Clap)
- MySQL reindeksiranje
- Binarna serijalizacija (bincode)
- Docker podrška

### Verzija 1.1.0 (18. oktobar 2025.)

Dodata podrška za pretraživanje po više reči (`POST /search/multi`), gde se rezultati
pojedinačnih pretraga kombinuju (OR logika).

### Verzija 1.2.0 (18. oktobar 2025.)

Uveden morfološki rečnik:
- Novi moduli: `morphology.rs`, `morphology_engine.rs`
- CLI komande: `morph-add`, `morph-stats`, `morph-search`, `morph-prefix`, `morph-import`
- API endpointi: `/morphology/form/:form`, `/morphology/prefix/:prefix`, `/morphology/stats`
- Trie-bazirano skladištenje sa podrškom za homonime

### Verzija 1.2.1 (18. oktobar 2025.)

Ispravljen kritičan bag sa konfliktom ID-ova pri uvozu iz više tabela.
Dodata podrška za srpske vrste reči (Imenica, Glagol, Pridev, itd.).

### Verzija 1.2.2 (19. oktobar 2025.)

Dodato čuvanje originalnog ID-a iz baze podataka (`original_id` polje u `WordEntry`),
čime je omogućena sledljivost unosa do izvorne baze.

### Verzija 1.2.3 (19. oktobar 2025.)

Ispravljen kritičan problem prekoračenja steka pri čuvanju velikih indeksa.
Save operacije se sada izvršavaju u niti sa 32MB steka.

### Naknadne verzije

Dodati su moduli za odrednice (`odrednica.rs`, `odrednica_engine.rs`), naslove
(`naslov.rs`, `naslov_engine.rs`), pomoćne funkcije za obradu teksta (`text_utils.rs`),
komanda `import-all` za skupni uvoz, i podrška za pravila hifenacije.

---

## 14. Zaključak

Pretraživač korpusa srpskog jezika je sistema specifične namene, dizajniran da efikasno
radi sa lingvističkim podacima srpskog jezika. Ključne karakteristike arhitekture su:

1. **Trie kao osnovna struktura**: Omogućava brzo prefiksno, sufiksno i tačno pretraživanje
   sa složenošću proporcionalnom dužini reči, a ne veličini vokabulara.

2. **Četiri nezavisna engine-a**: Svaki pokriva drugi aspekt lingvističkog sistema
   (pun tekst, morfologija, odrednice, naslovi) i može se nezavisno ažurirati.

3. **Podrška za srpski jezik**: Transliteracija ćirilica-latinica, ekavsko-ijekavski
   oblici, padežni oblici za sve promenljive vrste reči, ekspanzija zagrada u
   odrednicama.

4. **Brza perzistencija**: Bincode serijalizacija omogućava učitavanje indeksa za
   manje od sekunde, u poređenju sa 5-10 sekundi za prethodnu Python implementaciju.

5. **Produkcijska spremnost**: Docker podrška, health check endpointi, konfigurisanje
   putem varijabli okruženja, CORS podrška, strukturirano logovanje.

6. **Dvoslojna arhitektura**: Čista biblioteka (`search-engine`) ne zavisi od veb
   radnog okvira niti baze podataka, čime se obezbeđuje testabilnost i mogućnost
   ponovne upotrebe u drugim kontekstima.
