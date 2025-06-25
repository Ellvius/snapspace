# Shared builder stage
FROM debian:bullseye-slim AS builder

# System dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    sudo \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install code-server
RUN curl -fsSL https://code-server.dev/install.sh | sh