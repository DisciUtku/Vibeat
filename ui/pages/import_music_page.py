import os
import threading
import customtkinter as ctk
from tkinter import filedialog
from analysis.metadata_parser import extract_metadata
from analysis.visualizer import animate_waveform
from storage.file_manager import save_library, load_library

class ImportMusicPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.status_label = ctk.CTkLabel(self, text="Waiting to import music...")
        self.status_label.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(self, mode="determinate")
        self.progress_bar.set(0)
        self.progress_bar.pack(padx=20, pady=5, fill="x")

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=5)

        self.import_button = ctk.CTkButton(button_frame, text="Import Files", command=self.import_music_files)
        self.import_button.pack(side="left", padx=10)

        self.import_dir_button = ctk.CTkButton(button_frame, text="Import Folder", command=self.import_music_folder)
        self.import_dir_button.pack(side="left", padx=10)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=700, height=300)
        self.scrollable_frame.pack(pady=10, padx=10, fill="both", expand=False)

        self.waveform_frame = ctk.CTkFrame(self)
        self.waveform_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.load_and_display_tracks()

    def import_music_files(self):
        filetypes = [("Audio Files", "*.mp3 *.wav"), ("All files", "*.*")]
        files = filedialog.askopenfilenames(title="Select Music Files", filetypes=filetypes)
        threading.Thread(target=self.process_files, args=(files,), daemon=True).start()

    def import_music_folder(self):
        folder = filedialog.askdirectory(title="Select Music Folder")
        if not folder:
            return
        valid_ext = ('.mp3', '.wav')
        files = []
        for root, _, filenames in os.walk(folder):
            for name in filenames:
                if name.lower().endswith(valid_ext):
                    files.append(os.path.join(root, name))
        threading.Thread(target=self.process_files, args=(files,), daemon=True).start()

    def process_files(self, files):
        if not files:
            print("No files selected.")
            return

        library = load_library()
        existing_paths = {os.path.abspath(track.get("filepath", "")) for track in library}
        all_metadata = []
        failed_count = 0
        skipped_count = 0

        if self.winfo_exists():
            self.after(0, lambda: self.progress_bar.configure(mode="indeterminate"))
            self.after(0, self.progress_bar.start)

        for f in files:
            normalized_path = os.path.abspath(f)

            if normalized_path in existing_paths:
                skipped_count += 1
                continue

            data = extract_metadata(normalized_path)
            if data:
                all_metadata.append(data)
                if self.winfo_exists():
                    self.after(0, lambda title=data["title"]: self.status_label.configure(text=f"Analyzing: {title}"))
                    self.after(0, lambda path=normalized_path: animate_waveform(path, self.waveform_frame))
            else:
                failed_count += 1

        if self.winfo_exists():
            self.after(0, self.progress_bar.stop)
            self.after(0, lambda: self.progress_bar.configure(mode="determinate"))
            self.after(0, lambda: self.progress_bar.set(1.0))

        save_library(all_metadata)

        if self.winfo_exists():
            self.after(0, self.load_and_display_tracks)

            message = "Done! ✅"
            if failed_count > 0:
                message += f" {failed_count} file(s) failed."
            if skipped_count > 0:
                message += f" {skipped_count} file(s) skipped (already imported)."

            self.after(0, lambda: self.status_label.configure(text=message))

    def load_and_display_tracks(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        library = load_library()
        for track in library:
            text = f"{track['title']} - {track['artist']} | {track.get('mood', 'Unknown')}"
            label = ctk.CTkLabel(self.scrollable_frame, text=text, anchor="w")
            label.pack(fill="x", padx=10, pady=2)
