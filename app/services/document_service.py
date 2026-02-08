from pathlib import Path
from typing import List

class SimpleTextSplitter:
    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[str]:
        chunks = []
        start = 0
        text_len = len(text)


        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap, chunk_size'dan küçük olmalı")

        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            #  start ilerlemek zorunda
            next_start = end - self.chunk_overlap
            if next_start <= start:
                break

            start = next_start

        return chunks


class DocumentService:
    def __init__(self, documents_path="data/documents", chunk_size=500, chunk_overlap=50):
        self.documents_path = Path(documents_path).resolve()
        self.text_splitter = SimpleTextSplitter(chunk_size, chunk_overlap)

    def split_text(self, text: str):
        return self.text_splitter.split_text(text)



    def read_text_file(self, file_path: str) -> str:
        # encoding list
        encodings = ["utf-8", "utf-8-sig", "cp1254", "cp1252", "latin-1"]

        last_err = None
        for enc in encodings:
            try:
                with open(file_path, "r", encoding=enc) as f:
                    return f.read()
            except Exception as e:
                last_err = e

        # bozuk karakterleri replace et
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Dosya okunamadı ({file_path}). Son hata: {last_err} / {e}")

    def read_document(self, file_path):
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")

        if file_path.suffix.lower() == ".txt":
            return self.read_text_file(str(file_path))

        raise ValueError(f"Desteklenmeyen dosya türü: {file_path.suffix}")

    def process_document(self, file_path):
        text = self.read_document(file_path)
        return self.text_splitter.split_text(text)

    def list_documents(self):
        if not self.documents_path.exists():
            return []
        return [str(p) for p in self.documents_path.glob("*.txt")]
