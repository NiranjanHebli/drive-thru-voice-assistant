import asyncio
import edge_tts
import io


class PiperTTS:
    def __init__(self, voice="en-IN-PrabhatNeural"):
        self.voice = voice

    async def synthesize(self, text: str) -> bytes:
        # edge_tts is purely async and extremely fast
        communicate = edge_tts.Communicate(text, self.voice)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]

        return audio_data
