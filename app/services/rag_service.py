import uuid
import numpy as np
import faiss
from typing import List, Dict
from app.services.document_service import DocumentService
from app.services.llm_service import LLMService
from app.services.buddy_store import BUDDY_DB, DocIndex

class RAGService:
    def __init__(self, embedding_model, top_k=3):
        self.top_k = top_k
        self.embedding_model = embedding_model
        self.llm_service = LLMService()

        # - fast: daha küçük chunk + daha düşük top_k -> daha hızlı, daha ucuz, ama bağlam kaçırabilir
        # - long: daha büyük chunk + daha yüksek top_k -> daha doğru/bağlamlı, ama daha yavaş ve prompt daha uzun

    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        emb = self.embedding_model.encode(texts, show_progress_bar=False)
        return np.array(emb).astype("float32")

    def build_index_for_text(self, text: str, mode: str) -> str:
        # Mode config
        # fast/long seçimi retrieval kalitesi ve latency arasında kontrollü bir denge kurar.
        if mode == "fast":
            chunk_size, overlap, top_k = 400, 50, 3
        else:
            chunk_size, overlap, top_k = 600, 80, 5

        doc_service = DocumentService(chunk_size=chunk_size, chunk_overlap=overlap)
        chunks = doc_service.split_text(text)

        meta = [{"source": "user_upload", "text": c} for c in chunks]
        embeddings = self.create_embeddings(chunks)
        dim = embeddings.shape[1]

        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)

        doc_id = str(uuid.uuid4())
        BUDDY_DB[doc_id] = DocIndex(
            mode=mode, text=text, chunks=chunks, meta=meta, index=index
        )
        return doc_id

    def search_in_doc(self, doc_id: str, query: str, k: int) -> List[Dict]:
        doc = BUDDY_DB[doc_id]
        query_emb = self.create_embeddings([query])
        distances, indices = doc.index.search(query_emb, k)

        results = []
        for i, idx in enumerate(indices[0]):
            results.append({
                "chunk": doc.chunks[idx],
                "source": doc.meta[idx]["source"],
                "distance": float(distances[0][i]),
                "rank": i + 1,
            })
        return results

    def ask_in_doc(self, doc_id: str, question: str, top_k: int = None) -> Dict:
        doc = BUDDY_DB[doc_id]

        # top_k override yoksa mode'a göre default seçiyoruz.
        #  "fast" modunda prompt şişmez, "long" modunda daha geniş bağlam taranır
        k = top_k or (3 if doc.mode == "fast" else 5)

        search_results = self.search_in_doc(doc_id, question, k)

        context = "\n\n".join(
            [f"[Doc {i+1}]\n{r['chunk']}" for i, r in enumerate(search_results)]
        )

        prompt = f"""You are a helpful assistant.
Answer using ONLY the context.

Context:
{context}

Question: {question}

If the answer is not in the context, say: "I don't have enough information."
"""

        answer = self.llm_service.chat(prompt)

        # basit confidence heuristiği
        confidence = "high" if len(search_results) >= 3 else "medium"

        return {
            "question": question,
            "answer": answer,
            "sources": [{
                "file": "user_upload",
                "chunk": r["chunk"],
                "relevance": 1.0 / (1.0 + r["distance"])  #  normalize
            } for r in search_results],
            "confidence": confidence
        }
