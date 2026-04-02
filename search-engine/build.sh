#!/bin/bash
set -e

echo "================================================================================  "
echo "Building Rust Search Engine"
echo "================================================================================"

# Check if Rust is installed
if ! command -v cargo &> /dev/null; then
    echo "✗ Cargo not found. Please install Rust from https://rustup.rs/"
    exit 1
fi

echo "✓ Cargo found: $(cargo --version)"

# Build all components
echo ""
echo "→ Building all components in release mode..."
cargo build --release

echo ""
echo "================================================================================  "
echo "BUILD COMPLETE"
echo "================================================================================"
echo "Binaries created:"
echo "  - ./target/release/search-cli"
echo "  - ./target/release/search-api"
echo ""
echo "Next steps:"
echo "  1. Create search index directory: mkdir -p search_index"
echo "  2. Add a document: ./target/release/search-cli add --id 1 --file test.txt"
echo "  3. Start API: ./target/release/search-api"
echo "================================================================================"
