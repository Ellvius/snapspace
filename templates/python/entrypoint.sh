#!/bin/bash

# Set up code-server configuration
mkdir -p /home/coder/.config/code-server
cat > /home/coder/.config/code-server/config.yaml << EOF
bind-addr: 0.0.0.0:8080
auth: none
cert: false
disable-telemetry: true
EOF

# Configure user preferences with all settings in one go
mkdir -p /home/coder/.local/share/code-server/User
cat > /home/coder/.local/share/code-server/User/settings.json << EOF
{
    "workbench.colorTheme": "Default Dark Modern",
    "window.autoDetectColorScheme": true,
    "workbench.preferredDarkColorTheme": "Default Dark Modern",
    "workbench.startupEditor": "none",
    "security.workspace.trust.enabled": false,
    "python.analysis.showStartupMessages": false,
    "extensions.ignoreRecommendations": true,
    "python.linting.flake8Enabled": false,
    "python.linting.enabled": false
}
EOF

# Silent background extension installation
(
    # Wait for server to be ready
    while ! curl -s http://localhost:8080 >/dev/null; do sleep 1; done
    
    # Install extensions silently
    for ext in ms-python.python ms-python.flake8 ms-python.black-formatter; do
        code-server --install-extension "$ext" >/dev/null 2>&1
    done
) &

# Start code-server in the background
echo "Starting code-server on port 8080..."
code-server --bind-addr=0.0.0.0:8080 --auth=none /home/coder/workspace &

# Helpful info
echo "Access VS Code at: http://localhost:8080"
echo "Installed packages:"
pip list | grep -E "(fastapi|uvicorn|black|flake8)"

# Keep container alive
tail -f /dev/null