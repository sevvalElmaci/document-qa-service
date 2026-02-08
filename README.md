# 🤖 Document QA Service (Local RAG)

FastAPI + FAISS + SentenceTransformer + Ollama ile çalışan yerel doküman soru-cevap servisi.

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Gereksinimler](#-gereksinimler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [API Dokümantasyonu](#-api-dokümantasyonu)
- [Proje Yapısı](#-proje-yapısı)
- [Yapılandırma](#-yapılandırma)

## ✨ Özellikler

- **Yerel LLM Desteği**: Ollama kullanarak tamamen yerel çalışır, internet gerektirmez
- **RAG (Retrieval Augmented Generation)**: Dokümanlarınızı analiz eder ve bağlamsal cevaplar üretir
- **İki Mod**: 
  - **Fast Mode**: Küçük dokümanlar için hızlı işlem (max 3200 karakter)
  - **Long Mode**: Büyük dokümanlar için kapsamlı analiz (max 50000 karakter)
- **FAISS Vektör Arama**: Hızlı ve verimli semantik arama
- **Streamlit Web Arayüzü**: Kullanıcı dostu interaktif arayüz
- **RESTful API**: FastAPI ile güçlü ve hızlı API

## 🔧 Gereksinimler

### Sistem Gereksinimleri
- Python 3.9 veya üzeri
- Node.js 16+ (docx oluşturma için, opsiyonel)
- En az 4GB RAM
- 2GB boş disk alanı

### Ollama Kurulumu
Bu proje Ollama kullandığı için önce Ollama'yı kurmanız gerekiyor:

1. [Ollama.ai](https://ollama.ai) adresinden Ollama'yı indirin ve kurun
2. Terminalde şu komutu çalıştırarak modeli indirin:
```bash
ollama pull llama3
```

3. Ollama'nın çalıştığını kontrol edin:
```bash
ollama list
```

## 🚀 Kurulum

### 1. Projeyi İndirin
```bash
unzip document-qa-service.zip
cd document-qa-service
```

### 2. Sanal Ortam Oluşturun
**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Gerekli paketler:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Veri validasyonu
- `sentence-transformers` - Embedding model
- `faiss-cpu` - Vektör arama
- `requests` - HTTP istekleri
- `streamlit` - Web arayüzü
- `python-multipart` - Dosya upload
- `Pillow` - Görsel işleme

### 4. Proje Yapısını Oluşturun (İlk Kurulum)
Eğer klasör yapısı eksikse:
```bash
python setup_project.py
```

## 💻 Kullanım

### Backend API'yi Başlatma

```bash
python run.py
```

Servis başladığında şu bilgileri göreceksiniz:
```
╔══════════════════════════════════════════════════════╗
║  Document QA Service v1.0.0
╚══════════════════════════════════════════════════════╝

🚀 Servis başlatılıyor...
📍 Bind Host: 0.0.0.0:8000
🌍 Local URL: http://localhost:8000
🤖 LLM Model: llama3
📚 Vektör DB: FAISS

📖 API Dokümantasyonu:
   - Swagger UI: http://localhost:8000/api/v1/docs
   - ReDoc:      http://localhost:8000/api/v1/redoc
```

### Frontend Arayüzü (Streamlit)

Yeni bir terminal açın ve:
```bash
streamlit run frontend/app.py
```

Tarayıcınızda otomatik olarak `http://localhost:8501` açılacaktır.

## 📖 API Dokümantasyonu

### Endpoints

#### 1. Doküman Yükleme
**POST** `/api/v1/upload`

Bir TXT dosyası yükler ve index oluşturur.

**Parametreler:**
- `mode` (query): `"fast"` veya `"long"` (default: `"fast"`)
- `file` (form): TXT dosyası

**Örnek:**
```bash
curl -X POST "http://localhost:8000/api/v1/upload?mode=fast" \
  -F "file=@mydocument.txt"
```

**Yanıt:**
```json
{
  "doc_id": "a1b2c3d4-5678-90ef-ghij-klmnopqrstuv",
  "mode": "fast",
  "chars": 1542,
  "chunks": 4
}
```

#### 2. Soru Sorma
**POST** `/api/v1/ask`

Yüklenen dokümana soru sorar.

**İstek Body:**
```json
{
  "doc_id": "a1b2c3d4-5678-90ef-ghij-klmnopqrstuv",
  "question": "Git version control nedir?",
  "top_k": 3
}
```

**Yanıt:**
```json
{
  "question": "Git version control nedir?",
  "answer": "Git, yazılım projelerinde kod değişikliklerini takip eden...",
  "sources": [
    {
      "file": "user_upload",
      "chunk": "Git bir versiyon kontrol sistemidir...",
      "relevance": 0.89
    }
  ],
  "confidence": "high"
}
```

#### 3. Sağlık Kontrolü
**GET** `/`

Servisin durumunu kontrol eder.

**Yanıt:**
```json
{
  "service": "Document QA Service",
  "version": "1.0.0",
  "status": "running",
  "docs": "/api/v1/docs"
}
```

## 📁 Proje Yapısı

```
document-qa-service/
├── app/
│   ├── __init__.py           # Paket başlatıcı
│   ├── main.py               # FastAPI uygulaması
│   ├── config.py             # Yapılandırma ayarları
│   ├── deps.py               # Dependency injection
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py         # API endpoint'leri
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py        # Pydantic modelleri
│   ├── services/
│   │   ├── __init__.py
│   │   ├── rag_service.py    # RAG servisi
│   │   ├── llm_service.py    # Ollama LLM servisi
│   │   ├── document_service.py  # Doküman işleme
│   │   └── buddy_store.py    # In-memory veri store
├── frontend/
│   ├── app.py                # Streamlit arayüzü
│   └── assets/
│       └── company_logo.jpg  # Logo (opsiyonel)
├── data/
│   ├── documents/            # Dokümanlar (opsiyonel)
│   └── vectordb/             # Vektör DB (opsiyonel)
├── run.py                    # Uygulama başlatıcı
├── setup_project.py          # Klasör yapısı oluşturucu
├── requirements.txt          # Python bağımlılıkları
└── README.md                 # Bu dosya
```

## ⚙️ Yapılandırma

### Ortam Değişkenleri


```env
# Uygulama
APP_NAME=Document QA Service
APP_VERSION=1.0.0
DEBUG=false

# API
API_HOST=0.0.0.0
API_PORT=8000
API_PREFIX=/api/v1

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
OLLAMA_TIMEOUT=120

# Embedding
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# RAG
TOP_K_RESULTS=3
MIN_RELEVANCE_SCORE=0.5

# Doküman İşleme
CHUNK_SIZE=500
CHUNK_OVERLAP=50
MAX_FILE_SIZE_MB=10
```

### Mod Ayarları

**Fast Mode** (Hızlı - Kısa Dokümanlar):
- Max karakter: 3200
- Chunk boyutu: 400
- Chunk örtüşme: 50
- Top-K: 3

**Long Mode** (Kapsamlı - Uzun Dokümanlar):
- Max karakter: 50000
- Chunk boyutu: 600
- Chunk örtüşme: 80
- Top-K: 5

## 🔍 Kullanım Senaryoları

### Senaryo 1: Web Arayüzü ile Kullanım

1. Backend'i başlatın: `python run.py`
2. Frontend'i başlatın: `streamlit run frontend/app.py`
3. Tarayıcıda `http://localhost:8501` adresine gidin
4. Bir TXT dosyası yükleyin
5. Sorularınızı sorun!

### Senaryo 2: API ile Kullanım

```python
import requests

# 1. Doküman yükle
with open("document.txt", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/upload?mode=fast",
        files={"file": f}
    )
    doc_id = response.json()["doc_id"]

# 2. Soru sor
response = requests.post(
    "http://localhost:8000/api/v1/ask",
    json={
        "doc_id": doc_id,
        "question": "Bu doküman ne hakkında?",
        "top_k": 3
    }
)
print(response.json()["answer"])
```
