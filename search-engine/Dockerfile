FROM rust:1.93 AS builder

WORKDIR /app

# Copy manifests
COPY Cargo.toml Cargo.lock* ./
COPY search-engine/Cargo.toml ./search-engine/
COPY search-cli/Cargo.toml ./search-cli/
COPY search-api/Cargo.toml ./search-api/

# Copy source code
COPY search-engine/src ./search-engine/src
COPY search-cli/src ./search-cli/src
COPY search-api/src ./search-api/src

# Build release binaries
RUN cargo build --release

# Runtime stage
FROM debian:trixie-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libssl-dev \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy binaries from builder
COPY --from=builder /app/target/release/search-api /usr/local/bin/
COPY --from=builder /app/target/release/search-cli /usr/local/bin/

# Create search index directory
RUN mkdir -p /app/search_index /app/backups

# Environment variables
ENV INDEX_PATH=/app/search_index/search_index.bin
ENV HOST=0.0.0.0
ENV PORT=9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:9090/health || exit 1

EXPOSE 9090

COPY entrypoint.sh /usr/local/bin/
ENTRYPOINT ["entrypoint.sh"]
