# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run

```bash
# Build all crates (release)
cargo build --release

# Build a single crate
cargo build -p search-engine --release

# Run all tests
cargo test

# Run tests for a single crate
cargo test -p search-engine

# Run a single test by name
cargo test -p search-engine test_name

# Start the API server (default 0.0.0.0:9090)
./target/release/search-api

# Docker build & run
docker compose up --build
```

## Environment Variables

- `INDEX_PATH` — search index file (default: `search_index/search_index.bin`)
- `MORPHOLOGY_PATH` — morphology dictionary (default: `search_index/morphology.bin`)
- `ODREDNICA_PATH` — dictionary entries index (default: `search_index/odrednica.bin`)
- `NASLOV_PATH` — publication titles index (default: `search_index/naslov.bin`)
- `HOST` / `PORT` — API bind address (default: `0.0.0.0:9090`)
- `RUST_LOG` — tracing filter (default: `search_api=info,tower_http=debug`)

## Architecture

Cargo workspace with three crates:

- **search-engine** — core library, no I/O dependencies beyond filesystem. Contains four independent engine types, each with its own trie-based index and bincode serialization:
  - `SearchEngine` (engine.rs) — full-text phrase search over documents. Uses forward + reverse tries, stores documents and token offsets. Supports phrase search with `***` hit highlighting, prefix/suffix word search, multi-word OR search, and word/sentence fragment modes.
  - `MorphologyEngine` (morphology_engine.rs) — morphological dictionary mapping word forms to base forms and grammatical info. Uses its own `MorphologyTrieNode`.
  - `OdrednicaEngine` (odrednica_engine.rs) — dictionary headword (odrednica) lookup with prefix search.
  - `NaslovEngine` (naslov_engine.rs) — publication title/abbreviation lookup with prefix search.

- **search-api** — Axum REST server. Holds all four engines in `AppState` as `Arc<RwLock<...>>`. Loads serialized `.bin` files at startup; runs with an empty engine if files are missing.

- **search-cli** — Clap-based CLI. Key commands: `add`, `reindex` (from MySQL), `import-all` (bulk import from two MySQL databases: recnik + korpus), `morph-*` and `odr-*` subcommands for morphology/odrednica management.

## Domain Context

This is a search engine for a Serbian language dictionary project (RSJ — Rečnik srpskoga jezika). The codebase handles Serbian-specific concerns:
- Cyrillic-to-Latin transliteration (`text_utils::cyr_to_lat`)
- Serbian grammatical word types in `morphology.rs` (Imenica, Glagol, Pridev, etc.)
- Hyphenation rules (`text_utils`)
- Field names use Serbian terminology: `rec` (word), `odrednica` (headword), `naslov` (title), `skracenica` (abbreviation), `potkorpus` (subcorpus), `vrsta` (type)

## Reindexing

Full reindex from MySQL databases runs via Docker:
```bash
./reindex.sh
```
This uses the `import-all` CLI command connecting to `recnik-mysql` and `korpus-mysql` hosts on the `recnik` Docker network.
