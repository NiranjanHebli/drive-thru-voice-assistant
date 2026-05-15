from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from app.ai_pipeline.stt_whisper import FasterWhisperSTT
from app.ai_pipeline.tts_piper import PiperTTS
from app.ai_pipeline.vad_silero import SileroVAD
from app.core.orchestrator import DialogueManager
import json
import os

app = FastAPI(title="Drive-Thru Voice Agent API")


@app.get("/")
async def get_frontend():
    html_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "frontend", "realtime_agent.html"
    )
    return FileResponse(html_path)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for sessions (to be replaced by Valkey)
sessions = {}


@app.websocket("/ws/drive-thru/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()

    if session_id not in sessions:
        sessions[session_id] = {"cart": [], "chat_history": []}

    session_data = sessions[session_id]

    try:
        vad = SileroVAD()
        stt = FasterWhisperSTT()
        tts = PiperTTS()
        dm = DialogueManager()
    except Exception as e:
        print(f"Error initializing models for session {session_id}: {e}")
        await websocket.close(code=1011)
        return

    audio_buffer = bytearray()
    is_speaking = False
    silence_counter = 0
    SILENCE_THRESHOLD = 15  # Approx 0.5s of silence (if chunks are small)

    # Task reference for currently playing TTS, so we can cancel it on barge-in
    current_tts_task = None

    try:
        while True:
            data = await websocket.receive_bytes()

            # Check VAD
            speech_detected = vad.is_speech(data)

            if speech_detected:
                if current_tts_task and not current_tts_task.done():
                    # Barge-in detected! Cancel the ongoing TTS
                    print("Barge-in detected! Cancelling TTS.")
                    current_tts_task.cancel()
                    current_tts_task = None
                    await websocket.send_json({"event": "barge_in"})

                is_speaking = True
                silence_counter = 0
                audio_buffer.extend(data)
            elif is_speaking:
                silence_counter += 1
                audio_buffer.extend(data)

                # If silence duration exceeds threshold, process the utterance
                if silence_counter > SILENCE_THRESHOLD:
                    is_speaking = False

                    # Transcribe
                    await websocket.send_json({"event": "stt_start"})
                    user_text = await stt.transcribe(bytes(audio_buffer))
                    audio_buffer.clear()

                    if not user_text or len(user_text.strip()) < 2:
                        continue

                    session_data["chat_history"].append(
                        {"role": "user", "content": user_text}
                    )
                    await websocket.send_json(
                        {"event": "transcription", "text": user_text}
                    )

                    # Process with Orchestrator
                    await websocket.send_json({"event": "llm_start"})
                    ai_response = await dm.process_turn(
                        session_id,
                        user_text,
                        session_data["cart"],
                        session_data["chat_history"],
                    )

                    session_data["chat_history"].append(
                        {"role": "assistant", "content": ai_response}
                    )
                    await websocket.send_json(
                        {
                            "event": "llm_response",
                            "text": ai_response,
                            "cart": session_data["cart"],
                        }
                    )

                    # Stream TTS back
                    async def stream_tts(text):
                        try:
                            async for chunk in tts.synthesize_stream(text):
                                await websocket.send_bytes(chunk)
                            await websocket.send_json({"event": "tts_done"})
                        except asyncio.CancelledError:
                            print("TTS stream cancelled.")
                            raise

                    current_tts_task = asyncio.create_task(stream_tts(ai_response))

    except WebSocketDisconnect:
        print(f"Client {session_id} disconnected")
        if session_id in sessions:
            del sessions[session_id]


if __name__ == "__main__":
    import uvicorn
    import os

    # Run with HTTPS if certificates exist
    key_path = os.path.join(os.path.dirname(__file__), "..", "..", "key.pem")
    cert_path = os.path.join(os.path.dirname(__file__), "..", "..", "cert.pem")

    if os.path.exists(key_path) and os.path.exists(cert_path):
        print("Starting secure server (HTTPS)...")
        uvicorn.run(
            app, host="0.0.0.0", port=8000, ssl_keyfile=key_path, ssl_certfile=cert_path
        )
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)
