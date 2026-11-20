import base64
import requests

from pathlib import Path

from config.settings import (
    CLOUDFLARE_ACCOUNT_ID,
    CLOUDFLARE_API_TOKEN,
)


class SpeechToTextProvider:

    def __init__(self):

        if not CLOUDFLARE_ACCOUNT_ID or not CLOUDFLARE_API_TOKEN:
            raise ValueError("Cloudflare credentials are missing.")

        self.model = "@cf/openai/whisper-large-v3-turbo"

        self.api_url = (
            "https://api.cloudflare.com/client/v4/accounts/"
            f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/{self.model}"
        )

        self.headers = {
            "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json",
        }

    def transcribe(self, audio_file: str) -> dict:

        audio_path = Path(audio_file)

        if not audio_path.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        audio_bytes = audio_path.read_bytes()

        if not audio_bytes:
            raise ValueError("Audio file is empty.")

        audio_base64 = base64.b64encode(
            audio_bytes
        ).decode("utf-8")

        payload = {
            "audio": audio_base64,
            "task": "transcribe",
            "language": "en",
            "vad_filter": True,
        }

        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        if not data.get("success", False):
            raise RuntimeError(
                f"Transcription failed: {data.get('errors')}"
            )

        result = data.get("result", {})
        transcript = result.get("text", "").strip()

        return {
            "text": transcript,
            "word_count": result.get("word_count", 0),
            "words": result.get("words", []),
            "transcript": transcript
        }

# if __name__ == "__main__":
#     stt_provider = SpeechToTextProvider()
#     audio_file_path = "recording.wav"  # Replace with your actual audio file path

#     try:
#         transcription_result = stt_provider.transcribe(audio_file_path)
#         print("Transcription Result:")
#         print(transcription_result)
#         print("\n\n\n" + transcription_result["transcript"])
#     except Exception as e:
#         print(f"Error during transcription: {e}")