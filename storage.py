"""Note storage operations"""
import json
import os
from typing import List
from models import Note
from config import DATA_DIR, NOTES_FILE


def ensure_data_dir():
    """Create data directory"""
    os.makedirs(DATA_DIR, exist_ok=True)


def load_notes() -> List[Note]:
    """
    Load notes
    
    Returns:
        List of Note objects
    """
    ensure_data_dir()
    
    if not os.path.exists(NOTES_FILE):
        return []
    
    try:
        with open(NOTES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Note.from_dict(note_dict) for note_dict in data]
    except (json.JSONDecodeError, IOError, KeyError):
        return []


def save_notes(notes: List[Note]):
    """
    Save notes
    
    Args:
        notes: List of Note objects to save
    """
    ensure_data_dir()
    
    try:
        notes_data = [note.to_dict() for note in notes]
        with open(NOTES_FILE, 'w', encoding='utf-8') as f:
            json.dump(notes_data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"Error saving notes: {e}")

