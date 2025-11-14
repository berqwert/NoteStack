"""Event handlers"""


def setup_text_handlers(text_input, placeholder_text: str = "Notunuzu buraya yazın..."):
    """
    Setup event handlers for text area
    
    Args:
        text_input: Text widget (CTkTextbox)
        placeholder_text: Placeholder text
    """
    def on_focus_in(event):
        """Clear placeholder when text area is focused"""
        current_text = text_input.get("1.0", "end-1c")
        if current_text.strip() == placeholder_text:
            text_input.delete("1.0", "end")
            text_input.configure(text_color=("gray10", "gray90"))
    
    def on_focus_out(event):
        """Add placeholder if text area is empty when focus is lost"""
        current_text = text_input.get("1.0", "end-1c")
        if not current_text.strip():
            text_input.insert("1.0", placeholder_text)
            text_input.configure(text_color="gray")
    
    text_input.bind("<FocusIn>", on_focus_in)
    text_input.bind("<FocusOut>", on_focus_out)


def get_text_content(text_input, placeholder_text: str = "Notunuzu buraya yazın...") -> str:
    """
    Get content from text area (filter placeholder)
    
    Args:
        text_input: Text widget (CTkTextbox)
        placeholder_text: Placeholder text
    
    Returns:
        Cleaned content
    """
    content = text_input.get("1.0", "end-1c").strip()
    if content == placeholder_text:
        return ""
    return content


def clear_text(text_input, placeholder_text: str = "Notunuzu buraya yazın..."):
    """
    Clear text area and add placeholder
    
    Args:
        text_input: Text widget (CTkTextbox)
        placeholder_text: Placeholder text
    """
    text_input.delete("1.0", "end")
    text_input.insert("1.0", placeholder_text)
    text_input.configure(text_color="gray")


def setup_search_handler(search_entry, search_callback):
    """
    Setup search functionality for notes
    
    Args:
        search_entry: Search entry widget
        search_callback: Callback function that receives search query and updates tabs
    """
    def on_search(event=None):
        search_query = search_entry.get()
        search_callback(search_query)
    
    search_entry.bind("<KeyRelease>", on_search)
    return on_search


