import requests
import os
import logging
from app.utils.retry import retry

logger = logging.getLogger(__name__)

class OllamaService:
    def __init__(self):
        self.api_url = f"http://{os.getenv('OLLAMA_HOST')}:11434"
        self.embed_url = f"http://{os.getenv('OLLAMA_HOST')}:{os.getenv('EMBEDDER_PORT')}"

    @retry(max_retries=5, delay=5)
    async def initialize(self):
        try:
            response = requests.post(f"{self.api_url}/api/pull", json={"name": "mistral:7b"})
            response.raise_for_status()
            logger.info("Initialized Ollama with mistral:7b model")
        except Exception as e:
            logger.error(f"Ollama initialization failed: {str(e)}")
            raise

    @retry(max_retries=5, delay=5)
    async def get_embedding(self, text: str):
        try:
            response = requests.post(f"{self.embed_url}/embed", json={"text": text}, timeout=10)
            response.raise_for_status()
            return response.json()["embedding"]
        except Exception as e:
            logger.error(f"Failed to get embedding: {str(e)}")
            raise

    @retry(max_retries=5, delay=5)
    async def test_generate(self):
        try:
            response = requests.post(
                f"{self.api_url}/api/generate",
                json={"model": "mistral:7b", "prompt": "Test prompt", "stream": False}
            )
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to generate with Ollama: {str(e)}")
            raise