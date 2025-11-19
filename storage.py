"""Note storage operations"""
import json
import os
from typing import List
from models import Note
from config import DATA_DIR, NOTES_FILE
from encryption import encrypt_data, decrypt_data, get_or_create_key


def ensure_data_dir():
    """Create data directory"""
    os.makedirs(DATA_DIR, exist_ok=True)


def _migrate_old_data() -> List[Note]:
    """Migrate notes from old project directory to new app data directory"""
    old_data_dir = "data"
    old_notes_file = os.path.join(old_data_dir, "notes.json")
    old_key_file = os.path.join(old_data_dir, ".key")
    
    if not os.path.exists(old_notes_file):
        return []
    
    notes = []
    try:
        with open(old_notes_file, 'rb') as f:
            encrypted_data = f.read()
        decrypted_json = decrypt_data(encrypted_data)
        data = json.loads(decrypted_json)
        notes = [Note.from_dict(note_dict) for note_dict in data]
    except Exception:
        try:
            with open(old_notes_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                notes = [Note.from_dict(note_dict) for note_dict in data]
        except (json.JSONDecodeError, IOError, KeyError):
            return []
    
    # Migrate key file if exists
    if notes and os.path.exists(old_key_file):
        ensure_data_dir()
        try:
            with open(old_key_file, 'rb') as f:
                key_data = f.read()
            new_key_file = os.path.join(DATA_DIR, ".key")
            with open(new_key_file, 'wb') as f:
                f.write(key_data)
        except Exception:
            pass
    
    return notes


def load_notes() -> List[Note]:
    """
    Load notes (encrypted, with backward compatibility and migration)
    
    Returns:
        List of Note objects
    """
    ensure_data_dir()
    
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_json = decrypt_data(encrypted_data)
            data = json.loads(decrypted_json)
            return [Note.from_dict(note_dict) for note_dict in data]
        except Exception:
            try:
                with open(NOTES_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    notes = [Note.from_dict(note_dict) for note_dict in data]
                    # Auto-migrate: save encrypted version (using internal save)
                    if notes:
                        _save_notes_encrypted(notes)
                    return notes
            except (json.JSONDecodeError, IOError, KeyError):
                pass
    
    old_notes = _migrate_old_data()
    if old_notes:
        _save_notes_encrypted(old_notes)
        return old_notes
    
    return []


def _save_notes_encrypted(notes: List[Note]):
    """Internal function to save notes encrypted (prevents recursion)"""
    ensure_data_dir()
    try:
        notes_data = [note.to_dict() for note in notes]
        json_str = json.dumps(notes_data, ensure_ascii=False, indent=2)
        encrypted_data = encrypt_data(json_str)
        with open(NOTES_FILE, 'wb') as f:
            f.write(encrypted_data)
    except IOError as e:
        print(f"Error saving notes: {e}")


def save_notes(notes: List[Note]):
    """
    Save notes (encrypted)
    
    Args:
        notes: List of Note objects to save
    """
    _save_notes_encrypted(notes)

