# Drive-Thru Voice Assistant (VA)

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit)
![License](https://img.shields.io/badge/license-MIT-green)

An AI-powered, voice-first drive-thru ordering assistant designed for Quick Service Restaurants (QSR). Built using an open-source AI stack (Llama-3, Faster-Whisper, Piper TTS, Silero VAD, FastAPI).

## Features
- **Real-Time Voice Engine (Phase 3)**: High-performance WebSocket server supporting bi-directional streaming of raw PCM audio.
- **Barge-in Support**: Users can interrupt the AI mid-sentence. The system detects speech via VAD and instantly kills the TTS stream.
- **Silero VAD**: Advanced Voice Activity Detection to identify speech boundaries in milliseconds.
- **Voice-Interactive AI**: Real-time voice ordering using Faster-Whisper (STT) and Edge-TTS (Neural Voices).
- **Conversational Memory**: The agent remembers previous turns and maintains order context.
- **Deterministic Business Logic**: LLM tool-calling strictly validated against `order_details.json`.
- **Automatic Checkout**: Smart total calculation including tax, packaging, and order finalization.


## Setup & Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Configure your `LLM_API_KEY` and `LLM_MODEL` in the `.env` file.

## Enabling HTTPS (Required for Real-Time Microphone Access)

To use the real-time voice frontend, modern browsers require a secure HTTPS connection to grant microphone access.

1. **Generate SSL Certificates:**
   Run the following command in the root of the project to generate self-signed certificates:
   ```bash
   openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
   ```
2. **Start the secure server:**
   The backend automatically detects `key.pem` and `cert.pem` and will start in HTTPS mode.

## Running the Application

### 1. Start the AI Backend (Real-Time WebSockets)
This handles the real-time audio pipeline, VAD, and Barge-in:
```bash
python -m app.api.main
```
Navigate to `https://localhost:8000` in your browser. (Note: Accept the self-signed certificate warning to proceed).

### 2. Start the Voice Agent Dashboard (Legacy)
The classic Streamlit-based customer interface:
```bash
streamlit run frontend/voice_agent_app.py
```

### 3. Start the Kitchen Display System (KDS)
```bash
streamlit run frontend/kds_app.py
```

### 4. Start the Admin Dashboard
```bash
streamlit run frontend/admin_app.py
```

## Architecture Diagram

[![](https://mermaid.ink/img/pako:eNqVVO9P2zAQ_VcsI6YitZAmKU2zaVJHVg3WAmrCkLbug-tcWwsnjpxE0AH_-85J6Q_oNJFPffa753fvTn2kXMVAfTrXLFuQKJikBL_DQxLATKRAuJJKEy5ZnkNeX1YAr8lUlkBmQkr_gHPozGbNvNDqDvwDy-rw6Qts3Yu4WPh29tCs1My19fGV1hKkVPcrtRl-nK_Vps7Usaz3qM01QLq2tiNme6zrdt4jpiFe--J8SyrmTue_UrVYXk7rhCd0oFVaQBqTIVuCntCaYL6b818TOgYmW5FIgNzCFI9I41s0Gp5chEcT-tv3fRP6piQMsCQsNLBEioIELF9MFdNxThrfg7BJ-nEi0jeV-PoeY_3rc_KBXGm-AGyJFUKl2-4GfXxqwPLC8BpoLlT8DoqVeD2_DTsYITsQTKo5LsmIpWxumn1N_YeTc3ItMpC4gNsOfvSrboUErQwgjTAD4Avc1QK48bsyU41_K6QoWlkH3bpdiDwDjbVRtJ8-HBrvQ8kS1nJIA-F-XhSFyDNGtfmNisu0wOxE_pa_v88vZY4t5jkZqrngGH7ACrbdcTTGFyKlJBnDXOBUlrUyruSGNPp6eYO0EaRlJUAaF-HV5dEr5pYDXKpPrdbnpwldT5E0rs9GJ6u6J5x1zRz0KyZOs8bBiBiI2e9gjHIHY2Q7GNOpMV7UgtG4PojGNTY91CdhsDmhTfxfEjH1C11CkyagE2YgfTTcCcW0E9wQH3_GTN-Z5J6xJmPpT6WSlzKtyvmC-jMmc0RlFrMCcDNxCMn6VGM8oM9UmRbUb9tWJUL9R_pAfdtyjzue27WstutaXcfrNOmS-qe9457t9Nodz_NOnXbPfW7SP9Wz1rGHNbZr2Zbds5yu6z3_BWDqn_4?type=png)](https://mermaid.live/edit#pako:eNqVVO9P2zAQ_VcsI6YitZAmKU2zaVJHVg3WAmrCkLbug-tcWwsnjpxE0AH_-85J6Q_oNJFPffa753fvTn2kXMVAfTrXLFuQKJikBL_DQxLATKRAuJJKEy5ZnkNeX1YAr8lUlkBmQkr_gHPozGbNvNDqDvwDy-rw6Qts3Yu4WPh29tCs1My19fGV1hKkVPcrtRl-nK_Vps7Usaz3qM01QLq2tiNme6zrdt4jpiFe--J8SyrmTue_UrVYXk7rhCd0oFVaQBqTIVuCntCaYL6b818TOgYmW5FIgNzCFI9I41s0Gp5chEcT-tv3fRP6piQMsCQsNLBEioIELF9MFdNxThrfg7BJ-nEi0jeV-PoeY_3rc_KBXGm-AGyJFUKl2-4GfXxqwPLC8BpoLlT8DoqVeD2_DTsYITsQTKo5LsmIpWxumn1N_YeTc3ItMpC4gNsOfvSrboUErQwgjTAD4Avc1QK48bsyU41_K6QoWlkH3bpdiDwDjbVRtJ8-HBrvQ8kS1nJIA-F-XhSFyDNGtfmNisu0wOxE_pa_v88vZY4t5jkZqrngGH7ACrbdcTTGFyKlJBnDXOBUlrUyruSGNPp6eYO0EaRlJUAaF-HV5dEr5pYDXKpPrdbnpwldT5E0rs9GJ6u6J5x1zRz0KyZOs8bBiBiI2e9gjHIHY2Q7GNOpMV7UgtG4PojGNTY91CdhsDmhTfxfEjH1C11CkyagE2YgfTTcCcW0E9wQH3_GTN-Z5J6xJmPpT6WSlzKtyvmC-jMmc0RlFrMCcDNxCMn6VGM8oM9UmRbUb9tWJUL9R_pAfdtyjzue27WstutaXcfrNOmS-qe9457t9Nodz_NOnXbPfW7SP9Wz1rGHNbZr2Zbds5yu6z3_BWDqn_4)

## Running Tests
```bash
PYTHONPATH=. pytest tests/
```