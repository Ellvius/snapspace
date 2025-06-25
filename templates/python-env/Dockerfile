# Python-specific stage
FROM python:3.11-slim AS python-runtime

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

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

# Copy startup files
COPY --chown=coder:coder sample/ /home/coder/workspace/
COPY --chown=coder:coder entrypoint.sh /home/coder/
RUN chmod +x /home/coder/entrypoint.sh

# Expose ports
EXPOSE 8080 8000 5000

# Set entrypoint
ENTRYPOINT [ "/home/coder/entrypoint.sh" ]