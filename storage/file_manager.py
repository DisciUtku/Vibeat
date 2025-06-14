import json
import os

LIBRARY_PATH = "data/music_library.json"

def load_library():
    if not os.path.exists(LIBRARY_PATH):
        return []
    with open(LIBRARY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_library(new_tracks):
    existing_tracks = load_library()

    existing_index = {}
    for track in existing_tracks:
        key = track.get("filepath") or f"{track.get('title')}::{track.get('artist')}"
        existing_index[key] = track

    for new_track in new_tracks:
        key = new_track.get("filepath") or f"{new_track.get('title')}::{new_track.get('artist')}"
        existing_index[key] = new_track 

    final_tracks = list(existing_index.values())

    os.makedirs(os.path.dirname(LIBRARY_PATH), exist_ok=True)
    with open(LIBRARY_PATH, "w", encoding="utf-8") as f:
        json.dump(final_tracks, f, indent=4)
