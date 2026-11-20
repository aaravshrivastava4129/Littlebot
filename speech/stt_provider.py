import sherpa_onnx
import numpy as np
from pathlib import Path


class SpeechToTextProvider:

    def __init__(self):
        model_dir = (
            Path(__file__).resolve().parent.parent
            / "models"
            / "parakeet-tdt-0.6b-v3-int8"
        )

        encoder = model_dir / "encoder.int8.onnx"
        decoder = model_dir / "decoder.int8.onnx"
        joiner = model_dir / "joiner.int8.onnx"
        tokens = model_dir / "tokens.txt"

        required_files = [encoder, decoder, joiner, tokens]

        for file in required_files:
            if not file.is_file():
                raise FileNotFoundError(
                    f"Required model file not found: {file}"
                )

        self.recognizer = sherpa_onnx.OfflineRecognizer.from_transducer(
            encoder=str(encoder),
            decoder=str(decoder),
            joiner=str(joiner),
            tokens=str(tokens),
            num_threads=4,
            sample_rate=16000,
            feature_dim=128,
            decoding_method="greedy_search",
            model_type="nemo_transducer"
        )

    def transcribe(self, audio_file: str) -> str:
        import soundfile as sf

        audio, sample_rate = sf.read(
            audio_file,
            dtype="float32",
            always_2d=False,
        )

        if audio.ndim > 1:
            audio = audio.mean(axis=1)

        audio = np.asarray(audio, dtype=np.float32)

        if sample_rate != 16000:
            raise ValueError(f"Expected 16000 Hz audio, received {sample_rate} Hz.")

        if len(audio) == 0:
            return ""

        stream = self.recognizer.create_stream()
        stream.accept_waveform(sample_rate, audio)

        self.recognizer.decode_stream(stream)

        return stream.result.text.strip()
