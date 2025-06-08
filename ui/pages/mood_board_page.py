import customtkinter as ctk
from storage.file_manager import load_library

class MoodBoardPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        title_label = ctk.CTkLabel(self, text="📊 Mood Board", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20)

        info_label = ctk.CTkLabel(self, text="This page will visualize mood distribution and other stats.")
        info_label.pack(pady=10)

        self.display_mood_stats()

    def display_mood_stats(self):
        library = load_library()
        mood_counts = {}

        for track in library:
            mood = track.get("mood", "Unknown")
            mood_counts[mood] = mood_counts.get(mood, 0) + 1

        for mood, count in mood_counts.items():
            label = ctk.CTkLabel(self, text=f"{mood}: {count} track(s)", anchor="w")
            label.pack(pady=2, padx=20, anchor="w")
