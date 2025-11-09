import tkinter as tk


def create_options_button(parent) -> tk.Button:
    """
    Create options button in top right
    
    Returns:
        options_button
    """
    # Top right frame
    top_frame = tk.Frame(parent, bg="#1a1a1a")
    top_frame.pack(fill="x", pady=10, padx=10)
    
    # Options button
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
    # Label
    title_label = tk.Label(
        parent,
        text="Başlık:",
        font=("Arial", 12),
        bg="#1a1a1a",
        fg="white"
    )
    title_label.pack(pady=(10, 5), padx=20, anchor="w")
    
    # Entry frame
    title_frame = tk.Frame(parent, bg="#1a1a1a")
    title_frame.pack(pady=(0, 10), padx=20, fill="x")
    
    # Entry widget
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
    # Text area frame
    text_frame = tk.Frame(parent, bg="#1a1a1a")
    text_frame.pack(pady=10, padx=20)
    
    # Text input widget
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
    
    # Scrollbar
    scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_input.yview)
    text_input.configure(yscrollcommand=scrollbar.set)
    
    # Add placeholder text
    text_input.insert("1.0", "Notunuzu buraya yazın...")
    text_input.config(fg="#999999")
    
    # Layout - use grid
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
    
    # Save button
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
    
    # Clear button
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
    # Notes list label
    notes_label = tk.Label(
        parent,
        text=f"Toplam {notes_count} not",
        font=("Arial", 14),
        bg="#1a1a1a",
        fg="white"
    )
    notes_label.pack(pady=10)
    
    # Footer
    footer = tk.Label(
        parent,
        text="💡 İpucu: Notlarınız otomatik olarak kaydedilir",
        font=("Arial", 11),
        bg="#1a1a1a",
        fg="gray"
    )
    footer.pack(pady=5)
    
    return notes_label, footer

