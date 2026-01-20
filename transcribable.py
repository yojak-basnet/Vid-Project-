# transcribable.py
import os
import json
import whisper

OUTPUT_PATH = "outputs/reports/transcript.json"

def audio_to_text(audio_path: str, model_size: str = "base") -> str:
    """
    Transcribes audio and writes outputs/reports/transcript.json
    Returns the path to the JSON file.
    """
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)

    transcript = {
        "text": result.get("text", ""),
        "segments": [
            {
                "start": float(seg.get("start", 0.0)),
                "end": float(seg.get("end", 0.0)),
                "text": str(seg.get("text", "")).strip()
            }
            for seg in result.get("segments", [])
        ]
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(transcript, f, indent=2)

    return OUTPUT_PATH
