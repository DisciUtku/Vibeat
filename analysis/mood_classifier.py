import librosa
from scipy.signal import find_peaks
import numpy as np

def analyze_bpm(filepath):
    try:
        y, sr = librosa.load(filepath, mono=True, duration=60.0)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

        if isinstance(tempo, (list, tuple, np.ndarray)):
            tempo = tempo[0]

        if tempo < 30 or tempo > 250:
            raise ValueError("Unrealistic tempo detected")

        return round(float(tempo), 2)
    except Exception as e:
        print(f"BPM analysis failed for {filepath}: {e}")
        return 0

def estimate_key(filepath):
    try:
        y, sr = librosa.load(filepath)
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        chroma_avg = chroma.mean(axis=1)
        key_index = chroma_avg.argmax()

        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        return keys[key_index]
    except Exception as e:
        print(f"Key estimation failed: {e}")
        return "Unknown"

def detect_mood(bpm, key, danceability, energy):
    if bpm == 0 or key == "Unknown":
        return "Unknown"

    energetic_keys = ['C', 'G', 'F']
    emotional_keys = ['A', 'D', 'E', 'B']

    if bpm >= 120 and energy > 0.1 and key in energetic_keys:
        return "Energetic / Confident"  # MIREX 1
    elif 90 <= bpm < 120 and danceability > 0.6:
        return "Cheerful / Fun"         # MIREX 2
    elif bpm < 90 and energy < 0.08 and key in emotional_keys:
        return "Emotional / Reflective" # MIREX 3
    elif 100 <= bpm <= 140 and energy > 0.12 and key in energetic_keys:
        return "Intense / Aggressive"   # MIREX 5
    else:
        return "Quirky / Unusual"       # MIREX 4

def estimate_danceability(y, sr):
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    if len(beats) < 2:
        return 0.0

    intervals = np.diff(librosa.frames_to_time(beats, sr=sr))
    variation = np.std(intervals)
    variation = np.clip(variation, 0, 0.5)

    danceability_score = 1 - (variation / 0.5)  # varyasyon 0.5 ise 0.0; 0.0 ise 1.0
    return round(danceability_score, 3)

def estimate_energy(y, sr):
    rms = librosa.feature.rms(y=y)[0]
    return round(np.mean(rms), 4)

def generateMoodDistribution(library):
    mood_counts = {}
    for track in library:
        mood = track.get("mood", "Unknown")
        mood_counts[mood] = mood_counts.get(mood, 0) + 1
    return mood_counts
