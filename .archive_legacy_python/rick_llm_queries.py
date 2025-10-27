#!/usr/bin/env python3
"""RICK LLM Integration - Ollama Wrapper"""

import requests
import json
import logging
from typing import Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import time

OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_TIMEOUT = 30

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class OllamaResponse:
    """Ollama API response wrapper"""
    success: bool
    content: str
    error: Optional[str] = None
    model: str = OLLAMA_MODEL
    timestamp: str = ""
    response_time: float = 0.0

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

class RickLLMClient:
    """Local Ollama LLM client"""

    def __init__(self, host: str = OLLAMA_HOST, model: str = OLLAMA_MODEL):
        self.host = host
        self.model = model
        self.is_available = self._check_availability()

    def _check_availability(self) -> bool:
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = [m.get("name", "") for m in data.get("models", [])]
                model_available = any(self.model in m for m in models)
                if model_available:
                    logger.info(f"✅ Ollama available with {self.model}")
                    return True
            return False
        except:
            return False

    def query(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> OllamaResponse:
        if not self.is_available:
            return OllamaResponse(success=False, content="", error="Ollama service not available")

        enriched_prompt = self._enrich_prompt(prompt, context)

        try:
            start_time = time.time()
            response = requests.post(
                f"{self.host}/api/generate",
                json={"model": self.model, "prompt": enriched_prompt, "stream": False},
                timeout=OLLAMA_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            
            return OllamaResponse(
                success=True,
                content=data.get("response", "").strip(),
                model=self.model,
                response_time=time.time() - start_time
            )
        except Exception as e:
            return OllamaResponse(success=False, content="", error=str(e))

    def health_check(self) -> Dict[str, Any]:
        health = {"ollama_connected": self.is_available, "model": self.model, "host": self.host}
        if self.is_available:
            try:
                response = requests.get(f"{self.host}/api/show", json={"name": self.model}, timeout=5)
                health["model_loaded"] = response.status_code == 200
            except:
                health["model_loaded"] = False
        return health

    def _enrich_prompt(self, prompt: str, context: Optional[Dict] = None) -> str:
        system_context = "You are Rick, an expert AI trading assistant. Keep responses concise and actionable.\n"
        if context:
            return system_context + "\nContext:\n" + json.dumps(context, indent=2, default=str) + "\n\nUser query:\n" + prompt
        return system_context + prompt

_rick_client = None

def get_rick_client() -> RickLLMClient:
    global _rick_client
    if _rick_client is None:
        _rick_client = RickLLMClient()
    return _rick_client

if __name__ == "__main__":
    rick = get_rick_client()
    print(f"Ollama Health: {rick.health_check()}")
