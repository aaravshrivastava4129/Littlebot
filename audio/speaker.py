import sounddevice as sd
import soundfile as sf

from pathlib import Path


class Speaker:

    def __init__(self, volume: float = 0.8):

        if not 0.0 <= volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0.")

        self.volume = volume
        self.current_stream = None

    def set_volume(self, volume: float):

        if not 0.0 <= volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0.")

        self.volume = volume

    def play(self, audio_file: str):

        path = Path(audio_file)

        if not path.is_file():
            raise FileNotFoundError(
                f"Audio file not found: {path}"
            )

        audio, sample_rate = sf.read(
            str(path),
            dtype="float32"
        )

        audio = audio * self.volume

        sd.play(audio, samplerate=sample_rate)
        sd.wait()

    def stop(self):

        sd.stop()

    def close(self):

        self.stop()
