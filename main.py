import tkinter as tk
from datetime import datetime

from config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT
from models import Note
from storage import load_notes, save_notes
from utils import validate_note
from ui import components
from ui.handlers import setup_text_handlers, get_text_content, clear_text


class DesktopApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg="#1a1a1a")
        
        # Notları yükle
        self.notes = load_notes()
        
        # UI oluştur
        self.create_widgets()
    
    def create_widgets(self):
        """Ana widget'ları oluştur"""
        # Başlık
        components.create_title(self.root)
        
        # Not başlığı input
        self.title_input = components.create_title_input(self.root)
        
        # Text area
        self.text_input, _, _ = components.create_text_area(self.root)
        setup_text_handlers(self.text_input)
        
        # Butonlar
        components.create_buttons(
            self.root,
            save_command=self.save_note,
            clear_command=self.clear_note
        )
        
        # Label'lar
        self.notes_label, _ = components.create_labels(self.root, len(self.notes))
    
    def save_note(self):
        """Notu kaydet"""
        title = self.title_input.get().strip()
        content = get_text_content(self.text_input)
        is_valid, error_msg = validate_note(content)
        
        if is_valid:
            # Yeni not oluştur
            new_note = Note(content=content, title=title)
            new_note.id = len(self.notes) + 1
            self.notes.append(new_note)
            
            # Kaydet
            save_notes(self.notes)
            
            # UI güncelle
            self.notes_label.configure(text=f"Toplam {len(self.notes)} not ✓")
            self.title_input.delete(0, tk.END)
            clear_text(self.text_input)
        else:
            self.notes_label.configure(text=f"❌ {error_msg}")
    
    def clear_note(self):
        """Notu temizle"""
        self.title_input.delete(0, tk.END)
        clear_text(self.text_input)
    
    def run(self):
        """Uygulamayı çalıştır"""
        self.root.mainloop()


if __name__ == "__main__":
    app = DesktopApp()
    app.run()
