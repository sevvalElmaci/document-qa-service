"""
FastAPI Ana Uygulama
"""

import logging
import traceback
from contextlib import asynccontextmanager

from fastapi import HTTPException, status
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer

from app.config import settings
from app.api.routes import router
from app.services.rag_service import RAGService

# Logging ayarları
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama başlangıç ve kapanış olayları"""
    logger.info("🚀 Uygulama başlatılıyor...")

    try:
        logger.info("🧠 Embedding modeli yükleniyor...")
        embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)

        logger.info("📚 RAG servisi oluşturuluyor...")
        rag_service = RAGService(
            embedding_model=embedding_model,
            top_k=settings.TOP_K_RESULTS
        )

        # Not: Index'i burada build etmiyoruz.
        # Çünkü senin akışın: upload -> build_index_for_text()
        app.state.rag_service = rag_service
        logger.info("✅ RAG servisi hazır!")
    except Exception:
        logger.error("RAG servisi başlatılamadı!")
        logger.error(traceback.format_exc())
        app.state.rag_service = None
        logger.warning(" Uygulama RAG olmadan çalışacak")

    yield
    logger.info(" Uygulama kapatılıyor...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Yerel LLM ile doküman soru-cevap servisi",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    lifespan=lifespan,
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(router, prefix=settings.API_PREFIX, tags=["QA"])


@app.get("/")
async def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": f"{settings.API_PREFIX}/docs",
    }


def get_rag_service(request: Request):
    """RAG service dependency injection"""
    rag_service = getattr(request.app.state, "rag_service", None)
    if rag_service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAG servisi hazır değil"
        )
    return rag_service
