import customtkinter as ctk

class PlaylistsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        title_label = ctk.CTkLabel(self, text="📂 Playlists", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20)

        info_label = ctk.CTkLabel(self, text="This is where playlist creation and management will be implemented.")
        info_label.pack(pady=10)
