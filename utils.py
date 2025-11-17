"""Utility functions for the desktop app"""
from datetime import datetime
from ui.dialogs import show_confirm

def format_date(date_string):
    """Format date string to readable format"""
    try:
        dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d %b %Y, %H:%M")
    except:
        return date_string

def validate_note(content):
    """Validate note content"""
    if not content or not content.strip():
        return False, "Note cannot be empty"
    if len(content) > 5000:
        return False, "Note is too long (max 5000 characters)"
    return True, ""

def confirm_delete(parent, note_title: str = None) -> bool:
    """
    Show confirmation dialog for deleting a note
    
    Args:
        parent: Parent window (CTk root)
        note_title: Title of the note to delete (optional)
    
    Returns:
        True if user confirms deletion, False otherwise
    """
    if note_title:
        message = f"'{note_title}' notunu silmek istediğinizden emin misiniz?\n\nBu işlem geri alınamaz."
    else:
        message = "Bu notu silmek istediğinizden emin misiniz?\n\nBu işlem geri alınamaz."
    
    return show_confirm(parent, "Not Sil", message)


def filter_notes_by_query(notes, query: str):
    """
    Filter notes by search query
    
    Args:
        notes: List of Note objects
        query: Search query string
    
    Returns:
        List of filtered Note objects
    """
    if not query or not query.strip():
        return notes
    
    query_lower = query.strip().lower()
    filtered = []
    
    for note in notes:
        title_match = note.title.lower() if note.title else ""
        content_match = note.content.lower() if note.content else ""
        if query_lower in title_match or query_lower in content_match:
            filtered.append(note)
    
    return filtered

