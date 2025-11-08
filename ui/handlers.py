"""Event handler'lar"""


def setup_text_handlers(text_input, placeholder_text: str = "Notunuzu buraya yazın..."):
    """
    Text area için event handler'ları ayarla
    
    Args:
        text_input: Text widget
        placeholder_text: Placeholder metni
    """
    def on_focus_in(event):
        """Text area'ya odaklanıldığında placeholder'ı temizle"""
        current_text = text_input.get("1.0", "end-1c")
        if current_text.strip() == placeholder_text:
            text_input.delete("1.0", "end")
            text_input.config(fg="black")
    
    def on_focus_out(event):
        """Text area'dan çıkıldığında boşsa placeholder ekle"""
        current_text = text_input.get("1.0", "end-1c")
        if not current_text.strip():
            text_input.insert("1.0", placeholder_text)
            text_input.config(fg="#999999")
    
    text_input.bind("<FocusIn>", on_focus_in)
    text_input.bind("<FocusOut>", on_focus_out)


def get_text_content(text_input, placeholder_text: str = "Notunuzu buraya yazın...") -> str:
    """
    Text area'dan içeriği al (placeholder'ı filtrele)
    
    Args:
        text_input: Text widget
        placeholder_text: Placeholder metni
    
    Returns:
        Temizlenmiş içerik
    """
    content = text_input.get("1.0", "end-1c").strip()
    if content == placeholder_text:
        return ""
    return content


def clear_text(text_input, placeholder_text: str = "Notunuzu buraya yazın..."):
    """
    Text area'yı temizle ve placeholder ekle
    
    Args:
        text_input: Text widget
        placeholder_text: Placeholder metni
    """
    text_input.delete("1.0", "end")
    text_input.insert("1.0", placeholder_text)
    text_input.config(fg="#999999")

