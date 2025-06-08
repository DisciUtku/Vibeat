import customtkinter as ctk
import os
import json

LIBRARY_PATH = "data/music_library.json"

class PreferencesPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        title_label = ctk.CTkLabel(self, text="⚙️ Preferences", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20)

        clear_button = ctk.CTkButton(
            self, text="🗑️ Clear Music Library", fg_color="red", hover_color="darkred",
            command=self.clear_library
        )
        clear_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=5)

    def clear_library(self):
        try:
            if os.path.exists(LIBRARY_PATH):
                with open(LIBRARY_PATH, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=4)
                self.status_label.configure(text="✅ Music library has been cleared.")
            else:
                self.status_label.configure(text="⚠️ Library file does not exist.")
        except Exception as e:
            self.status_label.configure(text=f"❌ Error: {e}")
