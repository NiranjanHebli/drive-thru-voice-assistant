class Orchestrator:
    """
    Manages the local AI cascade pipeline state and handles barge-in (interruptions).
    """
    def __init__(self):
        self.is_speaking = False
        self.whisper_buffer = []

    async def handle_audio_stream(self, audio_chunk):
        """
        Receives audio from stream.py, runs VAD, and triggers STT/LLM if needed.
        """
        pass

    def interrupt(self):
        """
        Kills current TTS output and clears Whisper buffer when barge-in is detected.
        """
        self.is_speaking = False
        self.whisper_buffer = []
        print("Interruption detected: Pipeline reset.")
