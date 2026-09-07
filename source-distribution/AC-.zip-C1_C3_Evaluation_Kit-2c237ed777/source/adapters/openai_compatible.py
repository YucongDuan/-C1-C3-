"""
OpenAI-compatible Chat Completions adapter (requests-based).
Works with any endpoint that accepts: {"model": ..., "messages": [...]} and returns choices[0].message.content.
"""
from typing import List, Dict
import os, requests

class OpenAICompatibleAdapter:
    def __init__(self, endpoint: str, api_key_env: str = "API_KEY", model: str = "", timeout_sec: int = 120, headers: dict | None = None):
        self.endpoint = endpoint
        self.api_key = os.getenv(api_key_env, "")
        self.model = model
        self.timeout_sec = timeout_sec
        self.headers = headers or {}
        if self.api_key:
            self.headers.setdefault("Authorization", f"Bearer {self.api_key}")
        self.headers.setdefault("Content-Type", "application/json")

    def chat(self, messages: List[Dict[str, str]]) -> str:
        payload = {"model": self.model, "messages": messages}
        resp = requests.post(self.endpoint, json=payload, headers=self.headers, timeout=self.timeout_sec)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
