import customtkinter as ctk
from ui.pages.import_music_page import ImportMusicPage
from ui.pages.playlists_page import PlaylistsPage
from ui.pages.all_songs_page import AllSongsPage
from ui.pages.mood_board_page import MoodBoardPage
from ui.pages.preferences_page import PreferencesPage
from ui.pages.music_player_page import MusicPlayerPage

# Global erişim için tanımlar
global_progress_label = None
global_progress_bar = None

def set_global_progress(value):
    if global_progress_bar:
        global_progress_bar.set(value)

def set_global_value(text):
    if global_progress_label:
        global_progress_label.configure(text=text)

def launch_app():
    global global_progress_bar, global_progress_label

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
        if page_class == ImportMusicPage:
           page = page_class(content_frame, update_progress=(set_global_progress, set_global_value))
        else:
            page = page_class(content_frame)
        page.pack(expand=True, fill="both")
        current_page["widget"] = page


    nav_buttons = [
        ("🎵 Import Music", lambda: show_page(ImportMusicPage)),
        ("📂 Playlists", lambda: show_page(PlaylistsPage)),
        ("🎧 Music Player", lambda: show_page(MusicPlayerPage)),
        ("🎶 All Songs", lambda: show_page(AllSongsPage)),
        ("📊 Mood Board", lambda: show_page(MoodBoardPage)),
        ("⚙️ Preferences", lambda: show_page(PreferencesPage))
    ]

    for text, command in nav_buttons:
        btn = ctk.CTkButton(sidebar_frame, text=text, command=command)
        btn.pack(pady=10, padx=10, fill="x")

    # Progress bar ve label EN ALTA taşındı
    global_progress_label = ctk.CTkLabel(sidebar_frame, text="")
    global_progress_label.pack(side="bottom", pady=(0, 2), padx=10)

    global_progress_bar = ctk.CTkProgressBar(sidebar_frame, mode="determinate")
    global_progress_bar.set(0)
    global_progress_bar.pack(side="bottom", padx=10, pady=(0, 10), fill="x")

    show_page(ImportMusicPage)
    app.mainloop()
