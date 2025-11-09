"""Utility functions for the desktop app"""
from datetime import datetime

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

