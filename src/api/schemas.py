from pydantic import BaseModel, Field

class RequestCreate(BaseModel):
    """Схема создания заявки."""
    topic: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    category_id: int = Field(..., gt=0)
    priority: str = Field(..., pattern="^(Высокий|Средний|Низкий)$")
    requester_id: int = Field(..., gt=0)
    assignee_id: int | None = Field(None, gt=0)

class RequestUpdate(BaseModel):
    """Схема частичного обновления заявки."""
    topic: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, min_length=1)
    category_id: int | None = Field(None, gt=0)
    priority: str | None = Field(None, pattern="^(Высокий|Средний|Низкий)$")
    assignee_id: int | None = Field(None, gt=0)

class StatusUpdate(BaseModel):
    """Схема смены статуса."""
    status_id: int = Field(..., ge=1, le=4)

class RequestResponse(BaseModel):
    """Схема ответа заявки."""
    id: int
    request_number: str
    topic: str
    description: str
    priority: str
    created_at: str
    category_id: int
    status_id: int
    requester_id: int
    assignee_id: int | None