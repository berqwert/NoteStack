import customtkinter as ctk
from tkinter import Menu
import tkinter as tk


class TabHoverHandler:
    """Handle tab hover events and context menu"""
    
    def __init__(self, root, tabview, delete_callback):
        """
        Initialize tab hover handler
        
        Args:
            root: Root window
            tabview: ctk.CTkTabview widget
            delete_callback: Callback function for delete action (receives note_id)
        """
        self.root = root
        self.tabview = tabview
        self.delete_callback = delete_callback
        self.hovered_tab_name = None
        self.tab_menu = None
        self.hover_timer = None
        self.overlay_widgets = {}  # Store overlay widgets for each tab
        
        self._setup_menu()
        self._create_overlays()
        self._bind_events()
    
    def _setup_menu(self):
        """Setup context menu"""
        self.tab_menu = Menu(self.root, tearoff=0, bg="#2a2a2a", fg="white",
                           activebackground="#007AFF", activeforeground="white")
        self.tab_menu.add_command(label="🗑️ Delete", command=self._delete_hovered_note)
    
    def _create_overlays(self):
        """Create invisible overlay widgets on top of tab headers for hover detection"""
        try:
            if hasattr(self.tabview, '_segmented_button'):
                seg_button = self.tabview._segmented_button
                
                # Get tab values from tab_references instead
                if hasattr(self.tabview, 'tab_references') and self.tabview.tab_references:
                    values = list(self.tabview.tab_references.keys())
                    
                    # Get the canvas or frame that contains the buttons
                    parent_widget = None
                    if hasattr(seg_button, '_canvas'):
                        parent_widget = seg_button._canvas
                    elif hasattr(seg_button, '_frame'):
                        parent_widget = seg_button._frame
                    elif hasattr(seg_button, '_parent_canvas'):
                        parent_widget = seg_button._parent_canvas
                    
                    if parent_widget and values:
                        # Calculate button positions
                        try:
                            total_width = seg_button.winfo_width()
                            total_height = seg_button.winfo_height()
                            
                            if total_width > 0 and len(values) > 0:
                                button_width = total_width / len(values)
                                
                                # Create invisible labels for each tab
                                for i, tab_name in enumerate(values):
                                    if tab_name in self.tabview.tab_references:
                                        # Create invisible label overlay
                                        overlay = tk.Label(
                                            parent_widget,
                                            bg='',
                                            width=int(button_width),
                                            height=1,
                                            cursor='arrow'
                                        )
                                        
                                        # Place overlay at button position
                                        overlay.place(x=i * button_width, y=0, width=button_width, height=total_height)
                                        
                                        # Bind hover events
                                        overlay.bind('<Enter>', lambda e, name=tab_name: self.on_tab_enter(name, e))
                                        overlay.bind('<Leave>', lambda e: self.on_tab_leave())
                                        
                                        self.overlay_widgets[tab_name] = overlay
                        except Exception:
                            pass
        except Exception:
            pass
    
    def _bind_events(self):
        """Bind hover events - alternative approach using periodic checking"""
        # Also bind to root window as fallback
        self.root.bind("<Motion>", self.on_mouse_motion)
    
    def on_tab_enter(self, tab_name, event):
        """Handle mouse entering a tab button"""
        try:
            if tab_name and tab_name in self.tabview.tab_references:
                if self.hovered_tab_name == tab_name:
                    return
                
                self.hovered_tab_name = tab_name
                
                if self.hover_timer:
                    self.root.after_cancel(self.hover_timer)
                
                menu_x = event.x_root
                menu_y = event.y_root + 20
                
                self._close_menu()
                self.hover_timer = self.root.after(400, lambda: self._show_menu(menu_x, menu_y))
        except Exception:
            pass
    
    def on_tab_leave(self):
        """Handle mouse leaving a tab button"""
        if self.hover_timer:
            self.root.after_cancel(self.hover_timer)
            self.hover_timer = None
    
    def on_mouse_motion(self, event):
        """Handle mouse motion - fallback method"""
        try:
            if not hasattr(self.tabview, '_segmented_button'):
                return
            
            seg_button = self.tabview._segmented_button
            
            try:
                seg_x = seg_button.winfo_rootx()
                seg_y = seg_button.winfo_rooty()
                seg_width = seg_button.winfo_width()
                seg_height = seg_button.winfo_height()
            except:
                seg_x = self.tabview.winfo_rootx()
                seg_y = self.tabview.winfo_rooty()
                seg_width = self.tabview.winfo_width()
                seg_height = 50
            
            root_x = event.x_root
            root_y = event.y_root
            
            if (seg_x <= root_x <= seg_x + seg_width and 
                seg_y <= root_y <= seg_y + seg_height):
                rel_x = root_x - seg_x
                tab_name = self._get_tab_at_position(rel_x, seg_button)
                
                if tab_name and tab_name in self.tabview.tab_references:
                    if self.hovered_tab_name != tab_name:
                        self.hovered_tab_name = tab_name
                        if self.hover_timer:
                            self.root.after_cancel(self.hover_timer)
                        menu_x = root_x
                        menu_y = root_y + 20
                        self._close_menu()
                        self.hover_timer = self.root.after(400, lambda: self._show_menu(menu_x, menu_y))
                else:
                    self._close_menu()
                    self.hovered_tab_name = None
            else:
                if self.hover_timer:
                    self.root.after_cancel(self.hover_timer)
                    self.hover_timer = None
                self._close_menu()
                self.hovered_tab_name = None
        except Exception:
            pass
    
    def _get_tab_at_position(self, x, seg_button):
        """Determine which tab is at the given x position"""
        try:
            # Get tab names from tabview.tab_references instead of segmented_button.values
            if not hasattr(self.tabview, 'tab_references') or not self.tabview.tab_references:
                return None
            
            # Get tab names from tab_references keys
            values = list(self.tabview.tab_references.keys())
            if not values:
                return None
            
            try:
                total_width = seg_button.winfo_width()
            except:
                return None
            
            if total_width <= 0:
                return None
            
            button_width = total_width / len(values) if len(values) > 0 else 0
            
            if button_width <= 0:
                return None
            
            button_index = int(x / button_width)
            button_index = max(0, min(button_index, len(values) - 1))
            
            result = values[button_index]
            return result
        except Exception:
            return None
    
    def _show_menu(self, x, y):
        """Show menu at specific position"""
        try:
            if self.hovered_tab_name and self.hovered_tab_name in self.tabview.tab_references:
                self.tab_menu.post(x, y)
        except Exception:
            pass
    
    def _close_menu(self):
        """Close the tab menu if it exists"""
        if self.tab_menu:
            try:
                self.tab_menu.unpost()
            except:
                pass
    
    def _delete_hovered_note(self):
        """Delete the note that is currently being hovered"""
        if self.hovered_tab_name is None:
            return
        
        try:
            note_id = self.tabview.tab_references.get(self.hovered_tab_name)
            if note_id:
                self.delete_callback(note_id)
                self._close_menu()
                self.hovered_tab_name = None
                if self.hover_timer:
                    self.root.after_cancel(self.hover_timer)
                    self.hover_timer = None
        except Exception:
            pass
    
    def reset(self):
        """Reset hover state (call after tab refresh)"""
        # Destroy old overlays
        for overlay in self.overlay_widgets.values():
            try:
                overlay.destroy()
            except:
                pass
        self.overlay_widgets.clear()
        
        self.hovered_tab_name = None
        self._close_menu()
        if self.hover_timer:
            self.root.after_cancel(self.hover_timer)
            self.hover_timer = None
        
        # Recreate overlays after refresh
        self._create_overlays()


def highlight_matching_tabs(tabview, tab_references, matched_note_ids):
    """
    Highlight matching tabs in red, keep others normal
    
    Args:
        tabview: CTkTabview widget
        tab_references: Dictionary mapping tab names to note IDs
        matched_note_ids: Set of note IDs that match the search query
    """
    if not hasattr(tabview, '_segmented_button'):
        return
    
    seg_button = tabview._segmented_button
    if not hasattr(seg_button, '_buttons_dict'):
        return
    
    for tab_name, note_id in tab_references.items():
        if tab_name in seg_button._buttons_dict:
            button = seg_button._buttons_dict[tab_name]
            if note_id in matched_note_ids:
                button.configure(fg_color="#FF3B30", hover_color="#CC2E24")
            else:
                button.configure(fg_color=["#3B3B3B", "#2B2B2B"], hover_color=["#4A4A4A", "#3A3A3A"])
