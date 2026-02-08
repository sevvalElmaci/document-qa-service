#!/usr/bin/env python3
"""
Proje klasör yapısını oluşturan script
"""

import os
from pathlib import Path

def create_project_structure():
    """Proje için gerekli klasör yapısını oluşturur"""
    
    base_dir = Path("document-qa-service")
    
    # Ana klasörler
    directories = [
        "app",
        "app/api",
        "app/services",
        "app/utils",
        "data/documents",
        "data/vectordb",
        "tests",
        "frontend",
        "docs",
    ]
    
    # __init__.py dosyaları gereken klasörler
    init_files = [
        "app/__init__.py",
        "app/api/__init__.py",
        "app/services/__init__.py",
        "app/utils/__init__.py",
        "tests/__init__.py",
    ]
    
    # .gitkeep dosyaları (boş klasörlerin git'te tutulması için)
    gitkeep_files = [
        "data/documents/.gitkeep",
        "data/vectordb/.gitkeep",
    ]
    
    print("📁 Proje klasör yapısı oluşturuluyor...")
    
    # Klasörleri oluştur
    for directory in directories:
        dir_path = base_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {directory}/")
    
    # __init__.py dosyalarını oluştur
    for init_file in init_files:
        file_path = base_dir / init_file
        file_path.touch()
        print(f"   ✓ {init_file}")
    
    # .gitkeep dosyalarını oluştur
    for gitkeep in gitkeep_files:
        file_path = base_dir / gitkeep
        file_path.touch()
        print(f"   ✓ {gitkeep}")
    
    print("\n✅ Klasör yapısı başarıyla oluşturuldu!")
    print(f"\n📂 Proje dizini: {base_dir.absolute()}")
    print("\n🚀 Sonraki adımlar:")
    print("   1. cd document-qa-service")
    print("   2. python -m venv venv")
    print("   3. source venv/bin/activate (veya Windows'ta venv\\Scripts\\activate)")
    print("   4. pip install -r requirements.txt")

if __name__ == "__main__":
    create_project_structure()
