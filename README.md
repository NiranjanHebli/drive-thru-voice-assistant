#  Drive-Thru Ordering VA

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit)
![License](https://img.shields.io/badge/license-MIT-green)

An AI-powered, voice-first drive-thru ordering assistant designed for Quick Service Restaurants (QSR). Built using an open-source AI stack (Llama-3, Faster-Whisper, Piper TTS, FastAPI).

## Features
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

## Running the Application

Everything now runs through Streamlit for a unified, stable experience.

### 1. Start the Voice Agent
This is the main customer-facing interface:
```bash
streamlit run frontend/voice_agent_app.py
```

### 2. Start the Kitchen Display System (KDS)
To monitor incoming orders in real-time:
```bash
streamlit run frontend/kds_app.py
```

### 3. Start the Admin Dashboard
To monitor interactions and manage the menu:
```bash
streamlit run frontend/admin_app.py
```

## Running Tests
To verify the ordering logic and tool execution:
```bash
PYTHONPATH=. pytest tests/
```

## Architecture Diagram 

[![High Level Diagram](https://mermaid.ink/img/pako:eNqdVn9v4jgQ_SpWVrtqpUALgRbYaiUK7ZYrvVYNu0hXTsgkE_A12JHjtGXbfvcb20kIbXXSLX859pvx_HjzzLMTiBCcnrOUNFmRyXDGCf4-fyZDiBgH4qtNDGQQ0zSFlDwytSLTFVNAJvCkLDjQhwgnEsKBWCckYnHc-xR6zagZuamS4h56nzzPy9e1RxaqVa-ZPLmBiIXsfYqi6OsbX4s4g4qzRvf4KGz-rjO6XoCseIuiTnR4-LvelhKAV7x5nQ54wf_wZv2l2cIW_SxcArmbOUPJHqA2WcmMjCmWfk8f7M-cvy1e_wZZqsQaJKKL5c75BZXhI5WA51csIF-InwC9B0n6UtJNCQUevovilAb3uK8DOaep6t-Myq2BkLBzzdRH1BQWvkCAQo5IoBjKyUJ-26NJckATdpCazXqy2c3gWgYrwDOqhM5iyGgslhmQK8rpMndxQXkYI9tOqVxCjfFdD_3RRIg4ReP-iOglOXuCIEN_qQ0gDOdKzAMqlUuWoOYiikCmb8JIFFuzX7aSiNxuGB99dFc7zTAMxpf7_1k3Hy-mtoG-ojgYX8iQKrpz208a38Pmbm_m2JW5Y8RrV7AWckNMAMYYr9qv2P3hX_-prYQMQc5DUJTFaf2fVHDj4Qp4ZjAVs49C7I_mNyyBWM8zhnmdACe-yGQAeETKo72xCGhMvt_8ID7IB5C7JfvZHz5jjiwGKfSHCQH5BcEKxUJBoJjQrXrdmviTybOlE8gaykaalPUNmSBKGBXZtRmPr9BmHNM1rXmkc0pGHOmSBcoYPjBKHhCyazOZ-GijE5F6bZDas77BXLWFf1Sfcym4yrlvuRwzRX6McAw3bwbscqipf8kUspiTIWYU0w3xN5jh2lx7H6ZzHIF3vO-Ha8b1WOqenYUMWZOzFfffWVSiRCnupylbcqIlR3DgKtV5DbSiFMJcUahSI9xCDApdruoYjrBbHUU3nyq3nINSgXfMLH9dTbqtqu4i-kMX--5ik1zshYsVc03yW938WsltIDi31CFjsWSBPShyICe12jfygm2xPDsgF0AlzuTMeSnFzpqU2RYmqE-3kwGaTH1fw6e-BU59kiNu6aOlBxmsMn6vQRi9RW2LP8L5TAMaAjmPxaPdR5h2sg3MDgCE2gdmb1G4yFGGjBNJeRpIliiNwvpYFC5y1C2k2OA0f1sRg_WzGFzkGBuvZWk1qzJeo4gDGmvl0g9ALk_b2PV9J9ZZo27kY2ujPeZMsOD8ozBo1jUDWKh1boSU13jt4UOwVyc-fQAjb6a2hju7UIts1cktqExyGwnWIYu3RSpTK96DKlNMJ-rGS0maEU6zlFmS96PKc2tU3SmsL_EtJzc4zQt89cril3ejGmypmt4F-BeoRxr5uNrM8mTGLM85fwdetGjkWZs5OCm6TUPNTqn_TfkY0JoW5XRc_D_GQqeHwgeugzmtqf50nrWfmaMQjC9yD5chlRjtjL-iTUL5X0KsCzMpsuXK6UU0TvErS3TX8L1FzdtCUGj0DGdcOb1Gs902Tpzes_OE361m_bB13D469NqNdueo6zobp1fzvG692Wkfdbpe8_i4cdh9dZ1f5tpGveV5x81Gu9X02h2v22m9_gvAekl8?type=png)](https://mermaid.live/edit#pako:eNqdVn9v4jgQ_SpWVrtqpUALgRbYaiUK7ZYrvVYNu0hXTsgkE_A12JHjtGXbfvcb20kIbXXSLX859pvx_HjzzLMTiBCcnrOUNFmRyXDGCf4-fyZDiBgH4qtNDGQQ0zSFlDwytSLTFVNAJvCkLDjQhwgnEsKBWCckYnHc-xR6zagZuamS4h56nzzPy9e1RxaqVa-ZPLmBiIXsfYqi6OsbX4s4g4qzRvf4KGz-rjO6XoCseIuiTnR4-LvelhKAV7x5nQ54wf_wZv2l2cIW_SxcArmbOUPJHqA2WcmMjCmWfk8f7M-cvy1e_wZZqsQaJKKL5c75BZXhI5WA51csIF-InwC9B0n6UtJNCQUevovilAb3uK8DOaep6t-Myq2BkLBzzdRH1BQWvkCAQo5IoBjKyUJ-26NJckATdpCazXqy2c3gWgYrwDOqhM5iyGgslhmQK8rpMndxQXkYI9tOqVxCjfFdD_3RRIg4ReP-iOglOXuCIEN_qQ0gDOdKzAMqlUuWoOYiikCmb8JIFFuzX7aSiNxuGB99dFc7zTAMxpf7_1k3Hy-mtoG-ojgYX8iQKrpz208a38Pmbm_m2JW5Y8RrV7AWckNMAMYYr9qv2P3hX_-prYQMQc5DUJTFaf2fVHDj4Qp4ZjAVs49C7I_mNyyBWM8zhnmdACe-yGQAeETKo72xCGhMvt_8ID7IB5C7JfvZHz5jjiwGKfSHCQH5BcEKxUJBoJjQrXrdmviTybOlE8gaykaalPUNmSBKGBXZtRmPr9BmHNM1rXmkc0pGHOmSBcoYPjBKHhCyazOZ-GijE5F6bZDas77BXLWFf1Sfcym4yrlvuRwzRX6McAw3bwbscqipf8kUspiTIWYU0w3xN5jh2lx7H6ZzHIF3vO-Ha8b1WOqenYUMWZOzFfffWVSiRCnupylbcqIlR3DgKtV5DbSiFMJcUahSI9xCDApdruoYjrBbHUU3nyq3nINSgXfMLH9dTbqtqu4i-kMX--5ik1zshYsVc03yW938WsltIDi31CFjsWSBPShyICe12jfygm2xPDsgF0AlzuTMeSnFzpqU2RYmqE-3kwGaTH1fw6e-BU59kiNu6aOlBxmsMn6vQRi9RW2LP8L5TAMaAjmPxaPdR5h2sg3MDgCE2gdmb1G4yFGGjBNJeRpIliiNwvpYFC5y1C2k2OA0f1sRg_WzGFzkGBuvZWk1qzJeo4gDGmvl0g9ALk_b2PV9J9ZZo27kY2ujPeZMsOD8ozBo1jUDWKh1boSU13jt4UOwVyc-fQAjb6a2hju7UIts1cktqExyGwnWIYu3RSpTK96DKlNMJ-rGS0maEU6zlFmS96PKc2tU3SmsL_EtJzc4zQt89cril3ejGmypmt4F-BeoRxr5uNrM8mTGLM85fwdetGjkWZs5OCm6TUPNTqn_TfkY0JoW5XRc_D_GQqeHwgeugzmtqf50nrWfmaMQjC9yD5chlRjtjL-iTUL5X0KsCzMpsuXK6UU0TvErS3TX8L1FzdtCUGj0DGdcOb1Gs902Tpzes_OE361m_bB13D469NqNdueo6zobp1fzvG692Wkfdbpe8_i4cdh9dZ1f5tpGveV5x81Gu9X02h2v22m9_gvAekl8)