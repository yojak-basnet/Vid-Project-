# frames.py
import os
import json
import shutil
from moviepy.editor import VideoFileClip

def extract_frames(video_path, interval_seconds=2,
                   frames_dir="outputs/frames",
                   meta_path="outputs/reports/frames_meta.json"):

    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # 🔥 CLEAN OLD OUTPUTS (fresh run every time)
    if os.path.isdir(frames_dir):
        shutil.rmtree(frames_dir)          # deletes all old frames
    os.makedirs(frames_dir, exist_ok=True)

    meta_dir = os.path.dirname(meta_path)
    os.makedirs(meta_dir, exist_ok=True)

    if os.path.exists(meta_path):
        os.remove(meta_path)               # deletes old metadata file

    frames_info = []

    with VideoFileClip(video_path) as clip:
        duration = clip.duration
        t = 0.0
        idx = 0

        while t < duration:
            frame_path = os.path.join(frames_dir, f"frame_{idx:05d}.png")
            clip.save_frame(frame_path, t=t)

            frames_info.append({
                "time": round(t, 3),
                "path": os.path.abspath(frame_path)
            })

            idx += 1
            t += interval_seconds

    with open(meta_path, "w") as f:
        json.dump(frames_info, f, indent=2)

    return frames_info
