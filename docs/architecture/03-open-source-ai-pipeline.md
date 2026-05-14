# Architectural Decision Record: Open-Source AI Cascade

## Context
The system requires real-time, sub-second conversational latency. To maintain data privacy and eliminate recurring cloud API costs, we cannot use proprietary native-audio models.

## Decision
We implemented a self-hosted "Cascade Pipeline" orchestrated by FastAPI, utilizing local VRAM on dedicated GPU hardware.

## Technology Stack
 **VAD (Silero):** Detects voice activity in milliseconds. Acts as the trigger mechanism.
 **STT (Faster-Whisper):** Transcribes audio to text locally.
 **LLM (Llama 3 8B Instruct via vLLM):** Handles reasoning, conversation, and JSON tool calling.
 **TTS (Piper):** Generates low-latency voice responses.
 **State Management (Valkey):** Open-source, OSI-compliant alternative to Redis for caching cart state.

## Barge-in Architecture (Handling Interruptions)
Because we use a cascade of individual models, the system does not natively "know" when to stop talking if interrupted. We rely on the `app/core/orchestrator.py`. 
When Piper TTS is speaking to the customer, Silero VAD continues to listen. If VAD detects human speech for more than 300ms, the Orchestrator instantly kills the TTS audio stream and clears the Whisper buffer, allowing the user to seamlessly change their order mid-sentence.