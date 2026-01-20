import json
import os
from openai import OpenAI

TRANSCRIPT_PATH = "outputs/reports/transcript.json"
FRAMES_META_PATH = "outputs/reports/frames_meta.json"
OUTPUT_PATH = "outputs/reports/api_result.json"

from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def analyze_transcript(transcript_path=TRANSCRIPT_PATH, frames_meta_path=FRAMES_META_PATH, output_path=OUTPUT_PATH):
    client = OpenAI()

    if not os.path.exists(transcript_path):
        raise FileNotFoundError("transcript.json not found")

    with open(transcript_path, "r") as f:
        transcript = json.load(f)

    segments = transcript.get("segments", [])
    if not segments:
        raise ValueError("Transcript has no segments")

    frames_meta = []
    if os.path.exists(frames_meta_path):
        with open(frames_meta_path, "r") as f:
            frames_meta = json.load(f)

    prompt = {
        "task": "Analyze transcript segments for YouTube policy violations.",
        "rules": [
            "Return ONLY a valid JSON object.",
            "If the content is safe, return: {\"violations\": []}.",
            "If content violates policy, return the EXACT sentence text as it appears.",
            "Use the EXACT start and end timestamps from the segment.",
            "Do not invent timestamps or rewrite text.",
            "Be conservative. Only flag content that clearly violates policy."
        ],
        "violation_categories": [
            "sexual content & nudity",
            "violence & graphic content",
            "hate speech & harassment",
            "self-harm & suicide",
            "drugs & alcohol",
            "weapons & dangerous activities",
            "misinformation & deception",
            "child safety violations",
            "spam & scams",
            "copyright & reused content"
        ],
        "output_format": {
            "violations": [
                {
                    "violation": "one of the violation_categories",
                    "text": "exact sentence from segment",
                    "time_range": [0.0, 0.0]
                }
            ]
        },
        "segments": segments,
        "frames_meta_info": {
            "note": "Frames are available but not analyzed yet.",
            "num_frames": len(frames_meta) if isinstance(frames_meta, list) else 0
        }
    }

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "You output ONLY a valid JSON object. No extra text."},
            {"role": "user", "content": json.dumps(prompt)}
        ],
        text={"format": {"type": "json_object"}}
    )

    raw_text = response.output_text
    if not raw_text:
        result = {"violations": []}
    else:
        result = json.loads(raw_text)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    return output_path


if __name__ == "__main__":
    analyze_transcript()
