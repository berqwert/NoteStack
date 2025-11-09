import tkinter as tk
from datetime import datetime

from config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT
from models import Note
from storage import load_notes, save_notes
from utils import validate_note
from ui import components
from ui.components import get_tab_label
from ui.handlers import setup_text_handlers, get_text_content, clear_text


class DesktopApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg="#1a1a1a")
        
        self.notes = load_notes()
        self.current_note_id = None
        self.create_widgets()
    
    def create_widgets(self):
        """Create main widgets"""
        self.options_button = components.create_options_button(self.root)
        self.notebook = components.create_note_tabs(
            self.root, 
            self.notes,
            on_tab_select=self.on_tab_select
        )
        components.create_title(self.root)
        self.title_input = components.create_title_input(self.root)
        self.text_input, _, _ = components.create_text_area(self.root)
        setup_text_handlers(self.text_input)
        components.create_buttons(
            self.root,
            save_command=self.save_note,
            clear_command=self.clear_note
        )
        self.notes_label, _ = components.create_labels(self.root, len(self.notes))
    
    def save_note(self):
        """Save note"""
        title = self.title_input.get().strip()
        content = get_text_content(self.text_input)
        is_valid, error_msg = validate_note(content)
        
        if is_valid:
            if self.current_note_id:
                note = next((n for n in self.notes if n.id == self.current_note_id), None)
                if note:
                    note.title = title
                    note.content = content
                    note.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_notes(self.notes)
                    self.notes_label.configure(text=f"Not güncellendi ✓")
                    self.current_note_id = None
                    self.title_input.delete(0, tk.END)
                    clear_text(self.text_input)
                    self.refresh_tabs()
            else:
                new_note = Note(content=content, title=title)
                new_note.id = len(self.notes) + 1
                self.notes.append(new_note)
                save_notes(self.notes)
                self.notes_label.configure(text=f"Toplam {len(self.notes)} not ✓")
                self.title_input.delete(0, tk.END)
                clear_text(self.text_input)
                self.refresh_tabs()
        else:
            self.notes_label.configure(text=f"❌ {error_msg}")
    
    def refresh_tabs(self):
        """Refresh tabs to show all notes"""
        for tab_id in self.notebook.tabs():
            self.notebook.forget(tab_id)
        
        for note in self.notes:
            tab_frame = tk.Frame(self.notebook, bg="#1a1a1a")
            self.notebook.add(tab_frame, text=get_tab_label(note))
            tab_frame.note_id = note.id
    
    def on_tab_select(self, note_id):
        """Handle tab selection"""
        note = next((n for n in self.notes if n.id == note_id), None)
        if note:
            self.current_note_id = note_id
            self.clear_inputs()
            self.title_input.insert(0, note.title)
            self.text_input.insert("1.0", note.content)
            self.text_input.config(fg="black")

    def clear_inputs(self):
        """Clear input fields"""
        self.title_input.delete(0, tk.END)
        self.text_input.delete("1.0", tk.END)
    
    def clear_note(self):
        """Clear note"""
        self.current_note_id = None
        self.title_input.delete(0, tk.END)
        clear_text(self.text_input)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = DesktopApp()
    app.run()
