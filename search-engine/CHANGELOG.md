# Changelog

All notable changes to this project will be documented in this file.

## [1.2.3] - 2025-10-19

### Fixed
- **Critical**: Fixed stack overflow when saving large indexes
  - Save operations now run in dedicated thread with 32MB stack (up from 2MB default)
  - Uses raw pointers to avoid expensive cloning of large structures
  - Prevents crash with deep trie structures on large datasets (100k+ docs/words)
  - Applies to both document search index and morphology dictionary

### Changed
- All save operations now use 32MB stack thread without cloning overhead
- Removed unnecessary `Clone` trait implementations

### Performance
- For persistent stack overflow: Set `RUST_MIN_STACK=33554432` environment variable
- See PERFORMANCE_TROUBLESHOOTING.md for debugging slow indexing issues

## [1.2.2] - 2025-10-19

### Added
- **Original database ID preservation**: Database IDs now stored as metadata in `original_id` field
- `add_word_with_original_id()` method to preserve database IDs during import
- CLI output now displays both engine ID and original database ID: `[ID: 1] [DB ID: 42]`
- API responses include `original_id` field in word entries

### Changed
- `WordEntry` struct now includes optional `original_id: Option<i32>` field
- Import process preserves original database IDs while using auto-generated unique IDs internally
- Better traceability: can now map back to original database records

## [1.2.1] - 2025-10-18

### Fixed
- **Critical**: Fixed ID conflicts when importing from multiple database tables with separate ID sequences
  - Changed `morph-import` to use auto-generated IDs instead of database IDs
  - Each word type (noun, verb, adj) had separate ID sequences causing overwrites
  - Now uses `engine.add_word()` which auto-generates unique IDs across all types

### Added
- **Serbian word type support** for morphology system:
  - `Imenica` (noun)
  - `Glagol` (verb)
  - `Pridev` (adjective)
  - `Prilog` (adverb)
  - `Zamenica` (pronoun)
  - `Predlog` (preposition)
  - `Veznik` (conjunction)
  - `Uzvik` (interjection)
  - `Recca` (particle)
  - `Broj` (numeral)
- Serbian word types work alongside English types in the same system

## [1.2.0] - 2025-10-18

### Added
- **Major Feature**: Morphological dictionary system for word forms and grammatical information
- **New module**: `morphology.rs` - Word types, entries, and trie structure
- **New module**: `morphology_engine.rs` - Engine for managing morphological data
- **CLI commands**:
  - `morph-add` - Add word with base form, type, and grammatical forms
  - `morph-stats` - Show morphology dictionary statistics
  - `morph-search` - Search for words by any grammatical form
  - `morph-prefix` - Prefix search for autocomplete functionality
  - `morph-import` - Import words from MySQL database
- **API endpoints**:
  - `GET /morphology/form/:form` - Find words by exact form
  - `GET /morphology/prefix/:prefix` - Find words by prefix (autocomplete)
  - `GET /morphology/stats` - Morphology dictionary statistics
- **Features**:
  - Trie-based storage for efficient lookups
  - Support for multiple word types (noun, verb, adjective, etc.)
  - Homonym support (same form, different words)
  - Binary serialization for fast loading
  - Separate data file (`morphology.bin`)
- **Documentation**: Comprehensive morphology guide (MORPHOLOGY.md)

### Changed
- API state now includes morphology engine alongside document search
- Environment variable `MORPHOLOGY_PATH` for morphology dictionary location (default: `data/morphology.bin`)

### Fixed
- Removed unused import warnings in `morphology_engine.rs` and `search-api/src/main.rs`
- Fixed MySQL query in `morph-import` to use `query_map` for proper type inference
- Project compiles with zero warnings and zero errors

## [1.1.0] - 2025-10-18

### Added
- **New endpoint**: `POST /search/multi` - Multi-word search that combines results from multiple single-word searches
- Each word is searched independently and results are merged
- Documents matching any word are included once with all matching fragments
- New documentation: `MULTI_WORD_SEARCH.md` with comprehensive examples and use cases

### Changed
- API now supports both phrase search (exact matching) and multi-word search (OR-style matching)

## [1.0.3] - 2025-10-18

### Fixed
- **Critical**: Removed CLI code that was accidentally in `search-api/src/main.rs`
- API server now contains only web server code (no clap, no mysql imports in API)
- Fixed compilation errors in search-api
- Project now compiles cleanly with zero errors and zero warnings

## [1.0.2] - 2025-10-18

### Fixed
- Fixed unused variable warning in `cmd_save` function (prefixed with underscore)
- Project now compiles with zero warnings

## [1.0.1] - 2025-10-17

### Fixed
- Added `DocumentMetadata` to public exports in `search-engine/src/lib.rs`
- Now correctly exports: `SearchEngine`, `SearchResult`, `DocumentMetadata`, `TrieNode`
- Added `Default` derive to `DocumentMetadata` for cleaner initialization

### Changed
- `DocumentMetadata::new()` now uses `Self::default()` implementation

## [1.0.0] - 2025-10-17

### Added
- Initial release of Rust Search Engine
- Complete trie-based search engine implementation
- Forward trie for prefix/exact search
- Reverse trie for suffix search
- Phrase search with hit highlighting
- Word and sentence fragment modes
- Fragment merging for overlapping matches
- Case-insensitive search with preserved formatting
- REST API server with Axum
- CLI tool for document management
- MySQL database reindexing support
- Binary serialization with bincode
- Docker and Docker Compose support
- Comprehensive documentation
- Unit tests
- Build and setup scripts

### Features
- Full-text phrase search
- Prefix search (autocomplete)
- Suffix search (word endings)
- Hit highlighting with `***` markers
- Multiple fragment modes
- Thread-safe concurrent operations
- Health checks and statistics
- Progress tracking for large datasets
- Memory-optimized data structures

### Performance
- 60% faster indexing than Python version
- 2x faster search queries
- 20-30% less memory usage
- <1s startup time vs 5-10s for Python
- Single 15MB binary deployment
