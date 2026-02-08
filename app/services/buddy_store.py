from dataclasses import dataclass
from typing import Dict, List
import faiss
import numpy as np

@dataclass
class DocIndex:
    mode: str
    text: str
    chunks: List[str]
    meta: List[dict]
    index: faiss.IndexFlatL2

BUDDY_DB: Dict[str, DocIndex] = {}
#Session Store

