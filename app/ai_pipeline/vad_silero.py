import torch
import numpy as np


class SileroVAD:
    def __init__(self, threshold=0.5, sampling_rate=16000):
        self.threshold = threshold
        self.sampling_rate = sampling_rate
        # Load the Silero VAD model from Torch Hub
        self.model, utils = torch.hub.load(
            repo_or_dir="snakers4/silero-vad",
            model="silero_vad",
            force_reload=False,
            trust_repo=True,
        )
        (
            self.get_speech_timestamps,
            self.save_audio,
            self.read_audio,
            self.VADIterator,
            self.collect_chunks,
        ) = utils

        self.vad_iterator = self.VADIterator(self.model)

    def is_speech(self, audio_chunk_bytes: bytes) -> bool:
        """
        Check if the given PCM audio chunk contains speech.
        Silero VAD requires chunks of exactly 512 samples (1024 bytes) at 16000Hz.
        """
        # Convert bytes to numpy int16 array, then to float32 tensor
        audio_int16 = np.frombuffer(audio_chunk_bytes, dtype=np.int16)

        # If the chunk is not 512 samples, pad it or truncate it (simplified for real-time WebSocket streams
        # where clients ideally send 1024-byte chunks or we just take the first 512 samples if larger).
        # A more robust implementation would maintain an internal byte buffer.

        if len(audio_int16) < 512:
            pad_width = 512 - len(audio_int16)
            audio_int16 = np.pad(audio_int16, (0, pad_width), mode="constant")
        elif len(audio_int16) > 512:
            audio_int16 = audio_int16[:512]

        audio_float32 = audio_int16.astype(np.float32) / 32768.0
        audio_tensor = torch.from_numpy(audio_float32)

        # Determine speech probability
        with torch.no_grad():
            speech_prob = self.model(audio_tensor, self.sampling_rate).item()

        return speech_prob > self.threshold

    def reset_state(self):
        """Reset the internal state of the VAD model."""
        self.vad_iterator.reset_states()
