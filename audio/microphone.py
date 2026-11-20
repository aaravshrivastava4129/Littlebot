import sounddevice as sd
import soundfile as sf
import numpy as np

from pathlib import Path
from threading import Event, Thread

class Microphone:
    def __init__(self, sample_rate: int = 16000, channels: int = 1):

        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.audio_data = []
        self.stop_event = Event()
        self.stream = None

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print("Audio Status:", status)

        if self.recording:
            self.audio_data.append(indata.copy())

    def start_recording(self):

        if self.recording:
            print("Already recording.")
            return

        self.audio_data = []
        self.recording = True

        self.stream = sd.InputStream(samplerate=self.sample_rate, channels=self.channels, callback=self._audio_callback, dtype='float32')

        self.stream.start()
        print("Listening... Press ENTER to stop.")

    def stop_recording(self, output_file: str = "recording.wav"):

        if not self.recording:
            print("Not currently recording.")
            return None

        self.recording = False

        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        if not self.audio_data:
            print("No audio data recorded.")
            return None

        audio = np.concatenate(self.audio_data, axis=0)
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        sf.write(str(output_path), audio, self.sample_rate)

        print(f"Recording saved: {output_path}")

        return str(output_path)

# if __name__ == "__main__":
#     mic = Microphone(sample_rate=16000, channels=1)
#     input("Press ENTER to start recording...")
#     mic.start_recording()

#     input()

#     mic.stop_recording("recording.wav")