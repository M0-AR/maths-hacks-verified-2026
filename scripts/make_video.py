"""Make docs/assets/demo.mp4 if imageio-ffmpeg is available; else reuse the GIF.

GitHub READMEs play GIFs everywhere but strip raw <video> tags, so the repo
treats GIF as primary and MP4/YouTube as progressive enhancement.
"""
from __future__ import annotations
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ROOT = Path(__file__).resolve().parents[1]
OUT_GIF = ROOT / "docs" / "assets" / "demo_brownian.gif"
OUT_MP4 = ROOT / "docs" / "assets" / "demo.mp4"


def main() -> Path:
    import random
    rnd = random.Random(12345)
    paths = [[0.0] for _ in range(5)]
    for _ in range(80):
        for p in paths:
            p.append(p[-1] + rnd.gauss(0, 0.12))
    fig, ax = plt.subplots(figsize=(6, 3.5))
    lines = [ax.plot([], [], lw=1.5)[0] for _ in range(5)]
    ax.set_xlim(0, 80); ax.set_ylim(-4, 4)
    ax.set_title("Demo: 5 Wiener paths grow like sqrt(t)")
    ax.grid(alpha=0.3)

    def update(f):
        for ln, p in zip(lines, paths):
            ln.set_data(range(f + 1), p[:f + 1])
        return lines

    ani = animation.FuncAnimation(fig, update, frames=80, interval=60, blit=True)
    try:
        import imageio_ffmpeg  # noqa: F401
        import matplotlib as mpl
        mpl.rcParams["animation.ffmpeg_path"] = __import__("imageio_ffmpeg").get_ffmpeg_exe()
        ani.save(OUT_MP4, writer="ffmpeg", fps=12)
        print(f"wrote {OUT_MP4} ({OUT_MP4.stat().st_size//1024} KB)")
        plt.close(fig)
        return OUT_MP4
    except Exception as e:
        print(f"ffmpeg unavailable ({e}); GIF remains canonical: {OUT_GIF}")
        plt.close(fig)
        return OUT_GIF


if __name__ == "__main__":
    print(main())
