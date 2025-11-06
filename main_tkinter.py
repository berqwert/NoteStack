import tkinter as tk
from tkinter import scrolledtext
import json
import os
from datetime import datetime
from config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, DATA_DIR, NOTES_FILE, MAX_NOTE_LENGTH
from utils import validate_note

class DesktopApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg="#1a1a1a")
        
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
        title = tk.Label(
            self.root,
            text="📝 Notlarım",
            font=("Arial", 32, "bold"),
            bg="#1a1a1a",
            fg="white"
        )
        title.pack(pady=20)
        
        # Text area container
        text_frame = tk.Frame(self.root, bg="#1a1a1a")
        text_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Text widget ve scrollbar'ı manuel oluştur (macOS uyumluluğu için)
        self.text_input = tk.Text(
            text_frame,
            height=15,
            width=70,
            font=("Arial", 14),
            bg="#2b2b2b",
            fg="white",
            insertbackground="white",
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=2,
            highlightthickness=3,
            highlightbackground="#4A90E2",
            highlightcolor="#4A90E2",
            selectbackground="#4A90E2"
        )
        
        # Scrollbar ekle
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=self.text_input.yview)
        self.text_input.configure(yscrollcommand=scrollbar.set)
        
        # Placeholder text ekle
        self.text_input.insert("1.0", "Notunuzu buraya yazın...")
        self.text_input.config(fg="gray")
        
        # Layout
        self.text_input.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Placeholder davranışı için event binding
        self.text_input.bind("<FocusIn>", self.on_text_focus_in)
        self.text_input.bind("<FocusOut>", self.on_text_focus_out)
        
        # Butonlar frame
        button_frame = tk.Frame(self.root, bg="#1a1a1a")
        button_frame.pack(pady=10, fill="x")
        
        # Kaydet butonu
        save_btn = tk.Button(
            button_frame,
            text="💾 Kaydet",
            command=self.save_note,
            width=15,
            height=2,
            bg="#007AFF",
            fg="white",
            font=("Arial", 12),
            cursor="hand2"
        )
        save_btn.pack(side="left", padx=10)
        
        # Temizle butonu
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Temizle",
            command=self.clear_note,
            width=15,
            height=2,
            bg="#FF3B30",
            fg="white",
            font=("Arial", 12),
            cursor="hand2"
        )
        clear_btn.pack(side="left", padx=10)
        
        # Not listesi
        self.notes_label = tk.Label(
            self.root,
            text=f"Toplam {len(self.notes)} not",
            font=("Arial", 14),
            bg="#1a1a1a",
            fg="white"
        )
        self.notes_label.pack(pady=10)
        
        # Footer
        footer = tk.Label(
            self.root,
            text="💡 İpucu: Notlarınız otomatik olarak kaydedilir",
            font=("Arial", 11),
            bg="#1a1a1a",
            fg="gray"
        )
        footer.pack(pady=5)
    
    def save_note(self):
        """Notu kaydet"""
        content = self.text_input.get("1.0", "end-1c").strip()
        # Placeholder text'i kontrol et
        if content == "Notunuzu buraya yazın...":
            content = ""
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
            self.text_input.insert("1.0", "Notunuzu buraya yazın...")
            self.text_input.config(fg="gray")
        else:
            self.notes_label.configure(text=f"❌ {error_msg}")
    
    def clear_note(self):
        """Notu temizle"""
        self.text_input.delete("1.0", "end")
        self.text_input.insert("1.0", "Notunuzu buraya yazın...")
        self.text_input.config(fg="gray")
    
    def on_text_focus_in(self, event):
        """Text area'ya odaklanıldığında placeholder'ı temizle"""
        current_text = self.text_input.get("1.0", "end-1c")
        if current_text.strip() == "Notunuzu buraya yazın...":
            self.text_input.delete("1.0", "end")
            self.text_input.config(fg="white")
    
    def on_text_focus_out(self, event):
        """Text area'dan çıkıldığında boşsa placeholder ekle"""
        current_text = self.text_input.get("1.0", "end-1c")
        if not current_text.strip():
            self.text_input.insert("1.0", "Notunuzu buraya yazın...")
            self.text_input.config(fg="gray")
    
    def run(self):
        """Uygulamayı çalıştır"""
        self.root.mainloop()

if __name__ == "__main__":
    app = DesktopApp()
    app.run()

