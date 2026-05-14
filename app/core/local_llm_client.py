import httpx


class LocalLLMClient:
    def __init__(self, endpoint_url="http://localhost:8000/v1/chat/completions"):
        self.endpoint_url = endpoint_url
        self.client = httpx.AsyncClient()

    async def generate(self, messages, tools=None):
        """Sends the conversation array to the local LLM and returns the response."""
        payload = {
            "model": "llama3-8b-instruct",
            "messages": messages,
            "temperature": 0.2,  # Low temperature for deterministic drive-thru ordering
        }

        if tools:
            payload["tools"] = tools

        try:
            response = await self.client.post(
                self.endpoint_url, json=payload, timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            print(f"LLM API Connection Error: {e}")
            return None
        finally:
            await self.client.aclose()
