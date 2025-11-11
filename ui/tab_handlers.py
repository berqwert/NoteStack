import tkinter as tk
from tkinter import Menu


class TabHoverHandler:
    """Handle tab hover events and context menu"""
    
    def __init__(self, root, notebook, delete_callback):
        """
        Initialize tab hover handler
        
        Args:
            root: Root window
            notebook: ttk.Notebook widget
            delete_callback: Callback function for delete action (receives note_id)
        """
        self.root = root
        self.notebook = notebook
        self.delete_callback = delete_callback
        self.hovered_tab_index = None
        self.tab_menu = None
        
        self._setup_menu()
        self._bind_events()
    
    def _setup_menu(self):
        """Setup context menu"""
        self.tab_menu = Menu(self.root, tearoff=0, bg="#2a2a2a", fg="white",
                           activebackground="#007AFF", activeforeground="white")
        self.tab_menu.add_command(label="🗑️ Delete", command=self._delete_hovered_note)
    
    def _bind_events(self):
        """Bind hover events to notebook"""
        self.notebook.bind("<Motion>", self.on_tab_hover)
        self.notebook.bind("<Leave>", lambda e: self._close_menu())
    
    def on_tab_hover(self, event):
        """Handle mouse motion over notebook tabs"""
        elem = str(self.notebook.identify(event.x, event.y))
        if "label" not in elem:
            self._close_menu()
            self.hovered_tab_index = None
            return
        
        try:
            index = self.notebook.index(f"@{event.x},{event.y}")
            if self.hovered_tab_index == index:
                return
            
            self.hovered_tab_index = index
            
            menu_x = event.x_root
            menu_y = event.y_root + 20
            
            self._close_menu()
            self.root.after(400, lambda: self._show_menu(menu_x, menu_y))
        except tk.TclError:
            pass
    
    def _show_menu(self, x, y):
        """Show menu at specific position"""
        self.tab_menu.post(x, y)
    
    def _close_menu(self):
        """Close the tab menu if it exists"""
        if self.tab_menu:
            try:
                self.tab_menu.unpost()
            except:
                pass
    
    def _delete_hovered_note(self):
        """Delete the note that is currently being hovered"""
        if self.hovered_tab_index is None:
            return
        
        try:
            tab_id = self.notebook.tabs()[self.hovered_tab_index]
            tab_frame = self.notebook.nametowidget(tab_id)
            note_id = getattr(tab_frame, 'note_id', None)
            if note_id:
                self.delete_callback(note_id)
                self._close_menu()
                self.hovered_tab_index = None
        except (tk.TclError, IndexError):
            pass
    
    def reset(self):
        """Reset hover state (call after tab refresh)"""
        self.hovered_tab_index = None
        self._close_menu()

