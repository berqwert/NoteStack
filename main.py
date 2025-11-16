import customtkinter as ctk
from datetime import datetime

from config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT
from models import Note
from storage import load_notes, save_notes
from utils import validate_note, confirm_delete, filter_notes_by_query
from ui import components
from ui.components import get_tab_label
from ui.handlers import setup_text_handlers, get_text_content, clear_text, setup_search_handler
from ui.tab_handlers import TabHoverHandler, highlight_matching_tabs

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class DesktopApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(600, 400)  # Minimum window size
        
        self.notes = load_notes()
        self.current_note_id = None
        self.create_widgets()
        self.setup_tab_hover()
        self.setup_keyboard_shortcuts()
    
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
        self.text_input, _ = components.create_text_area(self.root)
        setup_text_handlers(self.text_input)
        _, self.clear_btn = components.create_buttons(
            self.root,
            save_command=self.save_note,
            clear_command=self.clear_note
        )
        self.notes_label, _ = components.create_labels(self.root, len(self.notes))
        self.update_clear_button()
        self.setup_search()
        
        # Automatically select first note on startup if notes exist
        if self.notes:
            first_note = self.notes[0]
            for tab_name, note_id in self.notebook.tab_references.items():
                if note_id == first_note.id:
                    self.notebook.set(tab_name)
                    self.on_tab_select(first_note.id)
                    break
    
    def setup_tab_hover(self):
        """Setup hover events for tab context menu"""
        self.tab_hover_handler = TabHoverHandler(
            self.root,
            self.notebook,
            self.delete_note
        )
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        def save_shortcut(e):
            self.save_note()
            return "break"
        
        def new_shortcut(e):
            self.new_note()
            return "break"
        
        def focus_title(e):
            self.title_input.focus()
            return "break"
        
        def focus_search(e):
            if hasattr(self.notebook, 'search_entry'):
                self.notebook.search_entry.focus()
            return "break"
        
        self.root.bind("<Control-s>", save_shortcut)
        self.root.bind("<Command-s>", save_shortcut)
        self.root.bind("<Control-n>", new_shortcut)
        self.root.bind("<Command-n>", new_shortcut)
        self.root.bind("<Escape>", new_shortcut)
        self.root.bind("<Control-t>", focus_title)
        self.root.bind("<Command-t>", focus_title)
        self.root.bind("<Control-f>", focus_search)
        self.root.bind("<Command-f>", focus_search)
    
    def setup_search(self):
        """Setup search functionality"""
        if hasattr(self.notebook, 'search_entry'):
            def on_search_query(query):
                if query.strip():
                    filtered_notes = filter_notes_by_query(self.notes, query)
                    matched_note_ids = {note.id for note in filtered_notes}
                    self._reorder_tabs_with_matches(matched_note_ids)
                else:
                    self._update_tabs_with_notes(self.notes)
            
            setup_search_handler(self.notebook.search_entry, on_search_query)
    
    def _reorder_tabs_with_matches(self, matched_note_ids):
        """Reorder tabs: matched ones first, then select first matched tab"""
        matched_notes = []
        unmatched_notes = []
        
        for note in self.notes:
            if note.id in matched_note_ids:
                matched_notes.append(note)
            else:
                unmatched_notes.append(note)
        
        reordered_notes = matched_notes + unmatched_notes
        self._update_tabs_with_notes(reordered_notes)
        highlight_matching_tabs(self.notebook, self.notebook.tab_references, matched_note_ids)
        
        if matched_notes:
            first_matched_note = matched_notes[0]
            actual_tab_name = None
            for t_name, note_id in self.notebook.tab_references.items():
                if note_id == first_matched_note.id:
                    actual_tab_name = t_name
                    break
            
            if actual_tab_name:
                self.notebook.set(actual_tab_name)
                self.on_tab_select(first_matched_note.id)
    
    def _update_tabs_with_notes(self, notes):
        """Update tabs with given notes list"""
        for tab_name in list(self.notebook.tab_references.keys()):
            try:
                self.notebook.delete(tab_name)
            except:
                pass
        
        self.notebook.tab_references = {}
        used_tab_names = set()
        
        for note in notes:
            base_tab_name = get_tab_label(note)
            tab_name = base_tab_name
            
            counter = 1
            while tab_name in used_tab_names:
                tab_name = f"{base_tab_name} ({counter})"
                counter += 1
            
            used_tab_names.add(tab_name)
            tab_frame = self.notebook.add(tab_name)
            tab_frame.note_id = note.id
            self.notebook.tab_references[tab_name] = note.id
        
        if hasattr(self.notebook, '_segmented_button'):
            def on_tab_changed(value=None):
                selected_tab = value if value else self.notebook.get()
                if selected_tab and selected_tab in self.notebook.tab_references:
                    note_id = self.notebook.tab_references[selected_tab]
                    self.on_tab_select(note_id)
            
            self.notebook._segmented_button.configure(command=on_tab_changed)
        
        if hasattr(self, 'tab_hover_handler'):
            self.tab_hover_handler.reset()
        
        highlight_matching_tabs(self.notebook, self.notebook.tab_references, set())

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
                    self.title_input.delete(0, "end")
                    clear_text(self.text_input)
                    self.refresh_tabs()
                    self.update_clear_button()
            else:
                new_note = Note(content=content, title=title)
                new_note.id = len(self.notes) + 1
                self.notes.append(new_note)
                save_notes(self.notes)
                self.notes_label.configure(text=f"Toplam {len(self.notes)} not ✓")
                self.title_input.delete(0, "end")
                clear_text(self.text_input)
                self.refresh_tabs()
                self.update_clear_button()
        else:
            self.notes_label.configure(text=f"❌ {error_msg}")
    
    def refresh_tabs(self):
        """Refresh tabs to show all notes"""
        self._update_tabs_with_notes(self.notes)
    
    def on_tab_select(self, note_id):
        """Handle tab selection"""
        note = next((n for n in self.notes if n.id == note_id), None)
        if note:
            self.current_note_id = note_id
            self.clear_inputs()
            self.title_input.insert(0, note.title)
            self.text_input.delete("1.0", "end")
            self.text_input.insert("1.0", note.content)
            self.text_input.configure(text_color=("gray10", "gray90"))
            self.update_clear_button()

    def clear_inputs(self):
        """Clear input fields"""
        self.title_input.delete(0, "end")
        self.text_input.delete("1.0", "end")
    
    def clear_note(self):
        """Clear note or delete if editing existing note"""
        if self.current_note_id:
            # If editing a note, delete it
            self.delete_note(self.current_note_id)
        else:
            # If new note, just clear inputs
            self.current_note_id = None
            self.title_input.delete(0, "end")
            clear_text(self.text_input)
            self.update_clear_button()
    
    def update_clear_button(self):
        """Update clear button text and appearance based on current state"""
        if self.current_note_id:
            self.clear_btn.configure(
                text="🗑️ Kaldır",
                fg_color="#FF3B30",
                hover_color="#CC2E24"
            )
        else:
            self.clear_btn.configure(
                text="🗑️ Temizle",
                fg_color="#FF3B30",
                hover_color="#CC2E24"
            )
    
    def new_note(self):
        """Create new note - clear inputs and reset state"""
        self.current_note_id = None
        self.title_input.delete(0, "end")
        clear_text(self.text_input)
        self.notes_label.configure(text=f"Toplam {len(self.notes)} not")
        self.update_clear_button()
    
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
                self.title_input.delete(0, "end")
                clear_text(self.text_input)
                self.update_clear_button()
            
            self.refresh_tabs()
            self.notes_label.configure(text=f"Toplam {len(self.notes)} not ✓")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = DesktopApp()
    app.run()
