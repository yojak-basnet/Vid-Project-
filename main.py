import os
import shutil

from extract_audio import extract_audio
from transcribable import audio_to_text
from frames import extract_frames
from analyze import analyze_transcript

FRAMES_DIR = "outputs/frames"
REPORTS_DIR = "outputs/reports"

TRANSCRIPT_PATH = os.path.join(REPORTS_DIR, "transcript.json")
FRAMES_META_PATH = os.path.join(REPORTS_DIR, "frames_meta.json")
API_RESULT_PATH = os.path.join(REPORTS_DIR, "api_result.json")


def clean_outputs():
    if os.path.isdir(FRAMES_DIR):
        shutil.rmtree(FRAMES_DIR)

    os.makedirs(FRAMES_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    for p in [TRANSCRIPT_PATH, FRAMES_META_PATH, API_RESULT_PATH]:
        if os.path.exists(p):
            os.remove(p)


def get_video_path():
    video_path = input("Enter full path to video: ").strip().strip('"').strip("'")
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    return video_path


def main():
    try:
        video_path = get_video_path()
        clean_outputs()

        frames_info = extract_frames(
            video_path,
            interval_seconds=2,
            frames_dir=FRAMES_DIR,
            meta_path=FRAMES_META_PATH
        )
        print(f"Extracted {len(frames_info)} frames")

        audio_path = extract_audio(video_path)
        print(f"Audio extracted: {audio_path}")

        transcript_path = audio_to_text(audio_path)
        print(f"Transcript saved: {transcript_path}")

        api_result_path = analyze_transcript(
            transcript_path=transcript_path,
            frames_meta_path=FRAMES_META_PATH,
            output_path=API_RESULT_PATH
        )
        print(f"Policy analysis saved: {api_result_path}")

    except Exception as e:
        print("Pipeline error:", e)


if __name__ == "__main__":
    main()
