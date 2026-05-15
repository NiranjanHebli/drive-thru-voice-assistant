import asyncio
import speech_recognition as sr
import io


class FasterWhisperSTT:
    def __init__(self, model_size="base"):
        self.model_size = model_size
        self.recognizer = sr.Recognizer()

    async def transcribe(self, audio_buffer: bytes) -> str:
        # Use asyncio to not block the main thread, though SR is sync
        loop = asyncio.get_event_loop()

        def _transcribe_sync():
            try:
                # Try to load as WAV file (for Streamlit mic recorder)
                try:
                    with sr.AudioFile(io.BytesIO(audio_buffer)) as source:
                        audio_data = self.recognizer.record(source)
                except Exception:
                    # If not a valid WAV, assume raw PCM 16-bit 16000Hz (for WebSockets)
                    audio_data = sr.AudioData(audio_buffer, 16000, 2)

                # Use Google's free Web API for immediate interactivity without heavy local models
                return self.recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                return ""
            except Exception as e:
                print(f"STT Error: {e}")
                return ""

        text = await loop.run_in_executor(None, _transcribe_sync)
        return text
