import customtkinter as ctk
from ui.pages.import_music_page import ImportMusicPage
from ui.pages.playlists_page import PlaylistsPage
from ui.pages.all_songs_page import AllSongsPage
from ui.pages.mood_board_page import MoodBoardPage
from ui.pages.preferences_page import PreferencesPage

def launch_app():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Vibeat - Music Mood Analyzer")
    app.geometry("1100x750")

    sidebar_frame = ctk.CTkFrame(app, width=200)
    sidebar_frame.pack(side="left", fill="y")

    content_frame = ctk.CTkFrame(app)
    content_frame.pack(side="right", expand=True, fill="both")

    current_page = {"widget": None}

    def clear_page():
        if current_page["widget"] is not None:
            current_page["widget"].destroy()

    def show_page(page_class):
        clear_page()
        page = page_class(content_frame)
        page.pack(expand=True, fill="both")
        current_page["widget"] = page

    # Menü butonları
    nav_buttons = [
        ("🎵 Import Music", lambda: show_page(ImportMusicPage)),
        ("📂 Playlists", lambda: show_page(PlaylistsPage)),
        ("🎶 All Songs", lambda: show_page(AllSongsPage)),
        ("📊 Mood Board", lambda: show_page(MoodBoardPage)),
        ("⚙️ Preferences", lambda: show_page(PreferencesPage))
    ]

    for text, command in nav_buttons:
        btn = ctk.CTkButton(sidebar_frame, text=text, command=command)
        btn.pack(pady=10, padx=10, fill="x")

    # Varsayılan sayfa
    show_page(ImportMusicPage)

    app.mainloop()
