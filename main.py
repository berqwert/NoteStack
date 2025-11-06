import customtkinter as ctk
import json
import os
from datetime import datetime
from config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, DATA_DIR, NOTES_FILE, MAX_NOTE_LENGTH
from utils import format_date, validate_note

class DesktopApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # App ayarları
        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Veri dosyası
        self.data_file = NOTES_FILE
        self.ensure_data_dir()
        self.notes = self.load_notes()
        
        # UI oluştur
        self.create_widgets()
        
    def ensure_data_dir(self):
        """Veri klasörünü oluştur"""
        os.makedirs(DATA_DIR, exist_ok=True)
        
    def load_notes(self):
        """Notları yükle"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_notes(self):
        """Notları kaydet"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=2)
    
    def create_widgets(self):
        """Ana widget'ları oluştur"""
        # Başlık
        title = ctk.CTkLabel(
            self,
            text="📝 Notlarım",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(pady=20)
        
        # Not giriş alanı
        self.text_input = ctk.CTkTextbox(
            self,
            height=200,
            font=ctk.CTkFont(size=14)
        )
        self.text_input.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Butonlar frame
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)
        
        # Kaydet butonu
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Kaydet",
            command=self.save_note,
            width=150,
            height=40
        )
        save_btn.pack(side="left", padx=10)
        
        # Temizle butonu
        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Temizle",
            command=self.clear_note,
            width=150,
            height=40,
            fg_color="transparent",
            border_width=2
        )
        clear_btn.pack(side="left", padx=10)
        
        # Not listesi
        self.notes_label = ctk.CTkLabel(
            self,
            text=f"Toplam {len(self.notes)} not",
            font=ctk.CTkFont(size=14)
        )
        self.notes_label.pack(pady=10)
        
        # Footer
        footer = ctk.CTkLabel(
            self,
            text="💡 İpucu: Notlarınız otomatik olarak kaydedilir",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        footer.pack(pady=5)
    
    def save_note(self):
        """Notu kaydet"""
        content = self.text_input.get("1.0", "end-1c").strip()
        is_valid, error_msg = validate_note(content)
        if is_valid:
            note = {
                "id": len(self.notes) + 1,
                "content": content,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.notes.append(note)
            self.save_notes()
            self.notes_label.configure(text=f"Toplam {len(self.notes)} not ✓")
            self.text_input.delete("1.0", "end")
        else:
            self.notes_label.configure(text=f"❌ {error_msg}")
    
    def clear_note(self):
        """Notu temizle"""
        self.text_input.delete("1.0", "end")

if __name__ == "__main__":
    app = DesktopApp()
    app.mainloop()

