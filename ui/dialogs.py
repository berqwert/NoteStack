"""Modern dialog system for warnings, confirmations, and info messages"""
import customtkinter as ctk


class DialogWindow(ctk.CTkToplevel):
    """Base class for custom dialogs"""
    
    def __init__(self, parent, title: str, message: str, dialog_type: str = "info"):
        super().__init__(parent)
        self.title(title)
        self.geometry("480x280")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.result = None
        
        self._configure_colors(dialog_type)
        self._create_ui(title, message, dialog_type)
        self._center_window()
        self.focus()
    
    def _configure_colors(self, dialog_type: str):
        """Configure colors based on dialog type"""
        color_schemes = {
            "info": {"bg": "#1a1a1a", "icon_color": "#007AFF", "button_color": "#007AFF", "button_hover": "#0056CC"},
            "warning": {"bg": "#1a1a1a", "icon_color": "#FF9500", "button_color": "#FF9500", "button_hover": "#CC7700"},
            "error": {"bg": "#1a1a1a", "icon_color": "#FF3B30", "button_color": "#FF3B30", "button_hover": "#CC2E24"},
            "confirm": {"bg": "#1a1a1a", "icon_color": "#FF9500", "button_color": "#007AFF", "button_hover": "#0056CC"}
        }
        self.colors = color_schemes.get(dialog_type, color_schemes["info"])
        self.configure(fg_color=self.colors["bg"])
    
    def _create_ui(self, title: str, message: str, dialog_type: str):
        """Create dialog UI"""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=35, pady=35)
        
        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 25))
        
        icon_label = ctk.CTkLabel(
            header_frame,
            text=self._get_icon(dialog_type),
            font=("Arial", 52),
            text_color=self.colors["icon_color"]
        )
        icon_label.pack(side="left", padx=(0, 18))
        
        title_label = ctk.CTkLabel(header_frame, text=title, font=("Arial", 22, "bold"), anchor="w")
        title_label.pack(side="left", fill="x", expand=True)
        
        message_label = ctk.CTkLabel(
            container,
            text=message,
            font=("Arial", 15),
            wraplength=400,
            justify="left",
            anchor="w"
        )
        message_label.pack(fill="x", pady=(0, 30))
        
        self.buttons_frame = ctk.CTkFrame(container, fg_color="transparent")
        self.buttons_frame.pack(fill="x")
    
    def _get_icon(self, dialog_type: str) -> str:
        """Get icon emoji based on dialog type"""
        icons = {"info": "ℹ️", "warning": "⚠️", "error": "❌", "confirm": "❓"}
        return icons.get(dialog_type, "ℹ️")
    
    def _center_window(self):
        """Center dialog on parent window"""
        self.update_idletasks()
        parent_x = self.master.winfo_x()
        parent_y = self.master.winfo_y()
        parent_width = self.master.winfo_width()
        parent_height = self.master.winfo_height()
        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)
        self.geometry(f"+{x}+{y}")
    
    def _on_close(self):
        """Handle window close"""
        self.result = False
        self.destroy()
    
    def _create_button(self, text: str, command, width=130, height=42, fg_color=None, hover_color=None):
        """Helper method to create buttons"""
        if fg_color is None:
            fg_color = self.colors["button_color"]
        if hover_color is None:
            hover_color = self.colors["button_hover"]
        
        btn = ctk.CTkButton(
            self.buttons_frame,
            text=text,
            command=command,
            width=width,
            height=height,
            fg_color=fg_color,
            hover_color=hover_color,
            font=("Arial", 14, "bold"),
            corner_radius=10
        )
        return btn


class ConfirmDialog(DialogWindow):
    """Confirmation dialog with Yes/No buttons"""
    
    def __init__(self, parent, title: str, message: str):
        super().__init__(parent, title, message, "confirm")
        self._add_confirm_buttons()
    
    def _add_confirm_buttons(self):
        """Add Yes and No buttons"""
        no_btn = self._create_button("İptal", self._on_no, fg_color="#6c6c6c", hover_color="#555555")
        no_btn.pack(side="right", padx=(12, 0))
        
        yes_btn = self._create_button("Onayla", self._on_yes)
        yes_btn.pack(side="right")
        
        self.after(100, lambda: no_btn.focus())
    
    def _on_yes(self):
        """Handle Yes button click"""
        self.result = True
        self.destroy()
    
    def _on_no(self):
        """Handle No button click"""
        self.result = False
        self.destroy()


class InfoDialog(DialogWindow):
    """Information dialog with OK button"""
    
    def __init__(self, parent, title: str, message: str):
        super().__init__(parent, title, message, "info")
        self._add_ok_button()
    
    def _add_ok_button(self):
        """Add OK button"""
        ok_btn = self._create_button("Tamam", self._on_ok)
        ok_btn.pack(side="right")
        self.after(100, lambda: ok_btn.focus())
    
    def _on_ok(self):
        """Handle OK button click"""
        self.result = True
        self.destroy()


class WarningDialog(DialogWindow):
    """Warning dialog with OK button"""
    
    def __init__(self, parent, title: str, message: str):
        super().__init__(parent, title, message, "warning")
        self._add_ok_button()
    
    def _add_ok_button(self):
        """Add OK button"""
        ok_btn = self._create_button("Tamam", self._on_ok)
        ok_btn.pack(side="right")
        self.after(100, lambda: ok_btn.focus())
    
    def _on_ok(self):
        """Handle OK button click"""
        self.result = True
        self.destroy()


class ErrorDialog(DialogWindow):
    """Error dialog with OK button"""
    
    def __init__(self, parent, title: str, message: str):
        super().__init__(parent, title, message, "error")
        self._add_ok_button()
    
    def _add_ok_button(self):
        """Add OK button"""
        ok_btn = self._create_button("Tamam", self._on_ok)
        ok_btn.pack(side="right")
        self.after(100, lambda: ok_btn.focus())
    
    def _on_ok(self):
        """Handle OK button click"""
        self.result = True
        self.destroy()


def show_confirm(parent, title: str, message: str) -> bool:
    """Show confirmation dialog"""
    dialog = ConfirmDialog(parent, title, message)
    dialog.wait_window()
    return dialog.result if dialog.result is not None else False


def show_info(parent, title: str, message: str):
    """Show information dialog"""
    dialog = InfoDialog(parent, title, message)
    dialog.wait_window()


def show_warning(parent, title: str, message: str):
    """Show warning dialog"""
    dialog = WarningDialog(parent, title, message)
    dialog.wait_window()


def show_error(parent, title: str, message: str):
    """Show error dialog"""
    dialog = ErrorDialog(parent, title, message)
    dialog.wait_window()
