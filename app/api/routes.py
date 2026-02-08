from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from app.models.schemas import UploadResponse, AskRequest, AskResponse
from app.services.buddy_store import BUDDY_DB
from app.deps import get_rag_service

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_txt(
    mode: str = "fast",
    file: UploadFile = File(...),
    rag_service=Depends(get_rag_service),
):
    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported.")

    raw = await file.read()
    try:
        text = raw.decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded.")

    text = text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="File is empty.")

    if mode not in ["fast", "long"]:
        raise HTTPException(status_code=422, detail="mode must be 'fast' or 'long'.")

    if mode == "fast" and len(text) > 3200:
        raise HTTPException(status_code=422, detail="FAST mode max 3200 characters.")
    if mode == "long" and len(text) > 50000:
        raise HTTPException(status_code=422, detail="LONG mode max 50000 characters.")

    try:
        doc_id = rag_service.build_index_for_text(text=text, mode=mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    doc = BUDDY_DB[doc_id]

    return UploadResponse(
        doc_id=doc_id,
        mode=mode,
        chars=len(text),
        chunks=len(doc.chunks),
    )


@router.post("/ask", response_model=AskResponse)
async def ask(
    req: AskRequest,
    rag_service=Depends(get_rag_service),
):
    if req.doc_id not in BUDDY_DB:
        raise HTTPException(status_code=404, detail="doc_id not found. Upload a txt first.")

    result = rag_service.ask_in_doc(
        doc_id=req.doc_id,
        question=req.question,
        top_k=req.top_k
    )
    return result
