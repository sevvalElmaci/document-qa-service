from fastapi import Request, HTTPException, status
from app.services.rag_service import RAGService

def get_rag_service(request: Request) -> RAGService:
    rag_service = getattr(request.app.state, "rag_service", None)

    if rag_service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAG servisi henüz hazır değil"
        )

    return rag_service
