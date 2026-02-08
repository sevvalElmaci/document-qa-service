"""
LLM Service için birim testleri
"""
import sys
sys.path.insert(0, 'D:\\projeler\\caseStudyLLM\\document-qa-service')

from app.services.llm_service import LLMService


def test_llm_service_init():
    """LLMService başlatma testi"""
    llm = LLMService()
    assert llm.model == "llama3"
    assert llm.base_url == "http://localhost:11434"
    print("✅ test_llm_service_init PASSED")


def test_chat_function():
    """Chat fonksiyonu testi"""
    llm = LLMService()
    response = llm.chat("Hello")
    
    # Cevap string olmalı
    assert isinstance(response, str)
    # Boş olmamalı
    assert len(response) > 0
    print("✅ test_chat_function PASSED")


def test_chat_with_error():
    """Hatalı URL ile test"""
    llm = LLMService()
    llm.base_url = "http://localhost:99999"  # Yanlış port
    
    response = llm.chat("Test")
    assert "Hata" in response
    print("✅ test_chat_with_error PASSED")


if __name__ == "__main__":
    print("🧪 LLM Service Testleri Başlıyor...\n")
    
    try:
        test_llm_service_init()
        test_chat_function()
        test_chat_with_error()
        print("\n✅ Tüm testler başarılı!")
    except AssertionError as e:
        print(f"\n❌ Test başarısız: {e}")
    except Exception as e:
        print(f"\n❌ Hata: {e}")