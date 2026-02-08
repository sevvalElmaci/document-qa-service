"""
API Endpoint Testleri
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Health endpoint testleri"""
    
    def test_health_check_returns_200(self):
        """Health check 200 dönmeli"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
    
    def test_health_check_structure(self):
        """Health check doğru yapıda dönmeli"""
        response = client.get("/api/v1/health")
        data = response.json()
        
        assert "status" in data
        assert "service" in data
        assert "version" in data
        assert "rag_ready" in data
    
    def test_health_check_values(self):
        """Health check değerleri doğru olmalı"""
        response = client.get("/api/v1/health")
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["service"] == "Document QA Service"
        assert isinstance(data["rag_ready"], bool)


class TestAskEndpoint:
    """Ask endpoint testleri"""
    
    def test_ask_valid_question(self):
        """Geçerli soru 200 dönmeli"""
        payload = {"question": "What is Python?"}
        response = client.post("/api/v1/ask", json=payload)
        
        # RAG hazır değilse 503, hazırsa 200
        assert response.status_code in [200, 503]
    
    def test_ask_empty_question(self):
        """Boş soru 422 dönmeli"""
        payload = {"question": ""}
        response = client.post("/api/v1/ask", json=payload)
        assert response.status_code == 422
    
    def test_ask_short_question(self):
        """Çok kısa soru 422 dönmeli"""
        payload = {"question": "Hi"}
        response = client.post("/api/v1/ask", json=payload)
        assert response.status_code == 422
    
    def test_ask_long_question(self):
        """Çok uzun soru 422 dönmeli"""
        payload = {"question": "x" * 501}
        response = client.post("/api/v1/ask", json=payload)
        assert response.status_code == 422
    
    def test_ask_missing_question(self):
        """Eksik parametre 422 dönmeli"""
        payload = {}
        response = client.post("/api/v1/ask", json=payload)
        assert response.status_code == 422
    
    def test_ask_with_top_k(self):
        """top_k parametresi çalışmalı"""
        payload = {
            "question": "What is FastAPI?",
            "top_k": 5
        }
        response = client.post("/api/v1/ask", json=payload)
        assert response.status_code in [200, 503]
    
    def test_ask_invalid_top_k(self):
        """Geçersiz top_k 422 dönmeli"""
        payload = {
            "question": "What is FastAPI?",
            "top_k": 0  # min 1 olmalı
        }
        response = client.post("/api/v1/ask", json=payload)
        assert response.status_code == 422
    
    def test_ask_response_structure(self):
        """Response yapısı doğru olmalı (RAG hazırsa)"""
        payload = {"question": "What is Python?"}
        response = client.post("/api/v1/ask", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            assert "question" in data
            assert "answer" in data
            assert "sources" in data
            assert "confidence" in data
            assert isinstance(data["sources"], list)


class TestStatsEndpoint:
    """Stats endpoint testleri"""
    
    def test_stats_returns_200_or_503(self):
        """Stats endpoint 200 veya 503 dönmeli"""
        response = client.get("/api/v1/stats")
        assert response.status_code in [200, 503]
    
    def test_stats_structure(self):
        """Stats response yapısı doğru olmalı (RAG hazırsa)"""
        response = client.get("/api/v1/stats")
        
        if response.status_code == 200:
            data = response.json()
            assert "total_chunks" in data
            assert "indexed_documents" in data
            assert "embedding_model" in data


class TestRootEndpoint:
    """Root endpoint testleri"""
    
    def test_root_returns_200(self):
        """Root endpoint 200 dönmeli"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_structure(self):
        """Root response yapısı doğru olmalı"""
        response = client.get("/")
        data = response.json()
        
        assert "service" in data
        assert "version" in data
        assert "status" in data
        assert "docs" in data


# Çalıştırma
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
