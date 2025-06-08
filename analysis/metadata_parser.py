from mutagen import File
from mutagen import mp3
from analysis.mood_classifier import (
    analyze_bpm,
    estimate_key,
    estimate_danceability,
    estimate_energy,
    detect_mood
)
import librosa

def extract_metadata(filepath):
    try:
        audio = File(filepath)
        if audio is None or not hasattr(audio, "info"):
            raise ValueError("Unsupported or unreadable file")

        title = str(audio.tags.get("TIT2", "Unknown")) if audio.tags else "Unknown"
        artist = str(audio.tags.get("TPE1", "Unknown")) if audio.tags else "Unknown"
        duration = round(audio.info.length, 2)

        bpm = analyze_bpm(filepath)
        key = estimate_key(filepath)
        danceability = estimate_danceability(*librosa.load(filepath, duration=60.0))
        energy = estimate_energy(*librosa.load(filepath, duration=60.0))
        mood = detect_mood(bpm, key, danceability, energy)

        return {
            "title": title,
            "artist": artist,
            "duration": float(duration),
            "bpm": float(bpm),
            "key": key,
            "danceability": float(danceability),
            "energy": float(energy),
            "mood": mood,
            "filepath": filepath
        }

    except Exception as e:
        print(f"⚠️ Failed to analyze {filepath}: {e}")
        return None