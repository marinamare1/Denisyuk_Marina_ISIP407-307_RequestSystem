from fastapi import APIRouter, HTTPException

from src.api.schemas import (RequestCreate, RequestUpdate, StatusUpdate, RequestResponse)
from src.service import request as request_service
from src.repository import user as user_repository
from src.repository import status as status_repository
from src.repository import category as category_repository

router = APIRouter()

@router.get("/health")
def health():
    """Проверка, что приложение работает."""
    return {"status": "ok"}

@router.get("/requests")
def list_requests(q: str | None = None,
                  status_id: int | None = None,
                  category_id: int | None = None):
    """Список заявок с поиском и фильтрацией."""
    if q:
        return request_service.search_requests(q)
    if status_id or category_id:
        return request_service.filter_requests(status_id, category_id)
    return request_service.get_all_requests()

@router.get("/requests/{request_id}", response_model=RequestResponse)
def get_request(request_id: int):
    """Заявка по id."""
    try:
        return request_service.get_request(request_id)
    except request_service.BusinessError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/requests", status_code=201)
def create_request(data: RequestCreate):
    """Создание заявки."""
    try:
        new_id = request_service.create_request(
            topic=data.topic,
            description=data.description,
            category_id=data.category_id,
            priority=data.priority,
            requester_id=data.requester_id,
            assignee_id=data.assignee_id,
        )
        return {"id": new_id, "message": "Заявка создана"}
    except request_service.ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.patch("/requests/{request_id}")
def update_request(request_id: int, data: RequestUpdate):
    """Частичное обновление заявки."""
    try:
        request_service.edit_request(
            request_id=request_id,
            topic=data.topic,
            description=data.description,
            category_id=data.category_id,
            priority=data.priority,
        )
        return request_service.get_request(request_id)
    except request_service.BusinessError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except request_service.ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.patch("/requests/{request_id}/status")
def change_status(request_id: int, data: StatusUpdate):
    """Смена статуса с проверкой перехода."""
    try:
        request_service.change_status(request_id, data.status_id)
        return {"id": request_id, "status_id": data.status_id,
                "message": "Статус изменён"}
    except request_service.BusinessError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/requests/{request_id}", status_code=204)
def delete_request(request_id: int):
    """Удаление заявки."""
    try:
        request_service.delete_request(request_id)
    except request_service.BusinessError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users")
def list_users():
    """Список пользователей."""
    return user_repository.get_all()

@router.get("/statuses")
def list_statuses():
    """Справочник статусов."""
    return status_repository.get_all()

@router.get("/categories")
def list_categories():
    """Справочник категорий."""
    return category_repository.get_all()