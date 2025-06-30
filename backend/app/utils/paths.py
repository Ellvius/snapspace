from pathlib import Path

# SnapSpace/ root directory
BASE_DIR = Path(__file__).resolve().parents[3]

# Subdirectories
BACKEND_DIR = BASE_DIR / "backend"
TEMPLATE_DIR = BASE_DIR / "templates"
TRAEFIK_DIR = BASE_DIR / "traefik"
SCRIPTS_DIR = BASE_DIR / "scripts"