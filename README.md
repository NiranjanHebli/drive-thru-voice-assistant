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

```mermaid
graph TD
    %% Subgraphs representing the layers
    subgraph Frontend_Layer ["Frontend Layer"]
        UI["Real-Time Web UI<br>(HTML/JS)"]
        Dashboard["Streamlit Dashboards<br>(KDS, Admin)"]
    end

    subgraph API_Orchestration ["API & Orchestration"]
        FastAPI["FastAPI (WebSocket)"]
        DM["Dialogue Manager"]
    end

    subgraph AI_Pipeline ["AI Pipeline"]
        VAD["Silero VAD (Speech<br>Detection)"]
        STT["Faster-Whisper (STT)"]
        LLM["Llama-3 (LLM)"]
        TTS["Piper TTS (Synthesis)"]
    end

    subgraph Business_Logic ["Business Logic & Data"]
        Registry["Tool Registry"]
        Menu["Menu Data (JSON)"]
    end

    %% Connections and Data Flow
    UI <-->|"WebSocket (PCM/JSON)"| FastAPI
    FastAPI <--> DM
    
    DM --> VAD
    DM --> STT
    DM --> LLM
    DM --> TTS
    
    LLM <--> Registry
    Registry <--> Menu
    Dashboard <--> Menu

    %% Styling Classes for Nodes
    classDef blueBox fill:#d0e3ff,stroke:#4a86e8,stroke-width:2px,color:#000
    classDef yellowBox fill:#fff2cc,stroke:#d6b656,stroke-width:2px,color:#000
    classDef greenBox fill:#d9ead3,stroke:#93c47d,stroke-width:2px,color:#000
    classDef redBox fill:#f4cccc,stroke:#e06666,stroke-width:2px,color:#000

    %% Applying Styles to Nodes
    class UI,Dashboard blueBox
    class FastAPI,DM yellowBox
    class VAD,STT,LLM,TTS greenBox
    class Registry,Menu redBox

    %% Removing Subgraph Backgrounds
    style Frontend_Layer fill:none,stroke:#999,stroke-width:1px,stroke-dasharray: 5 5
    style API_Orchestration fill:none,stroke:#999,stroke-width:1px,stroke-dasharray: 5 5
    style AI_Pipeline fill:none,stroke:#999,stroke-width:1px,stroke-dasharray: 5 5
    style Business_Logic fill:none,stroke:#999,stroke-width:1px,stroke-dasharray: 5 5
```

## Running Tests
```bash
PYTHONPATH=. pytest tests/
```