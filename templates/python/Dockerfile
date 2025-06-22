FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Install code-server
RUN curl -fsSL https://code-server.dev/install.sh | sh

# Create a non-root user
RUN useradd --create-home --shell /bin/bash --groups sudo coder && \
    echo "coder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Install necessary python packages
RUN pip install --no-cache-dir \
    requests \
    pytest \
    black \
    flake8 \
    ipython

# Switch to non-root user
USER coder
WORKDIR /home/coder/workspace

# Copy sample files into the workspace directory
COPY --chown=coder:coder sample/ /home/coder/workspace/

# Copy and set up entrypoint script
COPY --chown=coder:coder entrypoint.sh /home/coder/
RUN chmod +x /home/coder/entrypoint.sh

# Expose ports
EXPOSE 8080 8000 5000

# Set entrypoint
ENTRYPOINT [ "/home/coder/entrypoint.sh" ]