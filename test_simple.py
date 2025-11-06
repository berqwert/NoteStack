import customtkinter as ctk

# Test basit bir pencere
root = ctk.CTk()
root.title("Test")
root.geometry("400x300")
ctk.set_appearance_mode("dark")

label = ctk.CTkLabel(root, text="Bu bir test label", font=ctk.CTkFont(size=20))
label.pack(pady=50)

button = ctk.CTkButton(root, text="Test Butonu", width=150, height=40)
button.pack(pady=20)

print("Pencere açılıyor...")
root.mainloop()

