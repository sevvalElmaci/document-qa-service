from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Dict
from pydantic import BaseModel
from typing import List, Optional

Mode = Literal["fast", "long"]


class SourceInfo(BaseModel):
    file: str
    chunk: str
    relevance: float


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None



class UploadResponse(BaseModel):
    doc_id: str
    mode: Mode
    chars: int
    chunks: int

class AskRequest(BaseModel):
    doc_id: str
    question: str = Field(min_length=3, max_length=500)
    top_k: Optional[int] = Field(default=None, ge=1, le=10)

class SourceItem(BaseModel):
    file: str
    chunk: str
    relevance: float

class AskResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceItem]
    confidence: str

class HealthResponse(BaseModel):
    status: str
    rag_ready: bool
    documents: int
    chunks: int
