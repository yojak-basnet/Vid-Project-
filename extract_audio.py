# extract_audio.py
import os
from moviepy.editor import VideoFileClip

def extract_audio(video_path):
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    audio_path = "extracted_audio.wav"

    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, codec="pcm_s16le")
    video.close()

    return audio_path
