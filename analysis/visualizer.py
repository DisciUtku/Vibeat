import time
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import random

def animate_waveform(filepath, frame, duration=10):
    for widget in frame.winfo_children():
        widget.destroy()

    try:
        y, sr = librosa.load(filepath, duration=duration)
        total_duration = librosa.get_duration(y=y, sr=sr)

        fig, ax = plt.subplots(figsize=(6, 2), dpi=100)
        ax.set_title("Waveform", fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor("#1a1a1a")
        fig.patch.set_facecolor("#1a1a1a")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # 🎨 Rastgele colormap seçimi
        color_maps = [
            "viridis", "cool", "magma", "twilight",
            "hsv", "inferno", "cividis", "plasma"
        ]
        cmap_name = random.choice(color_maps)
        cmap = cm.get_cmap(cmap_name)

        norm = mcolors.Normalize(vmin=0, vmax=len(y))
        segment_count = 30  # ⏩ daha kısa animasyon
        segment_length = len(y) // segment_count
        time_array = np.linspace(0, total_duration, num=len(y))

        for i in range(1, segment_count + 1):
            ax.clear()
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xlim(0, (i / segment_count) * total_duration)
            ax.set_ylim(-1.05, 1.05)
            ax.set_facecolor("#1a1a1a")

            for j in range(0, i * segment_length, segment_length):
                if j + segment_length >= len(y):
                    break
                start = j
                end = j + segment_length
                color = cmap(norm(j))
                ax.fill_between(
                    time_array[start:end],
                    y[start:end],
                    color=color,
                    linewidth=0.5,
                    alpha=0.9
                )

            canvas.draw()
            frame.update()
            time.sleep(0.025)  # ⏩ daha hızlı geçiş

    except Exception as e:
        print(f"Waveform animation error: {e}")
