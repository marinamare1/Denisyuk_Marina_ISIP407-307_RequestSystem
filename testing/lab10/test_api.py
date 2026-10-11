import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.main_api import app

client = TestClient(app)

# Бизнес-логика 

def test_get_all_requests():
    """GET /requests возвращает список заявок."""
    response = client.get("/requests")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_one_request():
    """GET /requests/1 возвращает заявку."""
    response = client.get("/requests/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "topic" in data

def test_create_request():
    """POST /requests создаёт заявку (201)."""
    payload = {
        "topic": "Автотест",
        "description": "Проверка создания",
        "category_id": 1,
        "priority": "Средний",
        "requester_id": 4
    }
    response = client.post("/requests", json=payload)
    assert response.status_code == 201
    assert "id" in response.json()

# API 

def test_health():
    """GET /health возвращает 200 и статус ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_nonexistent_request():
    """GET /requests/99999 возвращает 404."""
    response = client.get("/requests/99999")
    assert response.status_code == 404

def test_get_statuses():
    """GET /statuses возвращает список из 4 статусов."""
    response = client.get("/statuses")
    assert response.status_code == 200
    assert len(response.json()) == 4

# Валидация 

def test_create_empty_topic():
    """POST /requests с пустой темой — 422."""
    payload = {
        "topic": "",
        "description": "Описание",
        "category_id": 1,
        "priority": "Средний",
        "requester_id": 4
    }
    response = client.post("/requests", json=payload)
    assert response.status_code == 422

def test_create_invalid_priority():
    """POST /requests с неверным priority — 422."""
    payload = {
        "topic": "Тест",
        "description": "Описание",
        "category_id": 1,
        "priority": "Очень срочно",
        "requester_id": 4
    }
    response = client.post("/requests", json=payload)
    assert response.status_code == 422

# Регрессия

def test_status_change_forbidden():
    """Запрет перехода «В работе → Закрыта» — 400."""
    response = client.patch("/requests/1/status", json={"status_id": 4})
    assert response.status_code == 400

def test_categories_available():
    """GET /categories возвращает не менее 4 категорий."""
    response = client.get("/categories")
    assert response.status_code == 200
    assert len(response.json()) >= 4

# Запуск

if __name__ == "__main__":
    pytest.main([__file__, "-v"])