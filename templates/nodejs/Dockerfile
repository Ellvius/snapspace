FROM node:18-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Install code-server (VS Code in browser)
RUN curl -fsSL https://code-server.dev/install.sh | sh

# Create a non-root user
RUN useradd --create-home --shell /bin/bash --groups sudo coder && \
    echo "coder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Install essential global npm packages
RUN npm install -g \
    nodemon \
    typescript \
    ts-node

# Switch to non-root user
USER coder
WORKDIR /home/coder/workspace

# Copy sample files into the workspace directory
COPY --chown=coder:coder sample/ /home/coder/workspace/

# Copy and set up entrypoint script
COPY --chown=coder:coder entrypoint.sh /home/coder/
RUN chmod +x /home/coder/entrypoint.sh

# Expose ports
EXPOSE 8080 3000 5000

# Set the entrypoint
ENTRYPOINT ["/home/coder/entrypoint.sh"]