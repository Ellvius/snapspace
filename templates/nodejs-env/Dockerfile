# Node.js-specific stage
FROM node:18-slim AS node-runtime

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        sudo \
    && rm -rf /var/lib/apt/lists/*

# Copy from builder
COPY --from=builder /usr/bin/code-server /usr/bin/code-server
COPY --from=builder /usr/lib/code-server /usr/lib/code-server

# Create a non-root user
RUN useradd --create-home --shell /bin/bash --groups sudo coder && \
    echo "coder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Install global npm packages
RUN npm install -g nodemon typescript ts-node

# Switch to non-root user
USER coder
WORKDIR /home/coder/workspace

# Copy startup files
COPY --chown=coder:coder sample/ /home/coder/workspace/
COPY --chown=coder:coder entrypoint.sh /home/coder/
RUN chmod +x /home/coder/entrypoint.sh

# Expose ports
EXPOSE 8080 3000 5000

# Set entrypoint
ENTRYPOINT [ "/home/coder/entrypoint.sh" ]