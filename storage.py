"""Note storage operations"""
import json
import os
from pathlib import Path
from typing import List
from models import Note
from config import DATA_DIR, NOTES_FILE, KEY_FILE
from encryption import encrypt_data, decrypt_data, get_or_create_key


def ensure_data_dir():
    """Create data directory"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _migrate_old_data() -> List[Note]:
    """Migrate notes from old project directory to new app data directory"""
    # Check both old project directory and redirected APPDATA location
    old_data_dir = "data"
    old_notes_file = os.path.join(old_data_dir, "notes.json")
    old_key_file = os.path.join(old_data_dir, ".key")
    
    # Also check redirected APPDATA location (Windows Store Python)
    redirected_appdata = os.getenv('APPDATA')
    if redirected_appdata:
        redirected_path = Path(redirected_appdata) / "NoteStack"
        redirected_notes_file = redirected_path / "notes.json"
        redirected_key_file = redirected_path / ".key"
        
        # Try redirected location first (for migration)
        if redirected_notes_file.exists() and redirected_path != DATA_DIR:
            old_notes_file = str(redirected_notes_file)
            old_key_file = str(redirected_key_file)
    
    if not Path(old_notes_file).exists():
        return []
    
    notes = []
    old_notes_path = Path(old_notes_file)
    old_key_path = Path(old_key_file)
    
    # Try to decrypt with old key first
    if old_key_path.exists():
        try:
            old_key = old_key_path.read_bytes()
            from cryptography.fernet import Fernet
            fernet = Fernet(old_key)
            encrypted_data = old_notes_path.read_bytes()
            decrypted_json = fernet.decrypt(encrypted_data).decode('utf-8')
            data = json.loads(decrypted_json)
            notes = [Note.from_dict(note_dict) for note_dict in data]
        except Exception:
            # Fall through to try other methods
            pass
    
    # If decryption with old key failed, try with current key
    if not notes:
        try:
            encrypted_data = old_notes_path.read_bytes()
            decrypted_json = decrypt_data(encrypted_data)
            data = json.loads(decrypted_json)
            notes = [Note.from_dict(note_dict) for note_dict in data]
        except Exception:
            # Try plain text
            try:
                with old_notes_path.open('r', encoding='utf-8') as f:
                    data = json.load(f)
                    notes = [Note.from_dict(note_dict) for note_dict in data]
            except (json.JSONDecodeError, IOError, KeyError):
                pass
    
    # Migrate key file if exists
    old_key_path = Path(old_key_file)
    if notes and old_key_path.exists():
        ensure_data_dir()
        try:
            with old_key_path.open('rb') as f:
                key_data = f.read()
            with KEY_FILE.open('wb') as f:
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
    
    if NOTES_FILE.exists():
        try:
            with NOTES_FILE.open('rb') as f:
                encrypted_data = f.read()
            
            decrypted_json = decrypt_data(encrypted_data)
            data = json.loads(decrypted_json)
            return [Note.from_dict(note_dict) for note_dict in data]
        except Exception:
            try:
                with NOTES_FILE.open('r', encoding='utf-8') as f:
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
        with NOTES_FILE.open('wb') as f:
            f.write(encrypted_data)
    except IOError:
        pass


def save_notes(notes: List[Note]):
    """
    Save notes (encrypted)
    
    Args:
        notes: List of Note objects to save
    """
    _save_notes_encrypted(notes)

