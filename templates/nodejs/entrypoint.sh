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
    "extensions.ignoreRecommendations": true,
    "javascript.updateImportsOnFileMove.enabled": "always",
    "javascript.validate.enable": false,
    "eslint.enable": false
}
EOF

# Silent background extension installation (Node.js essentials)
(
    # Wait for server to be ready
    while ! curl -s http://localhost:8080 >/dev/null; do sleep 1; done

    # Install extensions silently (no loop used)
    code-server --install-extension dbaeumer.vscode-eslint >/dev/null 2>&1
    code-server --install-extension esbenp.prettier-vscode >/dev/null 2>&1
    code-server --install-extension ms-vscode.vscode-typescript-next >/dev/null 2>&1
) &


# Start code-server in the background
echo "Starting code-server on port 8080..."
code-server --bind-addr=0.0.0.0:8080 --auth=none /home/coder/workspace &

# Helpful info
echo "Access VS Code at: http://localhost:8080"
echo "Installed packages:"
npm list -g --depth=0 | grep -E "(nodemon|typescript|create-react-app|nestjs|express-generator)"

# Keep container alive
tail -f /dev/null