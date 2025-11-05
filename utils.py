"""Utility functions for the desktop app"""

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
        return False, "Not boş olamaz"
    if len(content) > 5000:
        return False, "Not çok uzun (max 5000 karakter)"
    return True, ""

