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
                # Convert raw bytes to AudioData for SpeechRecognition
                # Since streamlit-mic-recorder format="wav", it's a valid wav file buffer
                with sr.AudioFile(io.BytesIO(audio_buffer)) as source:
                    audio_data = self.recognizer.record(source)
                # Use Google's free Web API for immediate interactivity without heavy local models
                return self.recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                return "I couldn't understand that."
            except Exception as e:
                print(f"STT Error: {e}")
                return "There was an error with transcription."

        text = await loop.run_in_executor(None, _transcribe_sync)
        return text
