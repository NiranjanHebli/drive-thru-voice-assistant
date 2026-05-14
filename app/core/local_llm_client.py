import httpx
import os
from dotenv import load_dotenv

load_dotenv()


class LocalLLMClient:
    def __init__(self):
        self.endpoint_url = os.getenv(
            "LLM_API_URL", "http://localhost:8000/v1/chat/completions"
        )
        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.model = os.getenv("LLM_MODEL", "llama3-8b-instruct")
        self.client = httpx.AsyncClient()

    async def generate(self, messages, tools=None):
        """Sends the conversation array to the LLM and returns the response."""
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,  # Low temperature for deterministic drive-thru ordering
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            response = await self.client.post(
                self.endpoint_url, json=payload, headers=headers, timeout=30.0
            )
            if response.status_code != 200:
                print(f"ERROR: LLM API returned status {response.status_code}")
                print(f"Details: {response.text}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"LLM API HTTP Error: {e}")
            print(f"Response Body: {e.response.text}")
            return None
        except httpx.RequestError as e:
            print(f"LLM API Connection Error: {e}")
            return None
