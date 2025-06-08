import customtkinter as ctk
from storage.file_manager import load_library

class AllSongsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        title_label = ctk.CTkLabel(self, text="🎶 All Songs", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20)

        scrollable_frame = ctk.CTkScrollableFrame(self, width=800, height=500)
        scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.display_all_songs(scrollable_frame)

    def display_all_songs(self, frame):
        library = load_library()
        for track in library:
            text = f"{track['title']} - {track['artist']} | Mood: {track.get('mood', 'Unknown')}"
            label = ctk.CTkLabel(frame, text=text, anchor="w")
            label.pack(fill="x", padx=10, pady=4)
