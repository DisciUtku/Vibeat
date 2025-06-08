# Vibeat — Music Mood Analyzer

**Vibeat** is a desktop app that scans your music library, analyzes each track's mood, tempo, key, danceability, and energy — and visualizes it beautifully with waveform animations.

> A smart, offline-first music utility with a clean interface and deep audio insight — built with Python and CustomTkinter.

---

## Features

-  **Import Music**: Add `.mp3` or `.wav` files or folders to your library
-  **Analyze Mood**: Detects musical **mood**, **key**, **BPM**, **energy**, and **danceability**
-  **Waveform Animation**: Visual progress as each song is scanned
-  **Skips previously analyzed tracks**
-  **Simple library browser**
-  **JSON-based lightweight storage**
-  **No internet or external server required**

---

##  Installation

```bash
git clone https://github.com/disciutku/Vibeat.git
cd Vibeat
python -m venv .venv
.venv\\Scripts\\activate  # or source .venv/bin/activate
pip install -r requirements.txt
python main.py

Dependencies

 - CustomTkinter

 - Librosa

 - Mutagen

 - Matplotlib

 - NumPy


 ## Acknowledgements
Made with Python by Utku Disci