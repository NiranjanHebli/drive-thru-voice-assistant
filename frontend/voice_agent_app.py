import streamlit as st
from streamlit_mic_recorder import mic_recorder
import asyncio
import sys
import os

# Add root directory to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import importlib
from app.ai_pipeline import stt_whisper, tts_piper
from app.core import orchestrator

importlib.reload(stt_whisper)
importlib.reload(tts_piper)
importlib.reload(orchestrator)

from app.ai_pipeline.stt_whisper import FasterWhisperSTT
from app.ai_pipeline.tts_piper import PiperTTS
from app.core.orchestrator import DialogueManager

st.set_page_config(
    page_title="Drive-Thru Voice Agent", page_icon="🍔", layout="centered"
)

st.title("🍔 Drive-Thru Voice Agent")
st.markdown("Click the microphone to talk to the AI Drive-Thru Agent.")

# Initialize state
if "cart" not in st.session_state:
    st.session_state.cart = []
if "session_id" not in st.session_state:
    import uuid

    st.session_state.session_id = str(uuid.uuid4())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def process_voice_turn(audio_bytes):
    """Processes the recorded audio chunk through STT -> LLM -> TTS"""
    stt = FasterWhisperSTT()
    tts = PiperTTS()
    dm = DialogueManager()

    async def _run_pipeline():
        # 1. STT (Stub will return "I would like a burger" for now)
        user_text = await stt.transcribe(audio_bytes)
        st.session_state.chat_history.append(
            {"role": "user", "content": f"🗣️ [Transcribed]: {user_text}"}
        )

        # 2. LLM Orchestrator
        ai_response = await dm.process_turn(
            st.session_state.session_id,
            user_text,
            st.session_state.cart,
            st.session_state.chat_history,
        )
        st.session_state.chat_history.append(
            {"role": "assistant", "content": ai_response}
        )

        # 3. TTS Synthesis (using gTTS)
        audio_out = await tts.synthesize(ai_response)
        st.session_state.last_audio = audio_out

        return ai_response

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(_run_pipeline())


# --- UI Layout ---

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎙️ Record your order")
    audio = mic_recorder(
        start_prompt="🔴 Start Recording",
        stop_prompt="⏹️ Stop Recording",
        just_once=False,
        use_container_width=True,
        format="wav",
    )

    if audio is not None:
        with st.spinner("Analyzing audio..."):
            process_voice_turn(audio["bytes"])

    st.divider()
    st.subheader("💬 Conversation Log")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Autoplay the TTS response
    if "last_audio" in st.session_state and st.session_state.last_audio:
        st.audio(st.session_state.last_audio, format="audio/mp3", autoplay=True)
        # Clear it so it doesn't replay on random re-renders
        st.session_state.last_audio = None

with col2:
    st.subheader("🛒 Cart")
    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        for item in st.session_state.cart:
            st.write(f"- {item['item_name']} (₹{item['price']})")
        total = sum(item["price"] for item in st.session_state.cart)
        st.markdown("---")
        st.write(f"**Total: ₹{total}**")
