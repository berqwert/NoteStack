import tkinter as tk
from datetime import datetime

from config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT
from models import Note
from storage import load_notes, save_notes
from utils import validate_note, confirm_delete
from ui import components
from ui.components import get_tab_label
from ui.handlers import setup_text_handlers, get_text_content, clear_text
from ui.tab_handlers import TabHoverHandler


class DesktopApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg="#1a1a1a")
        
        self.notes = load_notes()
        self.current_note_id = None
        self.create_widgets()
        self.setup_tab_hover()
    
    def create_widgets(self):
        """Create main widgets"""
        self.options_button = components.create_options_button(self.root)
        self.notebook = components.create_note_tabs(
            self.root, 
            self.notes,
            on_tab_select=self.on_tab_select,
            new_note_command=self.new_note
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
    
    def setup_tab_hover(self):
        """Setup hover events for tab context menu"""
        self.tab_hover_handler = TabHoverHandler(
            self.root,
            self.notebook,
            self.delete_note
        )

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
        
        # Reset hover handler after refresh
        if hasattr(self, 'tab_hover_handler'):
            self.tab_hover_handler.reset()
    
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
    
    def new_note(self):
        """Create new note - clear inputs and reset state"""
        self.current_note_id = None
        self.title_input.delete(0, tk.END)
        clear_text(self.text_input)
        self.notes_label.configure(text=f"Toplam {len(self.notes)} not")
    
    def delete_note(self, note_id):
        """Delete note after confirmation"""
        note = next((n for n in self.notes if n.id == note_id), None)
        if not note:
            return
        
        note_title = note.title if note.title else None
        if confirm_delete(self.root, note_title):
            self.notes = [n for n in self.notes if n.id != note_id]
            save_notes(self.notes)
            
            if self.current_note_id == note_id:
                self.current_note_id = None
                self.title_input.delete(0, tk.END)
                clear_text(self.text_input)
            
            self.refresh_tabs()
            self.notes_label.configure(text=f"Toplam {len(self.notes)} not ✓")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = DesktopApp()
    app.run()
