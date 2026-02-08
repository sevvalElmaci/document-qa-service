#!/usr/bin/env python3
"""
Uygulamayı başlatan script
"""

import uvicorn
from app.config import settings


def normalize_prefix(prefix: str) -> str:
    """API prefix'i güvenli hale getirir"""
    if not prefix:
        return ""
    if not prefix.startswith("/"):
        prefix = "/" + prefix
    return prefix.rstrip("/")


def main():
    """Uygulamayı başlatır"""

    prefix = normalize_prefix(settings.API_PREFIX)

    # Tarayıcıdan açılacak adres her zaman localhost
    base_url = f"http://localhost:{settings.API_PORT}"

    print(f"""
╔══════════════════════════════════════════════════════╗
║  {settings.APP_NAME} v{settings.APP_VERSION}
╚══════════════════════════════════════════════════════╝

🚀 Servis başlatılıyor...
📍 Bind Host: {settings.API_HOST}:{settings.API_PORT}
🌍 Local URL: {base_url}
🤖 LLM Model: {settings.OLLAMA_MODEL}
📚 Vektör DB: {settings.VECTOR_DB_TYPE.upper()}

📖 API Dokümantasyonu:
   - Swagger UI: {base_url}{prefix}/docs
   - ReDoc:      {base_url}{prefix}/redoc

⚡ Hazır! CTRL+C ile durdurun.
""")

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning",
    )


if __name__ == "__main__":
    main()
