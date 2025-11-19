"""Configuration settings for the app"""
import os
from pathlib import Path

APP_NAME = "NoteStack"
APP_VERSION = "1.0.2"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
MAX_NOTE_LENGTH = 5000

def get_app_data_dir() -> str:
    """Get application data directory based on platform"""
    if os.name == 'nt':  # Windows
        appdata = os.getenv('APPDATA', str(Path.home() / 'AppData' / 'Roaming'))
    else:  # Linux/Mac
        appdata = os.path.expanduser('~/.config')
    
    app_dir = Path(appdata) / APP_NAME
    return str(app_dir)

DATA_DIR = get_app_data_dir()
NOTES_FILE = os.path.join(DATA_DIR, "notes.json")

