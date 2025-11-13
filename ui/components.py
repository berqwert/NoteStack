import customtkinter as ctk
from tkinter import ttk


def create_options_button(parent) -> ctk.CTkButton:
    """
    Create options button in top right
    
    Returns:
        options_button
    """
    top_frame = ctk.CTkFrame(parent, fg_color="transparent")
    top_frame.pack(fill="x", pady=10, padx=10)
    
    options_button = ctk.CTkButton(
        top_frame,
        text="⚙️",
        font=("Arial", 16),
        width=40,
        height=40,
        fg_color="#2a2a2a",
        hover_color="#3a3a3a",
        corner_radius=5
    )
    options_button.pack(side="right")
    
    return options_button


def create_title(parent) -> ctk.CTkLabel:
    """Create title widget"""
    title = ctk.CTkLabel(
        parent,
        text="📝 NoteStack",
        font=("Arial", 32, "bold")
    )
    title.pack(pady=20)
    return title


def create_title_input(parent) -> ctk.CTkEntry:
    """
    Create Entry widget for note title
    
    Returns:
        title_input Entry widget
    """
    title_label = ctk.CTkLabel(
        parent,
        text="Başlık:",
        font=("Arial", 12)
    )
    title_label.pack(pady=(10, 5), padx=20, anchor="w")
    
    title_input = ctk.CTkEntry(
        parent,
        font=("Arial", 14),
        height=40,
        corner_radius=5,
        border_width=2,
        border_color="#007AFF"
    )
    title_input.pack(pady=(0, 10), padx=20, fill="x")
    
    return title_input


def create_text_area(parent) -> tuple[ctk.CTkTextbox, ctk.CTkFrame]:
    """
    Create text area
    
    Returns:
        (text_input, text_frame) tuple
    """
    text_frame = ctk.CTkFrame(parent, fg_color="transparent")
    text_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    text_input = ctk.CTkTextbox(
        text_frame,
        font=("Arial", 14),
        wrap="word",
        corner_radius=5,
        border_width=3,
        border_color="#007AFF"
    )
    
    text_input.insert("1.0", "Notunuzu buraya yazın...")
    text_input.configure(text_color="#999999")
    
    text_input.pack(fill="both", expand=True)
    
    return text_input, text_frame


def create_buttons(parent, save_command, clear_command) -> tuple[ctk.CTkFrame, ctk.CTkButton]:
    """
    Create buttons frame
    
    Args:
        parent: Parent widget
        save_command: Save button command
        clear_command: Clear button command
    
    Returns:
        (button_frame, clear_btn) tuple - clear_btn reference for dynamic updates
    """
    button_frame = ctk.CTkFrame(parent, fg_color="transparent")
    button_frame.pack(pady=10)
    
    save_btn = ctk.CTkButton(
        button_frame,
        text="💾 Kaydet",
        command=save_command,
        width=150,
        height=40,
        fg_color="#007AFF",
        hover_color="#0056CC",
        font=("Arial", 12),
        corner_radius=5
    )
    save_btn.pack(side="left", padx=10)
    
    clear_btn = ctk.CTkButton(
        button_frame,
        text="🗑️ Temizle",
        command=clear_command,
        width=150,
        height=40,
        fg_color="#FF3B30",
        hover_color="#CC2E24",
        font=("Arial", 12),
        corner_radius=5
    )
    clear_btn.pack(side="left", padx=10)
    
    return button_frame, clear_btn


def create_labels(parent, notes_count: int) -> tuple[ctk.CTkLabel, ctk.CTkLabel]:
    """
    Create labels (note list and footer)
    
    Args:
        parent: Parent widget
        notes_count: Number of notes
    
    Returns:
        (notes_label, footer) tuple
    """
    notes_label = ctk.CTkLabel(
        parent,
        text=f"Toplam {notes_count} not",
        font=("Arial", 14)
    )
    notes_label.pack(pady=10)
    
    footer = ctk.CTkLabel(
        parent,
        text="💡 İpucu: Notlarınız otomatik olarak kaydedilir",
        font=("Arial", 11),
        text_color="gray"
    )
    footer.pack(pady=5)
    
    return notes_label, footer


def create_note_tabs(parent, notes, on_tab_select=None, new_note_command=None) -> ctk.CTkTabview:
    """
    Create tabs section to display notes
    
    Args:
        parent: Parent widget
        notes: List of Note objects
        on_tab_select: Callback function when tab is selected (receives note_id)
        new_note_command: New note button command (optional)
    
    Returns:
        tabview widget
    """
    notebook_frame = ctk.CTkFrame(parent, fg_color="transparent")
    notebook_frame.pack(fill="x", padx=20, pady=10)
    
    tabs_label = ctk.CTkLabel(
        notebook_frame,
        text="📑 Saved Notes",
        font=("Arial", 14, "bold")
    )
    tabs_label.pack(anchor="w", pady=(0, 10))
    
    tabs_container = ctk.CTkFrame(notebook_frame, fg_color="transparent")
    tabs_container.pack(fill="x", pady=(0, 10))
    
    tabview = ctk.CTkTabview(tabs_container, height=50)
    tabview.pack(side="left", fill="x", expand=True)
    
    if new_note_command:
        new_btn = ctk.CTkButton(
            tabs_container,
            text="➕ New Note",
            command=new_note_command,
            width=120,
            height=35,
            fg_color="#34C759",
            hover_color="#28A745",
            font=("Arial", 10),
            corner_radius=5
        )
        new_btn.pack(side="right", padx=(10, 0))
    
    # Store tab references with note_id
    tabview.tab_references = {}
    
    for note in notes:
        tab_name = get_tab_label(note)
        tab_frame = tabview.add(tab_name)
        tab_frame.note_id = note.id
        tabview.tab_references[tab_name] = note.id
    
    if on_tab_select:
        def on_tab_changed(value=None):
            # CustomTkinter passes the selected value as argument
            # But we can also get it from tabview.get()
            selected_tab = value if value else tabview.get()
            if selected_tab and selected_tab in tabview.tab_references:
                note_id = tabview.tab_references[selected_tab]
                on_tab_select(note_id)
        
        tabview._on_tab_select_callback = on_tab_select
        
        if hasattr(tabview, '_segmented_button'):
            tabview._segmented_button.configure(command=on_tab_changed)
    
    return tabview


def get_tab_label(note) -> str:
    """Generate label for tab from note"""
    if note.title:
        title = note.title[:20] + "..." if len(note.title) > 20 else note.title
        return f"📄 {title}"
    else:
        content_preview = note.content[:15].strip() if note.content else "Untitled"
        return f"📄 {content_preview}..."


def on_tab_changed(tabview, callback):
    """Handle tab change event"""
    selected_tab = tabview.get()
    if selected_tab in tabview.tab_references:
        note_id = tabview.tab_references[selected_tab]
        callback(note_id)
