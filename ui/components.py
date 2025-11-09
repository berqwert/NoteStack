import tkinter as tk
from tkinter import ttk


def create_options_button(parent) -> tk.Button:
    """
    Create options button in top right
    
    Returns:
        options_button
    """
    top_frame = tk.Frame(parent, bg="#1a1a1a")
    top_frame.pack(fill="x", pady=10, padx=10)
    
    options_button = tk.Button(
        top_frame,
        text="⚙️",
        font=("Arial", 16),
        bg="#2a2a2a",
        fg="white",
        relief=tk.FLAT,
        cursor="hand2",
        width=3,
        height=1
    )
    options_button.pack(side="right")
    
    return options_button


def create_title(parent) -> tk.Label:
    """Create title widget"""
    title = tk.Label(
        parent,
        text="📝 Notlarım",
        font=("Arial", 32, "bold"),
        bg="#1a1a1a",
        fg="white"
    )
    title.pack(pady=20)
    return title


def create_title_input(parent) -> tk.Entry:
    """
    Create Entry widget for note title
    
    Returns:
        title_input Entry widget
    """
    title_label = tk.Label(
        parent,
        text="Başlık:",
        font=("Arial", 12),
        bg="#1a1a1a",
        fg="white"
    )
    title_label.pack(pady=(10, 5), padx=20, anchor="w")
    
    title_frame = tk.Frame(parent, bg="#1a1a1a")
    title_frame.pack(pady=(0, 10), padx=20, fill="x")
    
    title_input = tk.Entry(
        title_frame,
        font=("Arial", 14),
        bg="white",
        fg="black",
        insertbackground="black",
        relief=tk.SOLID,
        borderwidth=2,
        highlightthickness=2,
        highlightbackground="#007AFF",
        highlightcolor="#007AFF"
    )
    title_input.pack(fill="x", ipady=5)
    
    return title_input


def create_text_area(parent) -> tuple[tk.Text, tk.Scrollbar, tk.Frame]:
    """
    Create text area and scrollbar
    
    Returns:
        (text_input, scrollbar, text_frame) tuple
    """
    text_frame = tk.Frame(parent, bg="#1a1a1a")
    text_frame.pack(pady=10, padx=20)
    
    text_input = tk.Text(
        text_frame,
        height=12,
        width=70,
        font=("Arial", 14),
        bg="white",
        fg="black",
        insertbackground="black",
        wrap=tk.WORD,
        relief=tk.SOLID,
        borderwidth=3,
        highlightthickness=3,
        highlightbackground="#007AFF",
        highlightcolor="#007AFF"
    )
    
    scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_input.yview)
    text_input.configure(yscrollcommand=scrollbar.set)
    
    text_input.insert("1.0", "Notunuzu buraya yazın...")
    text_input.config(fg="#999999")
    
    text_input.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    text_frame.grid_rowconfigure(0, weight=1)
    text_frame.grid_columnconfigure(0, weight=1)
    
    return text_input, scrollbar, text_frame


def create_buttons(parent, save_command, clear_command) -> tk.Frame:
    """
    Create buttons frame
    
    Args:
        parent: Parent widget
        save_command: Save button command
        clear_command: Clear button command
    
    Returns:
        button_frame
    """
    button_frame = tk.Frame(parent, bg="#1a1a1a")
    button_frame.pack(pady=10)
    
    save_btn = tk.Button(
        button_frame,
        text="💾 Kaydet",
        command=save_command,
        width=15,
        height=2,
        bg="#007AFF",
        fg="white",
        font=("Arial", 12),
        cursor="hand2"
    )
    save_btn.pack(side="left", padx=10)
    
    clear_btn = tk.Button(
        button_frame,
        text="🗑️ Temizle",
        command=clear_command,
        width=15,
        height=2,
        bg="#FF3B30",
        fg="white",
        font=("Arial", 12),
        cursor="hand2"
    )
    clear_btn.pack(side="left", padx=10)
    
    return button_frame


def create_labels(parent, notes_count: int) -> tuple[tk.Label, tk.Label]:
    """
    Create labels (note list and footer)
    
    Args:
        parent: Parent widget
        notes_count: Number of notes
    
    Returns:
        (notes_label, footer) tuple
    """
    notes_label = tk.Label(
        parent,
        text=f"Toplam {notes_count} not",
        font=("Arial", 14),
        bg="#1a1a1a",
        fg="white"
    )
    notes_label.pack(pady=10)
    
    footer = tk.Label(
        parent,
        text="💡 İpucu: Notlarınız otomatik olarak kaydedilir",
        font=("Arial", 11),
        bg="#1a1a1a",
        fg="gray"
    )
    footer.pack(pady=5)
    
    return notes_label, footer


def create_note_tabs(parent, notes, on_tab_select=None) -> ttk.Notebook:
    """
    Create tabs section to display notes
    
    Args:
        parent: Parent widget
        notes: List of Note objects
        on_tab_select: Callback function when tab is selected (receives note_id)
    
    Returns:
        notebook widget
    """
    notebook_frame = tk.Frame(parent, bg="#1a1a1a")
    notebook_frame.pack(fill="x", padx=20, pady=10)
    
    tabs_label = tk.Label(
        notebook_frame,
        text="📑 Saved Notes",
        font=("Arial", 14, "bold"),
        bg="#1a1a1a",
        fg="white"
    )
    tabs_label.pack(anchor="w", pady=(0, 10))
    
    notebook = ttk.Notebook(notebook_frame)
    notebook.pack(fill="x", pady=(0, 10))
    
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TNotebook', background='#1a1a1a', borderwidth=0)
    style.configure('TNotebook.Tab', 
                    background='#2a2a2a', 
                    foreground='white',
                    padding=[20, 10],
                    borderwidth=1)
    style.map('TNotebook.Tab',
              background=[('selected', '#007AFF')],
              foreground=[('selected', 'white')])
    
    for note in notes:
        tab_frame = tk.Frame(notebook, bg="#1a1a1a")
        notebook.add(tab_frame, text=get_tab_label(note))
        tab_frame.note_id = note.id
    
    if on_tab_select:
        notebook.bind("<<NotebookTabChanged>>", lambda e: on_tab_changed(notebook, on_tab_select))
    
    return notebook


def get_tab_label(note) -> str:
    """Generate label for tab from note"""
    if note.title:
        title = note.title[:20] + "..." if len(note.title) > 20 else note.title
        return f"📄 {title}"
    else:
        content_preview = note.content[:15].strip() if note.content else "Untitled"
        return f"📄 {content_preview}..."


def on_tab_changed(notebook, callback):
    """Handle tab change event"""
    selected_tab = notebook.index(notebook.select())
    tab_frame = notebook.nametowidget(notebook.tabs()[selected_tab])
    if hasattr(tab_frame, 'note_id'):
        callback(tab_frame.note_id)