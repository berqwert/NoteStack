import tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()
root.title("Test - Standart Tkinter")
root.geometry("800x600")
root.configure(bg="#1a1a1a")

# Başlık
title = tk.Label(
    root,
    text="📝 Notlarım",
    font=("Arial", 32, "bold"),
    bg="#1a1a1a",
    fg="white"
)
title.pack(pady=20)

# Text area container
text_frame = tk.Frame(root, bg="#1a1a1a")
text_frame.pack(pady=10, padx=20, fill="both", expand=True)

text_input = scrolledtext.ScrolledText(
    text_frame,
    height=15,
    width=70,
    font=("Arial", 14),
    bg="#2b2b2b",
    fg="white",
    insertbackground="white"
)
text_input.pack(fill="both", expand=True)

# Butonlar
button_frame = tk.Frame(root, bg="#1a1a1a")
button_frame.pack(pady=10)

save_btn = tk.Button(
    button_frame,
    text="💾 Kaydet",
    width=15,
    height=2,
    bg="#007AFF",
    fg="white",
    font=("Arial", 12)
)
save_btn.pack(side="left", padx=10)

clear_btn = tk.Button(
    button_frame,
    text="🗑️ Temizle",
    width=15,
    height=2,
    bg="#FF3B30",
    fg="white",
    font=("Arial", 12)
)
clear_btn.pack(side="left", padx=10)

# Label
notes_label = tk.Label(
    root,
    text="Toplam 0 not",
    font=("Arial", 14),
    bg="#1a1a1a",
    fg="white"
)
notes_label.pack(pady=10)

print("Standart Tkinter penceresi açılıyor...")
root.mainloop()

