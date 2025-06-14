import os
import pygame
import customtkinter as ctk
from tkinter import filedialog
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from PIL import Image, ImageTk
import io
from mutagen.id3 import ID3
import time

class MusicPlayerPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        pygame.mixer.init()
        self.current_file = None
        self.duration = 0
        self.updating_slider = True
        self.volume = 0.5
        self.is_playing = False
        self.current_position = 0
        self.seeking = False
        pygame.mixer.music.set_volume(self.volume)

        # Main container
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Album art frame
        self.album_frame = ctk.CTkFrame(self.main_container, width=300, height=300)
        self.album_frame.pack(pady=20)
        self.album_label = ctk.CTkLabel(self.album_frame, text="", font=("Arial", 14))
        self.album_label.pack(expand=True)
        self.album_image = None

        # Track info frame
        self.info_frame = ctk.CTkFrame(self.main_container)
        self.info_frame.pack(fill="x", pady=10)

        self.track_label = ctk.CTkLabel(self.info_frame, text="No track loaded", font=("Arial", 20, "bold"))
        self.track_label.pack()

        self.artist_label = ctk.CTkLabel(self.info_frame, text="Unknown Artist", font=("Arial", 16))
        self.artist_label.pack()

        # Time labels
        self.time_frame = ctk.CTkFrame(self.main_container)
        self.time_frame.pack(fill="x", pady=5)
        
        self.current_time_label = ctk.CTkLabel(self.time_frame, text="00:00", font=("Arial", 12))
        self.current_time_label.pack(side="left", padx=10)
        
        self.total_time_label = ctk.CTkLabel(self.time_frame, text="00:00", font=("Arial", 12))
        self.total_time_label.pack(side="right", padx=10)

        # Progress bar
        self.progress_var = ctk.DoubleVar()
        self.slider = ctk.CTkSlider(self.main_container, from_=0, to=100, variable=self.progress_var)
        self.slider.pack(fill="x", padx=20, pady=10)
        self.slider.bind("<ButtonRelease-1>", self.seek)
        self.slider.bind("<Button-1>", self.on_slider_click)
        self.slider.bind("<B1-Motion>", self.on_slider_drag)

        # Controls frame
        controls = ctk.CTkFrame(self.main_container)
        controls.pack(pady=10)

        # Volume control
        self.volume_frame = ctk.CTkFrame(controls)
        self.volume_frame.pack(side="left", padx=20)
        
        self.volume_label = ctk.CTkLabel(self.volume_frame, text="🔊", font=("Arial", 16))
        self.volume_label.pack(side="left", padx=5)
        
        self.volume_slider = ctk.CTkSlider(self.volume_frame, from_=0, to=1, width=100, command=self.set_volume)
        self.volume_slider.set(self.volume)
        self.volume_slider.pack(side="left", padx=5)

        # Playback controls
        self.play_button = ctk.CTkButton(controls, text="▶", width=40, command=self.toggle_play)
        self.play_button.pack(side="left", padx=10)

        self.next_button = ctk.CTkButton(controls, text="⏭", width=40, command=self.next_song)
        self.next_button.pack(side="left", padx=10)

        self.load_button = ctk.CTkButton(controls, text="Load Track", command=self.load_file)
        self.load_button.pack(side="left", padx=10)

        self.after(100, self.update_slider)

    def on_slider_click(self, event):
        self.seeking = True
        if self.is_playing:
            pygame.mixer.music.pause()

    def on_slider_drag(self, event):
        if self.seeking and self.current_file:
            value = self.progress_var.get()
            position = (value / 100) * self.duration
            self.current_time_label.configure(text=self.format_time(position))

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def load_file(self):
        filetypes = [("Audio Files", "*.mp3 *.wav")]
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            self.current_file = filepath
            self.load_metadata(filepath)
            self.duration = self.get_audio_length(filepath)
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            self.is_playing = True
            self.play_button.configure(text="⏸")
            self.total_time_label.configure(text=self.format_time(self.duration))

    def next_song(self):
        if self.current_file:
            # Get the directory of the current file
            current_dir = os.path.dirname(self.current_file)
            current_file = os.path.basename(self.current_file)
            
            # Get all audio files in the directory
            audio_files = [f for f in os.listdir(current_dir) if f.endswith(('.mp3', '.wav'))]
            
            if len(audio_files) > 1:
                # Find the index of current file
                current_index = audio_files.index(current_file)
                # Get the next file (loop back to start if at end)
                next_index = (current_index + 1) % len(audio_files)
                next_file = os.path.join(current_dir, audio_files[next_index])
                
                print(f"Loading next song: {next_file}")  # Debug print
                
                # Load and play the next file
                self.current_file = next_file
                self.load_metadata(next_file)
                self.duration = self.get_audio_length(next_file)
                
                # Stop current playback
                pygame.mixer.music.stop()
                # Load and play new file
                pygame.mixer.music.load(next_file)
                pygame.mixer.music.play()
                
                self.is_playing = True
                self.play_button.configure(text="⏸")
                self.total_time_label.configure(text=self.format_time(self.duration))
                self.progress_var.set(0)
                self.current_time_label.configure(text="00:00")

    def load_metadata(self, filepath):
        try:
            if filepath.endswith('.mp3'):
                audio = ID3(filepath)
                # Get title
                title = str(audio.get('TIT2', 'Unknown Title'))
                self.track_label.configure(text=title)
                
                # Get artist
                artist = str(audio.get('TPE1', 'Unknown Artist'))
                self.artist_label.configure(text=artist)
                
                # Get album art
                if 'APIC:' in audio:
                    artwork = audio['APIC:'].data
                    image = Image.open(io.BytesIO(artwork))
                    image = image.resize((300, 300), Image.Resampling.LANCZOS)
                    # Convert to CTkImage
                    self.album_image = ctk.CTkImage(light_image=image, dark_image=image, size=(300, 300))
                    self.album_label.configure(image=self.album_image, text="")
                else:
                    self.album_label.configure(image=None, text="No Album Art")
            else:
                self.track_label.configure(text=os.path.basename(filepath))
                self.artist_label.configure(text="Unknown Artist")
                self.album_label.configure(image=None, text="No Album Art")
        except Exception as e:
            print(f"Error loading metadata: {e}")
            self.track_label.configure(text=os.path.basename(filepath))
            self.artist_label.configure(text="Unknown Artist")
            self.album_label.configure(image=None, text="No Album Art")

    def toggle_play(self):
        if not self.current_file:
            return
            
        if self.is_playing:
            pygame.mixer.music.pause()
            self.play_button.configure(text="▶")
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()
            self.play_button.configure(text="⏸")
            self.is_playing = True

    def update_slider(self):
        if not self.seeking and self.current_file:
            if pygame.mixer.music.get_busy():
                pos = pygame.mixer.music.get_pos() / 1000.0
                self.current_position = pos
                if self.duration > 0:
                    progress = (pos / self.duration) * 100
                    self.progress_var.set(progress)
                    self.current_time_label.configure(text=self.format_time(pos))
            elif self.is_playing:
                # If we're supposed to be playing but get_busy() is False,
                # the song might have ended or had an error
                self.is_playing = False
                self.play_button.configure(text="▶")
                self.progress_var.set(0)
                self.current_time_label.configure(text="00:00")
        self.after(100, self.update_slider)

    def seek(self, event=None):
        if self.current_file and self.duration:
            self.seeking = False
            value = self.progress_var.get()
            position = (value / 100) * self.duration
            
            print(f"Seeking to position: {position} seconds")  # Debug print
            
            # Stop current playback
            pygame.mixer.music.stop()
            # Load the file again
            pygame.mixer.music.load(self.current_file)
            # Set the position before playing
            pygame.mixer.music.play(start=position)
            
            # Ensure we're in the correct play state
            if self.is_playing:
                pygame.mixer.music.unpause()
                self.play_button.configure(text="⏸")
            else:
                pygame.mixer.music.pause()
                self.play_button.configure(text="▶")
            
            # Force an immediate update of the current position
            self.current_position = position
            self.current_time_label.configure(text=self.format_time(position))
            
            # Start a timer to check if the music actually started playing
            def check_playback():
                if not pygame.mixer.music.get_busy() and self.is_playing:
                    print("Playback didn't start, retrying...")
                    pygame.mixer.music.play(start=position)
                    self.after(100, check_playback)
            
            self.after(100, check_playback)

    def set_volume(self, value):
        self.volume = value
        pygame.mixer.music.set_volume(value)
        if value == 0:
            self.volume_label.configure(text="🔇")
        elif value < 0.5:
            self.volume_label.configure(text="🔉")
        else:
            self.volume_label.configure(text="🔊")

    def get_audio_length(self, path):
        try:
            if path.endswith(".mp3"):
                audio = MP3(path)
            else:
                audio = WAVE(path)
            return audio.info.length
        except:
            return 0
