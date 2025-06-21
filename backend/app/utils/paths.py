from pathlib import Path

# SnapSpace/ root directory
BASE_DIR = Path(__file__).resolve().parents[3]

# Subdirectories
BACKEND_DIR = BASE_DIR / "backend"
TEMPLATE_DIR = BASE_DIR / "templates"
NGINX_DIR = BASE_DIR / "nginx"
SCRIPTS_DIR = BASE_DIR / "scripts"