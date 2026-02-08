"""Document Service - Doküman okuma ve işleme (LangChain'siz)"""
import os
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

        while start < text_len:
            end = start + self.chunk_size

            if end > text_len:
                end = text_len

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start = end - self.chunk_overlap

            if start >= text_len:
                break

        return chunks


class DocumentService:

    def __init__(self, documents_path="data/documents", chunk_size=500, chunk_overlap=50):
        self.documents_path = Path(documents_path)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = SimpleTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def read_text_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Dosya okunamadı: {e}")

    def read_document(self, file_path):
        """Doküman okur (txt)"""
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")

        if file_path.suffix.lower() == '.txt':
            return self.read_text_file(str(file_path))
        else:
            raise ValueError(f"Desteklenmeyen dosya türü: {file_path.suffix}")

    def split_text(self, text):
        """Metni chunk'lara böler"""
        chunks = self.text_splitter.split_text(text)
        return chunks

    def process_document(self, file_path):
        """Dokümanı okur ve chunk'lara böler"""
        text = self.read_document(file_path)
        chunks = self.split_text(text)
        return chunks

    def list_documents(self):
        """documents klasöründeki dosyaları listeler"""
        if not self.documents_path.exists():
            return []

        files = []
        for file in self.documents_path.glob('*'):
            if file.suffix.lower() in ['.txt', '.pdf']:
                files.append(str(file))
        return files


# Test
if __name__ == "__main__":
    print("📄 Document Service Testi\n")

    doc_service = DocumentService()

    print("📂 Mevcut dokümanlar:")
    docs = doc_service.list_documents()
    for doc in docs:
        print(f"  - {doc}")

    if docs:
        print(f"\n📖 İlk doküman işleniyor: {docs[0]}")
        chunks = doc_service.process_document(docs[0])

        print(f"\n✂️ Chunk sayısı: {len(chunks)}")
        print(f"\n📝 İlk chunk:")
        print(chunks[0])

        if len(chunks) > 1:
            print(f"\n📝 İkinci chunk:")
            print(chunks[1])
    else:
        print("\n⚠️ data/documents/ klasöründe doküman yok!")
