# Rust Document Search Engine

A high-performance, memory-efficient document search engine written in Rust with support for:

- Full-text phrase search with hit highlighting
- Multi-word search (combines results from multiple words)
- Prefix search (words starting with...)
- Suffix search (words ending with...)
- Morphological dictionary (word forms and grammatical information)
- Autocomplete support (prefix-based word suggestions)
- Case-insensitive matching with preserved formatting
- RESTful API server
- MySQL database reindexing
- Serialized index for fast startup

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [CLI Commands](#cli-commands)
- [API Endpoints](#api-endpoints)
- [Multi-Word Search](#multi-word-search)
- [Morphological Dictionary](#morphological-dictionary)
- [Configuration](#configuration)
- [Docker Deployment](#docker-deployment)
- [Performance](#performance)
- [Development](#development)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Verification Checklist](#verification-checklist)
- [Comparison with Python Version](#comparison-with-python-version)
- [Project Stats](#project-stats)
- [Learning Resources](#learning-resources)
- [License](#license)

## Features

### Search Capabilities

- Full-text phrase search
- Prefix search (autocomplete)
- Suffix search (word endings)
- Multi-word OR-style search
- Hit highlighting with `***` markers
- Case-insensitive with preserved formatting
- Word and sentence fragment modes
- Overlapping fragment merging

### Production Features

- REST API with Axum
- MySQL database reindexing
- Docker and Docker Compose support
- Health checks (Kubernetes ready)
- Thread-safe concurrent operations (`Arc<RwLock<SearchEngine>>`)
- Binary serialization for fast loading
- Progress tracking for large datasets
- Comprehensive logging (tracing framework)
- CORS support
- Error handling with Result types
- Environment configuration

## Project Structure

```
rust-search-engine/
├── Cargo.toml              # Workspace configuration
├── Dockerfile              # Production Docker image
├── docker-compose.yml      # Docker Compose setup
├── build.sh                # Build script
├── test-build.sh           # Test and verify build
├── quickstart.sh           # Quick setup script
├── search-engine/          # Core search engine library
│   ├── Cargo.toml
│   └── src/
│       ├── lib.rs          # Library exports
│       ├── trie.rs         # Trie data structure
│       ├── tokenizer.rs    # Text tokenization
│       └── engine.rs       # Main search engine
├── search-cli/             # Command-line interface
│   ├── Cargo.toml
│   └── src/
│       └── main.rs
└── search-api/             # REST API server
    ├── Cargo.toml
    └── src/
        └── main.rs
```

### Core Library (`search-engine/`)

- **lib.rs** — Public API exports and error type definitions
- **trie.rs** — `TrieNode` structure with word insertion, search (exact, prefix, suffix), position collection, and vocabulary counting
- **tokenizer.rs** — Regex-based tokenization with token extraction, positions, and lowercase normalization
- **engine.rs** — `SearchEngine` main implementation: document addition, phrase search with highlighting, word/sentence fragment generation, fragment merging, suffix/prefix search, serialization/deserialization, and statistics

### CLI Tool (`search-cli/`)

- Clap argument parsing with commands: `add`, `stats`, `reindex`
- MySQL connection handling, progress tracking, error handling

### API Server (`search-api/`)

- Axum web framework with routes for health, search, prefix, suffix, document retrieval, and stats
- Request/response models, CORS configuration, logging setup

## Prerequisites

- **Rust 1.75+** — install from https://rustup.rs/
- **MySQL/MariaDB** (optional) — for database reindexing
- **Docker** (optional) — for containerized deployment

### Installing Rust

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

Verify installation:

```bash
rustc --version
cargo --version
```

### Installing MySQL (optional)

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install mysql-server libmysqlclient-dev

# macOS
brew install mysql

# Fedora
sudo dnf install mysql-server mysql-devel
```

## Quick Start

### Automated Setup

```bash
chmod +x quickstart.sh
./quickstart.sh
```

This creates a data directory, generates a test document, builds the project, and adds the test document to the index.

Then start the API:

```bash
./target/release/search-api
```

The server starts on http://localhost:8000

### Manual Setup

#### 1. Build the project

```bash
# Build all components
cargo build --release

# Or build specific components
cargo build -p search-engine --release
cargo build -p search-cli --release
cargo build -p search-api --release
```

#### 2. Create data directory

```bash
mkdir -p data
```

#### 3. Create and add a test document

```bash
cat > test.txt << EOF
The quick brown fox jumps over the lazy dog.
This sentence contains every letter of the English alphabet.
The lazy dog was sleeping peacefully under the old oak tree.
EOF

./target/release/search-cli add \
    --id 1 \
    --file test.txt \
    --title "Test Document" \
    --author "Your Name"
```

Expected output:

```
✓ Loading existing index from "data/search_index.bin"
✓ Added document: 1
✓ Index saved to "data/search_index.bin"

Statistics:
  num_documents: 1
  total_chars: 168
  vocabulary_size: 27
```

#### 4. Start the API server

```bash
./target/release/search-api
```

Expected output:

```
INFO search_api: Loading index from data/search_index.bin
INFO search_api: ✓ Index loaded successfully
INFO search_api: Starting server on 0.0.0.0:8000
```

#### 5. Test the API

```bash
# Search for a phrase
curl -X POST http://localhost:8000/search \
    -H "Content-Type: application/json" \
    -d '{"phrase": "lazy dog", "fragment_size": 20, "mode": "word"}'

# Multi-word search
curl -X POST http://localhost:8000/search/multi \
    -H "Content-Type: application/json" \
    -d '{"words": ["quick", "lazy", "fox"], "fragment_size": 20}'

# Prefix search
curl http://localhost:8000/prefix/qui

# Suffix search
curl http://localhost:8000/suffix/ing

# Get statistics
curl http://localhost:8000/stats
```

## CLI Commands

### Add Document

```bash
./target/release/search-cli add \
    --id <DOC_ID> \
    --file <FILE_PATH> \
    --title "Document Title" \
    --author "Author Name" \
    --index data/search_index.bin
```

### Show Statistics

```bash
./target/release/search-cli stats --index data/search_index.bin
```

### Reindex from MySQL

```bash
./target/release/search-cli reindex \
    --host localhost \
    --port 3306 \
    --database mydb \
    --user root \
    --password secret \
    --output data/search_index.bin \
    --force
```

Options:

- `--force` — Overwrite existing index
- `--limit <N>` — Limit to N documents (for testing)

For large databases, progress is shown:

```
================================================================================
DATABASE REINDEXING
================================================================================
Database: mydb@localhost:3306
Output:   "data/search_index.bin"
================================================================================

→ Connecting to database...
✓ Connected to database

→ Counting documents...
✓ Found 10000 documents

→ Indexing documents...
  Progress: 1000/10000 (10.0%) | Speed: 245.3 docs/sec | ETA: 6.1 min
  Progress: 2000/10000 (20.0%) | Speed: 248.1 docs/sec | ETA: 5.4 min
  ...
```

## API Endpoints

### Health & Status

- `GET /` — Basic health check
- `GET /health` — Health status with index loaded flag
- `GET /health/detailed` — Detailed health information
- `GET /stats` — Search engine statistics

### Search

#### Phrase Search — `POST /search`

Request body:

```json
{
  "phrase": "search query or ~suffix",
  "fragment_size": 20,
  "mode": "word"
}
```

Response:

```json
{
  "query": "lazy dog",
  "total_matches": 2,
  "execution_time_ms": 1.23,
  "results": [
    {
      "doc_id": 1,
      "metadata": {
        "title": "Fox Story",
        "author": null
      },
      "fragments": [
        "... over the ***lazy dog***. The fox ..."
      ]
    }
  ]
}
```

Use `~` prefix for suffix search in phrases:

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"phrase": "~ing"}'
```

#### Multi-Word Search — `POST /search/multi`

Request body:

```json
{
  "words": ["quick", "lazy", "fox"],
  "fragment_size": 20,
  "mode": "word"
}
```

Response:

```json
{
  "words": ["quick", "lazy", "fox"],
  "total_matches": 2,
  "execution_time_ms": 2.45,
  "results": [
    {
      "doc_id": 1,
      "metadata": {
        "title": "Fox Story",
        "author": null
      },
      "fragments": [
        "The ***quick*** brown fox jumps over ...",
        "... over the ***lazy*** dog. The fox ...",
        "... brown ***fox*** jumps over the ..."
      ]
    }
  ]
}
```

**Note**: The multi-word endpoint performs separate single-word searches and merges results. Documents appear once even if they match multiple words, with all matching fragments included.

### Word Discovery

- `GET /prefix/{prefix}?limit=10` — Find words starting with prefix
- `GET /suffix/{suffix}?limit=10` — Find words ending with suffix

### Document Retrieval

- `GET /document/{id}` — Get full document text by ID

### Morphological Dictionary

- `GET /morphology/form/{form}` — Find words by grammatical form
- `GET /morphology/prefix/{prefix}?limit=10` — Prefix search for autocomplete
- `GET /morphology/stats` — Morphology dictionary statistics

See the [Morphological Dictionary](#morphological-dictionary) section below for full documentation, CLI commands, and integration examples.

## Multi-Word Search

The `/search/multi` endpoint allows you to search for multiple words simultaneously and combines the results into a single response. Each word is searched independently, and documents matching any of the words are included.

### How It Works

1. **Searches each word independently** — each word is a separate single-word query
2. **Merges results** — documents matching any word are included
3. **Deduplicates documents** — a document appears only once even if it matches multiple words
4. **Combines fragments** — all matching fragments from all words are included per document
5. **Sorts consistently** — results sorted by document ID

### Multi-Word vs Phrase Search

| Feature | Multi-Word (`/search/multi`) | Phrase (`/search`) |
|---------|-------|--------|
| Word location | Anywhere in document | Adjacent, in exact order |
| Order | Doesn't matter | Must match exactly |
| Match logic | OR (any word) | AND (exact phrase) |
| Highlighting | Each word separately | Entire phrase |

### Advanced Options

```bash
# With custom fragment size
curl -X POST http://localhost:8000/search/multi \
  -H "Content-Type: application/json" \
  -d '{"words": ["programming", "rust"], "fragment_size": 30}'

# Sentence mode
curl -X POST http://localhost:8000/search/multi \
  -H "Content-Type: application/json" \
  -d '{"words": ["database", "index"], "fragment_size": 20, "mode": "sentence"}'
```

### Use Cases

- **Topic-based search** — find documents about a topic using related keywords
- **Entity search** — find documents mentioning specific people or entities
- **Multi-language keywords** — search using synonyms or translations
- **Troubleshooting** — search across different error messages or symptoms

### Integration Examples

**Python:**

```python
import requests

response = requests.post(
    "http://localhost:8000/search/multi",
    json={
        "words": ["rust", "programming", "systems"],
        "fragment_size": 25
    }
)
data = response.json()
for result in data['results']:
    print(f"Document {result['doc_id']}: {result['metadata']['title']}")
    for fragment in result['fragments']:
        print(f"  - {fragment}")
```

**JavaScript:**

```javascript
const response = await fetch('http://localhost:8000/search/multi', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    words: ['rust', 'programming', 'systems'],
    fragment_size: 25
  })
});
const data = await response.json();
data.results.forEach(result => {
  console.log(`Document ${result.doc_id}: ${result.metadata.title}`);
  result.fragments.forEach(f => console.log(`  - ${f}`));
});
```

**Rust:**

```rust
let client = reqwest::Client::new();
let response = client
    .post("http://localhost:8000/search/multi")
    .json(&serde_json::json!({
        "words": ["rust", "programming", "systems"],
        "fragment_size": 25
    }))
    .send()
    .await?;
let data: serde_json::Value = response.json().await?;
println!("Found {} documents", data["total_matches"]);
```

### Performance Notes

- Proportional to the number of words searched
- Results cached per word, so duplicate words don't add overhead
- Typically 1-5ms per word
- Best practice: keep the word list under 10 words

### Error Handling

- Empty word list returns `400 Bad Request — "No words provided"`
- Invalid mode falls back to default "word" mode gracefully

## Morphological Dictionary

The morphological dictionary system stores and searches words with their grammatical forms. It is useful for building autocomplete features, spell checkers, lemmatizers, and morphological analyzers.

### Data Structure

Each word entry contains:

```json
{
  "id": 1,
  "original_id": 42,
  "base_form": "run",
  "word_type": "verb",
  "forms": ["runs", "running", "ran"]
}
```

- **id** — Auto-generated unique engine ID (no conflicts across word types)
- **original_id** — Original database ID preserved for traceability (`null` for manually added words)
- **base_form** — Dictionary form (lemma)
- **word_type** — Part of speech
- **forms** — All inflected/derived forms

### Supported Word Types

**English:** noun, verb, adjective, adverb, pronoun, preposition, conjunction, interjection, article, numeral, participle

**Serbian:** imenica (noun), glagol (verb), pridev (adjective), prilog (adverb), zamenica (pronoun), predlog (preposition), veznik (conjunction), uzvik (interjection), recca (particle), broj (numeral)

Custom types are also accepted (stored as `WordType::Other("custom-type")`).

### CLI Commands

#### Add a Word

```bash
./target/release/search-cli morph-add \
    --base "run" \
    --word-type "verb" \
    --forms "runs,running,ran,runner"
```

#### Search by Form

```bash
./target/release/search-cli morph-search --form "running"
```

Output:

```
Found 1 word(s) for form 'running':

  [ID: 1] run (verb)
    Forms: runs, running, ran, runner
```

For imported words, the output includes the database ID:

```
  [ID: 1] [DB ID: 42] pas (imenica)
    Forms: pas, psa, psu, psom, ...
```

#### Prefix Search (Autocomplete)

```bash
./target/release/search-cli morph-prefix --prefix "run" --limit 10
```

#### Show Statistics

```bash
./target/release/search-cli morph-stats
```

#### Import from MySQL

```bash
./target/release/search-cli morph-import \
    --host localhost \
    --database lexicon \
    --user root \
    --password secret \
    --table words \
    --force
```

Expected table structure:

```sql
CREATE TABLE words (
    id INT PRIMARY KEY,
    base_form VARCHAR(255) NOT NULL,
    word_type VARCHAR(50) NOT NULL,
    forms TEXT  -- comma-separated
);
```

Import uses auto-generated IDs internally to avoid conflicts when importing from multiple tables with separate ID sequences. The original database IDs are preserved in the `original_id` field for traceability.

### API Endpoints

#### Search by Form

```bash
curl http://localhost:8000/morphology/form/running
```

Response:

```json
{
  "form": "running",
  "total_matches": 1,
  "results": [
    {
      "id": 1,
      "original_id": 42,
      "base_form": "run",
      "word_type": "verb",
      "forms": ["runs", "running", "ran", "runner"]
    }
  ]
}
```

`original_id` is `null` for words not imported from a database.

#### Prefix Search (Autocomplete)

```bash
curl "http://localhost:8000/morphology/prefix/run?limit=10"
```

#### Statistics

```bash
curl http://localhost:8000/morphology/stats
```

### Homonym Support

The system supports words that share the same form but have different meanings:

```bash
# Add "leave" verb
./target/release/search-cli morph-add --base "leave" --word-type "verb" --forms "left,leaving,leaves"

# Add "left" adjective
./target/release/search-cli morph-add --base "left" --word-type "adjective" --forms "lefter,leftest"

# Search for "left" — returns both
curl http://localhost:8000/morphology/form/left
```

Response includes both words:

```json
{
  "form": "left",
  "total_matches": 2,
  "results": [
    {"id": 1, "base_form": "leave", "word_type": "verb", "forms": ["left", "leaving", "leaves"]},
    {"id": 2, "base_form": "left", "word_type": "adjective", "forms": ["lefter", "leftest"]}
  ]
}
```

### Use Cases and Integration

#### Autocomplete (JavaScript)

```javascript
async function autocomplete(prefix) {
  const response = await fetch(
    `http://localhost:8000/morphology/prefix/${prefix}?limit=10`
  );
  const data = await response.json();
  return data.results.map(word => ({
    text: word.base_form,
    type: word.word_type,
    forms: word.forms
  }));
}
```

#### Spell Checker (Python)

```python
import requests

def check_word(word):
    response = requests.get(f"http://localhost:8000/morphology/form/{word}")
    return response.json()['total_matches'] > 0
```

#### Lemmatization (Python)

```python
def get_lemma(word_form):
    response = requests.get(f"http://localhost:8000/morphology/form/{word_form}")
    return [w['base_form'] for w in response.json()['results']]

# get_lemma("running") -> ["run"]
```

#### Rust Integration

```rust
use search_engine::MorphologyEngine;

let engine = MorphologyEngine::load("data/morphology.bin")?;

let words = engine.search_by_form("running");
for word in words {
    println!("{} ({})", word.base_form, word.word_type.to_string());
}

let words = engine.search_by_prefix("run");
println!("Found {} words", words.len());
```

#### Database Traceability

Query the morphology dictionary, then look up details in the original database:

```python
response = requests.get("http://localhost:8000/morphology/form/psu")
word = response.json()["results"][0]

original_id = word["original_id"]  # 42
word_type = word["word_type"]       # "imenica"

# Query original database for full details
cursor.execute(f"SELECT * FROM reci_imenica WHERE id = %s", (original_id,))
```

### Morphology Performance

- **Exact form search**: <1ms
- **Prefix search**: 1-5ms (depends on matches)
- **Database import**: ~1000 words/second
- **Storage**: ~100-200 bytes per word, ~1-2 MB per 10,000 words

### Best Practices

- Organize by language: `MORPHOLOGY_PATH=data/morphology_en.bin`
- Create separate dictionaries for different domains (medical, legal, general)
- Limit autocomplete results: `?limit=10`
- Backup before import: `cp data/morphology.bin data/morphology.backup.bin`

### Morphology Troubleshooting

**Dictionary not loading:**

```bash
ls -lh data/morphology.bin
RUST_LOG=debug ./target/release/search-api
```

**No results found:**

```bash
./target/release/search-cli morph-search --form "test"
./target/release/search-cli morph-stats
```

**Import errors:**

```bash
# Test with limit first
./target/release/search-cli morph-import --host localhost --limit 10 ...

# Check table structure
mysql> DESCRIBE words;
```

## Configuration

### Environment Variables

For the API server:

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Bind address |
| `PORT` | `8000` | Port number |
| `INDEX_PATH` | `data/search_index.bin` | Path to index file |
| `MORPHOLOGY_PATH` | `data/morphology.bin` | Path to morphology dictionary |

For CLI (large datasets):

| Variable | Default | Description |
|----------|---------|-------------|
| `RUST_MIN_STACK` | system default | Stack size in bytes (set to `33554432` for 32MB to prevent overflow with large indexes) |

Example:

```bash
# API server
INDEX_PATH=/path/to/index.bin \
MORPHOLOGY_PATH=/path/to/morphology.bin \
PORT=3000 \
./target/release/search-api

# CLI with large datasets
RUST_MIN_STACK=33554432 ./target/release/search-cli reindex ...
```

## Docker Deployment

### Build and Run

```bash
docker build -t search-engine .
docker run -p 8000:8000 -v $(pwd)/data:/app/data search-engine
```

### Dockerfile

```dockerfile
FROM rust:1.75 as builder

WORKDIR /app
COPY . .

RUN cargo build --release

FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    libssl-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/target/release/search-api /usr/local/bin/
COPY --from=builder /app/target/release/search-cli /usr/local/bin/

RUN mkdir -p /app/data

ENV INDEX_PATH=/app/data/search_index.bin
ENV HOST=0.0.0.0
ENV PORT=8000

EXPOSE 8000

CMD ["search-api"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  search-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - INDEX_PATH=/app/data/search_index.bin
      - HOST=0.0.0.0
      - PORT=8000
    restart: unless-stopped

  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=secret
      - MYSQL_DATABASE=mydb
    volumes:
      - mysql-data:/var/lib/mysql
    ports:
      - "3306:3306"

volumes:
  mysql-data:
```

Run:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f search-api

# Reindex from MySQL
docker-compose exec search-api search-cli reindex \
    --host mysql \
    --port 3306 \
    --database mydb \
    --user root \
    --password secret \
    --force

# Stop services
docker-compose down
```

### Docker Resource Requirements

- **Memory**: at least 4GB for building
- **Disk**: at least 10GB
- Adjust in Docker Desktop under Preferences > Resources

## Performance

### Benchmarks (180k documents)

| Metric | Python | Rust | Improvement |
|--------|--------|------|-------------|
| Memory | 12 GB | 8-10 GB | 20-30% less |
| Indexing Speed | 200-250 docs/sec | 300-500 docs/sec | 60% faster |
| Search Speed | 5-10ms | <5ms | 2x faster |
| Startup Time | 5-10s | <1s | 10x faster |
| Binary Size | N/A | ~15 MB | Single binary |

### Search Speed

- Exact word: <1ms
- Phrase (2-3 words): 1-5ms
- Phrase (5+ words): 5-20ms
- Suffix search: 1-10ms (depends on matches)
- Prefix/Suffix discovery: <1ms

### Index Size

Approximately 1-2 MB per 1,000 documents (binary serialization).

| Documents | Index Size | RAM Usage |
|-----------|-----------|-----------|
| 1,000 | ~1-2 MB | ~100 MB |
| 10,000 | ~10-20 MB | ~500 MB |
| 100,000 | ~100-200 MB | ~5 GB |
| 1,000,000 | ~1-2 GB | ~50 GB |

### Key Optimizations

- `Vec<i32>` for document IDs (32-bit integers)
- `HashMap<char, Box<TrieNode>>` for trie children
- Binary serialization with `bincode`
- No garbage collection overhead
- Compile-time optimizations via LLVM
- Zero-copy where possible
- Stack allocation for hot paths

## Development

### Running Tests

```bash
# Run all tests
cargo test

# Run tests for specific package
cargo test -p search-engine

# Run with output
cargo test -- --nocapture

# Run specific test
cargo test --lib test_name -- --nocapture
```

### Running with Logging

```bash
# Enable debug logging
RUST_LOG=debug ./target/release/search-api

# Enable trace logging for specific module
RUST_LOG=search_engine=trace ./target/release/search-api

# Full verbose logging with backtrace
RUST_LOG=trace RUST_BACKTRACE=full ./target/release/search-api
```

### Code Formatting

```bash
cargo fmt

# Check without modifying
cargo fmt -- --check
```

### Linting

```bash
cargo clippy

# Treat warnings as errors
cargo clippy -- -D warnings
```

### Generate Documentation

```bash
cargo doc --open

# Without dependencies
cargo doc --no-deps --open
```

## Advanced Features

### Custom Fragment Size

Adjust how much context to show around matches:

```bash
# Small fragments (10 words)
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"phrase": "lazy dog", "fragment_size": 10}'

# Large fragments (50 words)
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"phrase": "lazy dog", "fragment_size": 50}'
```

### Sentence Mode

Show complete sentences instead of fixed word count:

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"phrase": "lazy dog", "mode": "sentence"}'
```

### Custom Tokenization

Modify `search-engine/src/tokenizer.rs` to implement custom tokenization rules.

### Stop Words

Add stopword filtering in `engine.rs`:

```rust
const STOPWORDS: &[&str] = &["the", "a", "an", "in", "on", "at"];

// Skip stopwords during indexing
if !STOPWORDS.contains(&token.as_str()) {
    self.forward_trie.insert_word(&token, doc_id, position as i32);
}
```

### Compression

The index uses `bincode` for efficient binary serialization. For additional compression, wrap with gzip:

```rust
use flate2::write::GzEncoder;
use flate2::Compression;

// In engine.save()
let file = File::create(path)?;
let encoder = GzEncoder::new(file, Compression::default());
let writer = BufWriter::new(encoder);
```

## Troubleshooting

### Build Issues

#### "unresolved import `search_engine::DocumentMetadata`"

Fixed in v1.0.1. Verify `search-engine/src/lib.rs` contains:

```rust
pub use engine::{SearchEngine, SearchResult, DocumentMetadata};
```

#### "linking with `cc` failed" / "cannot find -lmysqlclient"

Install MySQL development libraries:

```bash
# Ubuntu/Debian
sudo apt-get install libmysqlclient-dev

# Fedora/RHEL
sudo dnf install mysql-devel

# macOS
brew install mysql

# Arch Linux
sudo pacman -S mariadb-libs
```

#### "cargo: command not found"

Install Rust:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

#### Build takes forever / uses too much memory

```bash
# Build with single thread (uses less memory)
cargo build --release -j 1

# Or set environment variable
export CARGO_BUILD_JOBS=1
cargo build --release
```

If needed, increase swap space:

```bash
# Linux — create 4GB swap file
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Runtime Issues

#### "Address already in use (os error 98)"

Port 8000 is already in use:

```bash
# Find and kill the process
sudo lsof -i :8000
sudo kill -9 <PID>

# Or use a different port
PORT=8080 ./target/release/search-api
```

#### Index file not found

Normal on first run. The engine starts empty. Add documents to create the index:

```bash
mkdir -p data
./target/release/search-cli add --id 1 --file test.txt
```

#### MySQL connection refused

```bash
# Check MySQL is running
sudo systemctl status mysql    # Linux
brew services list             # macOS

# Start if needed
sudo systemctl start mysql     # Linux
brew services start mysql      # macOS

# Verify credentials
mysql -h localhost -u root -p

# Check bind address in /etc/mysql/mysql.conf.d/mysqld.cnf
# Change to: bind-address = 0.0.0.0
# Then restart: sudo systemctl restart mysql
```

#### "thread 'main' panicked"

```bash
# Run with backtrace
RUST_BACKTRACE=1 ./target/release/search-api

# Run with debug logging
RUST_LOG=debug ./target/release/search-api

# Check disk space
df -h
```

#### Stack overflow during save

Bincode's recursive serialization of deep trie structures can exceed stack limits on large datasets (100k+ docs/words). Fixed in v1.2.3 — save operations now run in a dedicated thread with 32MB stack.

If stack overflow persists:

```bash
# Increase stack for the entire process
RUST_MIN_STACK=33554432 ./target/release/search-cli reindex ...

# Or increase further to 64MB
RUST_MIN_STACK=67108864 ./target/release/search-cli reindex ...
```

#### Out of memory during indexing

```bash
# Index in batches
./target/release/search-cli reindex ... --limit 10000

# Increase system limits
ulimit -v 16777216  # 16GB

# Use Docker with memory limit
docker run -m 16g search-engine
```

#### Index corruption

Remove and rebuild:

```bash
rm data/search_index.bin
# Rebuild with reindex command or re-add documents
```

### Docker Issues

#### Docker build fails at "cargo build"

1. Build locally first to verify: `cargo build --release`
2. Check Docker resources (Docker Desktop > Preferences > Resources): at least 4GB memory, 10GB disk
3. Verbose build: `docker build --progress=plain -t search-engine .`

#### "docker-compose up" fails

```bash
# Build each service separately
docker-compose build search-api
docker-compose build mysql

# Check Docker Compose version (should be v2.0+)
docker-compose --version

# Try Docker Compose V2 syntax
docker compose up  # no hyphen
```

### Performance Issues

#### Searches are slow (>100ms)

1. Make sure you're using a **release build** (debug builds are 10-100x slower):

   ```bash
   cargo build --release
   ./target/release/search-api
   ```

2. Check if `finalize_index()` is called after adding documents
3. Limit results or use pagination for queries with many matches

#### Slow indexing

| Possible Cause | Diagnosis | Fix |
|----------------|-----------|-----|
| Debug build | `./target/debug/` in path | Use `cargo build --release` |
| Network latency | `time mysql ... -e "SELECT ... LIMIT 1000"` | Use localhost, check network |
| Disk I/O bottleneck | `iostat -x 1` shows high %util | Use SSD, save to /tmp first |
| Memory pressure | `vmstat 1` shows swapping | Increase RAM, reduce batch size |
| Debug logging | `RUST_LOG=trace` set | Remove or set to `info` |

#### Profiling

```bash
# Install flamegraph
cargo install flamegraph

# Profile the reindex
cargo flamegraph --bin search-cli -- reindex \
    --host localhost \
    --database your_db \
    --user root \
    --password secret \
    --limit 1000

# Open flamegraph.svg to see where time is spent
```

#### Expected indexing performance

| Dataset Size | Indexing Speed | Save Time | Total Time |
|--------------|----------------|-----------|------------|
| 100 docs | ~100 docs/sec | <1 sec | ~2 sec |
| 1,000 docs | ~200 docs/sec | ~1 sec | ~6 sec |
| 10,000 docs | ~300 docs/sec | ~5 sec | ~40 sec |
| 100,000 docs | ~400 docs/sec | ~30 sec | ~5 min |

Assumes release build, SSD, localhost database, and sufficient RAM.

#### Recommended workflow for large datasets (10k+)

```bash
# 1. Build in release mode
cargo build --release

# 2. Set larger stack
export RUST_MIN_STACK=33554432

# 3. Reindex
./target/release/search-cli reindex \
    --host localhost \
    --database your_db \
    --user root \
    --password secret \
    --output data/search_index.bin
```

#### High memory usage

```bash
# Check index size
ls -lh data/search_index.bin

# Rebuild index to compact
rm data/search_index.bin
./target/release/search-cli reindex ...
```

### Development Issues

#### Cargo check shows errors

```bash
cargo update         # Update dependencies
cargo clean          # Clean build artifacts
cargo build --release

# Verify Rust version (need 1.75+)
rustc --version
rustup update        # Update if needed
```

## Verification Checklist

Use this to verify the project is complete and working.

### File Verification

```bash
# Core library
[ -f search-engine/Cargo.toml ]
[ -f search-engine/src/lib.rs ]
[ -f search-engine/src/trie.rs ]
[ -f search-engine/src/tokenizer.rs ]
[ -f search-engine/src/engine.rs ]

# CLI
[ -f search-cli/Cargo.toml ]
[ -f search-cli/src/main.rs ]

# API
[ -f search-api/Cargo.toml ]
[ -f search-api/src/main.rs ]

# Config
[ -f Cargo.toml ]
[ -f Dockerfile ]
[ -f docker-compose.yml ]

# Scripts
[ -x build.sh ]
[ -x test-build.sh ]
[ -x quickstart.sh ]
```

### Build Verification

```bash
cargo check              # Syntax check (fast)
cargo test --lib         # Run tests
cargo build --release    # Build release binaries
ls -lh target/release/search-cli target/release/search-api  # ~15 MB each
```

### Functionality Verification

```bash
# Setup
mkdir -p data
echo "The quick brown fox jumps over the lazy dog." > test.txt

# Add document
./target/release/search-cli add --id 1 --file test.txt

# Verify index created
ls -lh data/search_index.bin

# Start API
./target/release/search-api &
API_PID=$!
sleep 2

# Test endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"phrase":"lazy dog"}'
curl http://localhost:8000/prefix/qui
curl http://localhost:8000/stats

# Cleanup
kill $API_PID
```

### Code Quality

```bash
cargo fmt -- --check     # Format check
cargo clippy -- -D warnings  # Lint check
cargo test --all-features    # All tests
cargo doc --no-deps          # Generate docs
```

### Export Verification

```bash
grep "pub use engine" search-engine/src/lib.rs
```

Must include: `SearchEngine`, `SearchResult`, `DocumentMetadata`

### Quick Automated Verification

```bash
./test-build.sh
```

## Comparison with Python Version

| Feature | Python | Rust |
|---------|--------|------|
| Memory (180k docs) | 12 GB | 8-10 GB |
| Indexing Speed | 200-250 docs/sec | 300-500 docs/sec |
| Search Speed | 5-10ms | <5ms |
| Startup Time | 5-10s | <1s |
| Binary Size | N/A | ~15 MB |
| Deployment | Requires Python runtime | Single binary |
| Type Safety | Runtime errors | Compile-time |
| Memory Safety | Manual | Guaranteed |
| Concurrency | GIL limited | True parallelism |

## Project Stats

| Metric | Value |
|--------|-------|
| Lines of Code | ~1,500 (Rust) |
| Source Size | ~100 KB |
| Build Time | 2-5 minutes |
| Binary Size | ~15 MB each |
| Dependencies | 15 crates |
| Unit Tests | 6 included |

### Dependencies

- **serde 1.0** — Serialization framework
- **bincode 1.3** — Binary serialization
- **regex 1.10** — Regular expressions
- **axum 0.7** — Web framework
- **tokio 1.35** — Async runtime
- **mysql 25.0** — MySQL connector
- **clap 4.5** — CLI argument parsing
- **anyhow 1.0** — Error handling
- **tracing 0.1** — Logging

### Build Artifacts

```
target/release/
├── search-cli         [~15 MB] - CLI executable
├── search-api         [~15 MB] - API server executable
└── libsearch_engine.* [~5 MB]  - Shared library
```

### Index Files (Runtime)

```
search_index/
└── search_index.bin   [varies] - ~1-2 MB per 1,000 documents
```

### Quick Commands

```bash
cargo build --release       # Build everything
cargo test                  # Run tests
cargo doc --open            # Generate documentation
cargo fmt                   # Format code
cargo clippy                # Lint code
cargo check                 # Check without building
cargo clean                 # Clean build artifacts
cargo update                # Update dependencies
./target/release/search-cli --help   # Run CLI
./target/release/search-api          # Run API
docker-compose up                    # Run with Docker
docker build -t search-engine .      # Create production build
```

## Learning Resources

This project uses clean, idiomatic Rust and is suitable for learning:

- Real-world data structures (tries)
- Web APIs with Axum
- Async programming with Tokio
- Database access with MySQL
- CLI tools with Clap
- Error handling patterns
- Testing practices

### External Resources

- **Rust Book**: https://doc.rust-lang.org/book/
- **Rust by Example**: https://doc.rust-lang.org/rust-by-example/
- **Axum Docs**: https://docs.rs/axum/
- **Tokio**: https://tokio.rs/
- **Serde**: https://serde.rs/
- **Project Code Docs**: `cargo doc --open`

## License

MIT License

## Contributing

Contributions are welcome! Please submit pull requests or open issues on GitHub.

## Support

For questions or issues:

- **Troubleshooting**: See the [Troubleshooting](#troubleshooting) section above
- **Version history**: See [CHANGELOG.md](CHANGELOG.md)
- **Code documentation**: Run `cargo doc --open`

---

**Version**: 1.2.3
**Status**: Production Ready
**Language**: Rust 1.75+
**License**: MIT
