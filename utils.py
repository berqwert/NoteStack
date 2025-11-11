"""Utility functions for the desktop app"""
from datetime import datetime
from tkinter import messagebox

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
        parent: Parent window (tkinter root)
        note_title: Title of the note to delete (optional)
    
    Returns:
        True if user confirms deletion, False otherwise
    """
    if note_title:
        message = f"'{note_title}' notunu silmek istediğinizden emin misiniz?\n\nBu işlem geri alınamaz."
    else:
        message = "Bu notu silmek istediğinizden emin misiniz?\n\nBu işlem geri alınamaz."
    
    result = messagebox.askyesno(
        title="Not Sil",
        message=message,
        icon="warning"
    )
    return result

