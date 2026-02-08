# Doküman Soru-Cevap Servisi - Proje Yapısı

## Önerilen Klasör Yapısı

```
document-qa-service/
│
├── app/                          # Ana uygulama kodu
│   ├── __init__.py
│   ├── main.py                   # FastAPI uygulaması (entry point)
│   ├── config.py                 # Konfigürasyon ayarları
│   │
│   ├── api/                      # API endpoints
│   │   ├── __init__.py
│   │   ├── routes.py             # /health, /ask endpoint'leri
│   │   └── models.py             # Pydantic request/response modelleri
│   │
│   ├── services/                 # İş mantığı katmanı
│   │   ├── __init__.py
│   │   ├── llm_service.py        # LLM ile iletişim
│   │   ├── document_service.py   # Doküman işleme
│   │   └── rag_service.py        # RAG mantığı (vektör arama + LLM)
│   │
│   └── utils/                    # Yardımcı fonksiyonlar
│       ├── __init__.py
│       ├── text_splitter.py      # Doküman parçalama
│       └── embeddings.py         # Embedding oluşturma
│
├── data/                         # Dokümanlar ve vektör DB
│   ├── documents/                # PDF, txt, md dosyaları
│   │   └── sample.txt
│   └── vectordb/                 # FAISS veya Chroma DB
│
├── tests/                        # Birim testler
│   ├── __init__.py
│   ├── test_api.py               # API endpoint testleri
│   ├── test_llm_service.py       # LLM servis testleri
│   └── test_document_service.py  # Doküman işleme testleri
│
├── frontend/                     # (Opsiyonel) Basit web arayüzü
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .gitignore                    # Git ignore dosyası
├── requirements.txt              # Python bağımlılıkları
├── README.md                     # Proje dökümantasyonu
└── run.py                        # Uygulamayı başlatma scripti
```

## Modüller ve Sorumlulukları

### 1. API Katmanı (`app/api/`)
- **routes.py**: FastAPI endpoint'lerini tanımlar
- **models.py**: Request ve response şemalarını içerir (Pydantic)

### 2. Servis Katmanı (`app/services/`)
- **llm_service.py**: Ollama ile iletişim kurar
- **document_service.py**: Dokümanları yükler, işler, parçalar
- **rag_service.py**: RAG akışını yönetir (doküman arama + LLM prompt)

### 3. Utils Katmanı (`app/utils/`)
- **text_splitter.py**: Dokümanları chunk'lara böler
- **embeddings.py**: Metinleri vektörlere dönüştürür

### 4. Data Klasörü (`data/`)
- **documents/**: Kullanıcı dokümanları
- **vectordb/**: FAISS veya ChromaDB dosyaları

### 5. Tests Klasörü (`tests/`)
- Her modül için ayrı test dosyası
- pytest kullanılacak

## Neden Bu Yapı?

✅ **Separation of Concerns**: Her katmanın net sorumluluğu var
✅ **Genişletilebilirlik**: Yeni özellikler eklemek kolay
✅ **Test Edilebilirlik**: Her modül bağımsız test edilebilir
✅ **Okunabilirlik**: Kod organizasyonu açık ve anlaşılır
