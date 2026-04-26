"""TODO: description du module."""

from pathlib import Path

VERSION = "2.3.0"
APP_NAME = "AutoClaude"

# Paths
ROOT_DIR = Path(__file__).parent.parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
ASSET_YES_PNG = ASSETS_DIR / "yes.png"
ASSET_LOGO_PNG = ASSETS_DIR / "Icone AutoClaude.png"
ASSET_LOGO_ICO = ASSETS_DIR / "Icone AutoClaude.ico"

# URLs
URL_WEBSITE = "https://serenia-tech.fr"
URL_GITHUB = "https://github.com/ServOMorph/AutoClaude"

# UI — palette SéréniaTech
COLOR_BG = "#1a202c"
COLOR_BG_SECONDARY = "#2d3748"
COLOR_PRIMARY = "#A5C9CA"
COLOR_SUCCESS = "#48BB78"
COLOR_WARNING = "#DB7857"
COLOR_TEXT = "#E2E8F0"
COLOR_TEXT_MUTED = "#718096"
COLOR_BORDER = "#4A5568"

# Window
WINDOW_WIDTH = 520
WINDOW_HEIGHT = 980

# Defaults
DEFAULT_INTERVAL = 0.5

# Overlay flottant
OVERLAY_WIDTH = 120
OVERLAY_HEIGHT = 40
OVERLAY_MARGIN = 20
OVERLAY_ALPHA = 0.8
OVERLAY_COLOR_ACTIVE = "#e74c3c"    # Rouge
OVERLAY_COLOR_INACTIVE = "#2ecc71"  # Vert
OVERLAY_TEXT_COLOR = "#ffffff"
