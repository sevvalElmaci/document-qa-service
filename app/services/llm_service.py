"""LLM Service - Ollama """
import logging
import requests
from app.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self, model: str | None = None, base_url: str | None = None):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.model = model or settings.OLLAMA_MODEL

    def chat(self, message: str) -> str:
        """
        Ollama LLM'e prompt gönderir ve yanıt döndürür.
        - Bu servis sadece LLM iletişiminden sorumludur.
        - Hata durumlarında exception fırlatır
        """
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": message,
            "stream": False
        }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=settings.OLLAMA_TIMEOUT
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "Cevap alınamadı")

        except requests.exceptions.RequestException as e:
            logger.error("Ollama LLM çağrısı başarısız", exc_info=True)
            raise RuntimeError("LLM servisi ile iletişim kurulamadı") from e
