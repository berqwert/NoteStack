"""Configuration settings for the app"""
import os
from pathlib import Path

APP_NAME = "NoteStack"
APP_VERSION = "1.0.2"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
MAX_NOTE_LENGTH = 5000

def get_app_data_dir() -> Path:
    """Get application data directory based on platform (returns Path object to avoid redirection)"""
    if os.name == 'nt':  # Windows
        # Use actual user profile path instead of APPDATA env (which can be redirected by Windows Store Python)
        appdata = Path.home() / 'AppData' / 'Roaming'
    else:  # Linux/Mac
        appdata = Path.home() / '.config'
    
    app_dir = appdata / APP_NAME
    return app_dir

# Centralized path management - all paths as Path objects
# All file operations should use these Path objects to avoid Windows Store Python redirection
DATA_DIR: Path = get_app_data_dir()
NOTES_FILE: Path = DATA_DIR / "notes.json"
KEY_FILE: Path = DATA_DIR / ".key"

