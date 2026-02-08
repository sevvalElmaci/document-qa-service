# 🚀 Hızlı Başlangıç Rehberi

## Proje Klasör Yapısını Oluşturma

Bu dosyalar proje yapınızın temelini oluşturur. Sırasıyla şu adımları izleyin:

### 1️⃣ Projeyi Oluşturun

```bash
# Proje klasörünü oluştur
mkdir document-qa-service
cd document-qa-service

# Git repository başlat
git init
```

### 2️⃣ Temel Dosyaları Ekleyin

Aşağıdaki dosyaları proje dizinine kopyalayın:
- ✅ `.gitignore`
- ✅ `requirements.txt`
- ✅ `README.md`
- ✅ `.env.example`
- ✅ `run.py`
- ✅ `setup_project.py`

### 3️⃣ Klasör Yapısını Oluşturun

```bash
# setup_project.py scriptini çalıştır
python setup_project.py
```

Bu script şu yapıyı oluşturacak:
```
document-qa-service/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
├── data/
│   ├── documents/
│   │   └── .gitkeep
│   └── vectordb/
│       └── .gitkeep
├── tests/
│   └── __init__.py
├── frontend/
└── docs/
```

### 4️⃣ Config Dosyasını Ekleyin

`app/config.py` dosyasını oluşturun (hazır template'i kullanın)

### 5️⃣ Virtual Environment Oluşturun

```bash
# Virtual environment oluştur
python -m venv venv

# Aktif et
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### 6️⃣ Bağımlılıkları Yükleyin

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 7️⃣ Environment Variables Ayarlayın

```bash
# .env.example dosyasını kopyala
cp .env.example .env

# Gerekirse ayarları düzenle
nano .env
```

### 8️⃣ Git İlk Commit

```bash
git add .
git commit -m "Initial project structure"
```

---

## ✅ Kontrol Listesi (Faz 1 - Gün 1)

- [x] GitHub repo oluştur → `git init`
- [x] Proje klasör yapısını kur → `python setup_project.py`
- [x] `.gitignore`, `requirements.txt` hazırla → ✅ Hazır
- [ ] LLM aracını seç ve test et → **Sırada bu!**

---

## 🎯 Sıradaki Adım: Ollama Kurulumu

Proje yapısı hazır! Şimdi Ollama'yı kurup ilk testi yapabiliriz.

**Komutlar:**
```bash
# Ollama'yı indir ve kur
# https://ollama.ai/download

# Model indir
ollama pull llama3

# Test et
ollama run llama3 "Merhaba, nasılsın?"
```

Hazır olduğunda bana haber ver, Ollama entegrasyonuna geçelim! 🚀
